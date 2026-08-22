import hashlib
import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SITE_ROOT / "brand" / "photo-asset-manifest.json"
MASTER_ROOT = SITE_ROOT / "brand" / "photo-masters"
WEB_ROOT = SITE_ROOT / "static" / "brand" / "photos"
SOCIAL_ROOT = SITE_ROOT / "brand" / "social" / "exports"
PREVIEW_ROOT = SITE_ROOT / "brand" / "social" / "previews"
TEMPLATE_ROOT = SITE_ROOT / "static" / "brand" / "templates"
SVG_NS = "{http://www.w3.org/2000/svg}"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError("invalid PNG")
    return struct.unpack(">II", data[16:24])


def jpeg_dimensions(data):
    if data[:2] != b"\xff\xd8":
        raise AssertionError("invalid JPEG")
    offset = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while offset + 9 < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker in {0xD8, 0xD9}:
            continue
        length = struct.unpack(">H", data[offset : offset + 2])[0]
        if marker in sof:
            height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
            return width, height
        offset += length
    raise AssertionError("JPEG dimensions not found")


def raster_dimensions(path):
    data = path.read_bytes()
    if path.suffix.lower() == ".png":
        return png_dimensions(data)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        return jpeg_dimensions(data)
    raise AssertionError(f"unsupported direct dimension check: {path}")


class PhotoAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.records = {record["path"]: record for record in cls.manifest["assets"]}

    def test_required_masters_and_documentary_set(self):
        campaign = {
            "campaign-robotics-hero-v1.png",
            "campaign-scratch-lab-v1.png",
            "campaign-eugene-builder-v1.png",
            "campaign-project-workbench-v1.png",
        }
        documentary = {
            "historical-robot-testing.jpg",
            "historical-coding-together.jpg",
            "historical-workbench-apparatus.jpg",
            "historical-robot-adjustment.jpg",
            "historical-scratch-use.jpg",
            "historical-classroom-context.jpg",
        }
        self.assertEqual({path.name for path in MASTER_ROOT.glob("*.png")}, campaign)
        self.assertEqual({path.name for path in (MASTER_ROOT / "documentary").glob("*.jpg")}, documentary)

    def test_manifest_covers_every_published_photo_and_hash(self):
        roots = (MASTER_ROOT, WEB_ROOT, SOCIAL_ROOT)
        published = {
            path.relative_to(SITE_ROOT).as_posix()
            for root in roots
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(set(self.records), published)
        required = {
            "semantic_role", "origin", "classification", "dimensions", "format",
            "crop_focal_point", "intended_pages_placements", "alt_text",
            "rights_confirmation", "metadata_removal_status", "sha256",
        }
        for relative, record in self.records.items():
            with self.subTest(asset=relative):
                self.assertTrue(required.issubset(record))
                self.assertEqual(record["sha256"], digest(SITE_ROOT / relative))
                self.assertIn(record["classification"], {
                    "reconstructed campaign image", "historical workshop photograph",
                    "canonical identity", "branded reconstructed campaign image",
                })

    def test_exact_social_dimensions(self):
        expected = {
            "identity/facebook-page-profile-1024.png": (1024, 1024),
            "covers/facebook-page-cover-clean.jpg": (1920, 800),
            "covers/facebook-page-cover-branded.png": (1920, 800),
            "covers/facebook-group-cover-clean.jpg": (1640, 856),
            "covers/facebook-group-cover-branded.png": (1640, 856),
            "covers/facebook-event-cover-clean.jpg": (1920, 1005),
            "covers/facebook-event-cover-branded.png": (1920, 1005),
            "covers/open-graph-link-preview-clean.jpg": (1200, 630),
            "covers/open-graph-link-preview-branded.png": (1200, 630),
        }
        for family in ("robotics", "scratch-lab", "eugene-teacher"):
            expected.update({
                f"campaigns/{family}/feed-square-1440.jpg": (1440, 1440),
                f"campaigns/{family}/feed-portrait-1440x1800.jpg": (1440, 1800),
                f"campaigns/{family}/feed-landscape-1440x754.jpg": (1440, 754),
                f"campaigns/{family}/story-reel-master-1440x2560.png": (1440, 2560),
                f"campaigns/{family}/story-reel-delivery-1080x1920.png": (1080, 1920),
            })
        for relative, dimensions in expected.items():
            with self.subTest(asset=relative):
                self.assertEqual(raster_dimensions(SOCIAL_ROOT / relative), dimensions)

    def test_responsive_widths_and_file_signatures(self):
        hero_slugs = {
            "home-hero", "robotics-banner", "scratch-banner", "computer-lab-banner",
            "teacher-about", "teacher-parents", "projects-workbench", "lessons-workbench",
        }
        card_slugs = {path.name.rsplit("-", 1)[0] for path in WEB_ROOT.glob("historical-*-400.avif")}
        for slug in hero_slugs:
            widths = (480, 768, 1200, 1600)
            for width in widths:
                for extension, signature in (("avif", b"ftypavif"), ("webp", b"WEBP"), ("jpg", b"\xff\xd8")):
                    path = WEB_ROOT / f"{slug}-{width}.{extension}"
                    with self.subTest(asset=path.name):
                        self.assertTrue(path.is_file())
                        data = path.read_bytes()[:32]
                        self.assertIn(signature, data)
                        self.assertEqual(self.records[path.relative_to(SITE_ROOT).as_posix()]["dimensions"]["width"], width)
        self.assertEqual(len(card_slugs), 6)

    def test_published_rasters_have_no_private_metadata_markers(self):
        forbidden = (b"Exif\x00\x00", b"http://ns.adobe.com/xap/1.0/", b"GPSLatitude", b"GPSLongitude", b"XML:com.adobe.xmp", b"Comment")
        for root in (MASTER_ROOT, WEB_ROOT, SOCIAL_ROOT, PREVIEW_ROOT):
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                data = path.read_bytes()
                with self.subTest(asset=path.relative_to(SITE_ROOT)):
                    for marker in forbidden:
                        self.assertNotIn(marker, data)

    def test_page_weight_targets(self):
        self.assertLessEqual((WEB_ROOT / "home-hero-480.avif").stat().st_size, 250_000)
        self.assertLessEqual((WEB_ROOT / "home-hero-1600.avif").stat().st_size, 400_000)
        for path in WEB_ROOT.glob("historical-*-400.avif"):
            with self.subTest(asset=path.name):
                self.assertLessEqual(path.stat().st_size, 150_000)

    def test_story_safe_zone_and_template_previews(self):
        root = ET.parse(TEMPLATE_ROOT / "social-story-1080x1920.svg").getroot()
        constants = root.find(f"{SVG_NS}metadata[@id='story-safe-area-constants']")
        self.assertEqual(
            {name: constants.attrib[name] for name in ("data-safe-left", "data-safe-top", "data-safe-right", "data-safe-bottom")},
            {"data-safe-left": "65", "data-safe-top": "269", "data-safe-right": "1015", "data-safe-bottom": "1248"},
        )
        templates = {path.stem for path in TEMPLATE_ROOT.glob("*.svg")}
        previews = {path.stem for path in PREVIEW_ROOT.glob("*.png")}
        self.assertEqual(previews, templates)
        for preview in PREVIEW_ROOT.glob("*.png"):
            self.assertEqual(preview.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_templates_reference_tracked_photos_and_alt_behavior(self):
        templates = "\n".join(path.read_text(encoding="utf-8") for path in (SITE_ROOT / "templates").glob("*.html"))
        referenced = set(re.findall(r"responsive_photo\('([^']+)'", templates))
        self.assertTrue({"home-hero", "robotics-banner", "scratch-banner", "computer-lab-banner", "teacher-about", "teacher-parents", "projects-workbench", "lessons-workbench"}.issubset(referenced))
        for slug in referenced:
            self.assertTrue(any(WEB_ROOT.glob(f"{slug}-*.avif")), slug)
        self.assertIn("alt=\"{{ alt }}\"", (SITE_ROOT / "templates" / "_macros.html").read_text(encoding="utf-8"))

    def test_profile_uses_canonical_logo_source(self):
        relative = "brand/social/exports/identity/facebook-page-profile-1024.png"
        self.assertEqual(self.records[relative]["origin"], "static/brand/logos/social-avatar.svg")
        builder = (SITE_ROOT / "brand" / "build_photo_assets.py").read_text(encoding="utf-8")
        self.assertIn('logo_root / "social-avatar.svg"', builder)
        self.assertNotIn("image_gen", builder)


if __name__ == "__main__":
    unittest.main()
