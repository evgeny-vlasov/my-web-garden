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
            "campaign-scratch-class-v2.png",
            "campaign-eugene-builder-v1.png",
            "campaign-project-workbench-v1.png",
        }
        reconstructed = {"reconstructed-coding-together-v1.png"}
        documentary = {
            "historical-robot-testing.jpg",
            "historical-workbench-apparatus.jpg",
            "historical-robot-adjustment.jpg",
            "historical-scratch-use.jpg",
            "historical-classroom-context.jpg",
        }
        self.assertEqual({path.name for path in MASTER_ROOT.glob("*.png")}, campaign | reconstructed)
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
                    "reconstructed coding-class scene", "canonical identity",
                    "branded reconstructed campaign image",
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
        card_slugs = {
            path.name.rsplit("-", 1)[0]
            for pattern in ("historical-*-400.avif", "reconstructed-*-400.avif")
            for path in WEB_ROOT.glob(pattern)
        }
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

    def test_withdrawn_child_images_and_hashes_are_absent(self):
        withdrawn_names = {
            "campaign-scratch-lab-v1.png",
            "historical-coding-together.jpg",
        }
        withdrawn_hashes = {
            "09505f2153b5e53250e4209869e200add947dcecb4448aa0dadf26b1583760a6",
            "09711bdc8c0a050ad8c86132c7a04e0a090dff20340f2739cd730eacf4de13c9",
            "0c620ec88fcf2bbc51bb4d0e2fe9d91aac9e2b08b57c6077d6197ba243c954bb",
            "11577fb58b74a7016a3578342309c642bece96fecb44896e4c9ba1d77b111593",
            "1f8c30a75ca3d6f89b59803b34ad4f11a8ddf7bace1eb360a6ca5960f1c334f5",
            "245fb8801bb498ee9f7cb9db4275b010dee666b205bb1182cf8f293bbd2693a7",
            "26da5a7335e6f147614ca8506fc7fa489853a1656b94ad1858889dd979e5e15f",
            "292a46ed5d66ccf27b983f399add86e2e6486736325e20f2162184ffe70d4893",
            "3672ca6b6fd9877ca638fc42a48eb273a4646331a846632e1a74f2c3c2f2ffde",
            "453f99907baa659534ac781c2be11eadcfe65527a9669a297d447d986ada96e3",
            "473957885c6fb1738b76677e8aa2c99a835af1e3b68a02d882de796d728a38b1",
            "48a8d97c24ca46c6aa0bacd1e89aa53c1a4bb3a555da4473bd53e657f862576e",
            "4cd25118397df7e7204b37ef613ebab8602711ffdcb12ac454ddb5164fe31e33",
            "4ef0080480c6c8e8a189d568951f34062bd1dfbd32fceff7112a510c3bc59eaf",
            "5dd4fac1b4ddb19afdce6c402bf2695951841ce3ce9b44e490a8e8dac3907fc9",
            "648151113534191c1b05ed3748cc72f6b1699b5332c6b6616a0b4ca56f702c12",
            "68781090e2aead71cc0367ac3b94b0657fcb42c328ca023090b4c75b34ec2769",
            "71f7e75387720aae289536e70c9d0ab3e9634c49f8000a62521ed26a238d5bc3",
            "84835eb43f448876862203e65fa6e330d95e831e9c49661c1f862fbc647e638a",
            "865f207b8f7062d74a95ddc00beae3a759d6355ec26ef2e5fdfe832af63aed09",
            "897497acb3b5d4008a653351b89fe01887b99054bb33ac446d8ffe2e34c1e5f9",
            "8a3129aa0d9d6df6b527da8d4c8ef62aaa9f8cdae03089776fee67089abe3e8b",
            "938ac81e44dc81126ddbf89e89e9e1c858c6d614bc2c2ca615241a8cee6d6484",
            "96fe4e7364acbe83a415a165b2cbeb9d99575a08c7dc68b24b9dccaab41a33e0",
            "99ac3e119f1f5e728814bc9fb5cf00195b9b15759132fb38a50bb9fea145502a",
            "9a1c3f0c9bf65a3ddcd7ef42dd9b3722434e22c1996c011536078abcbd8da94d",
            "9c604a1edbd8d0d34c4aae32e0a49be1ab1c3e0c6ea44eb85ed70b104af2b996",
            "9d756b2223870a465ba95b843ed41902ebedc8524fd6030e2989defbcfada382",
            "a3792170fd20c38e457f6bc9b6560bb7751cfaf2c08ae75ba0c9cc0a1719e970",
            "ad64809a84ff06c99f1e13d0fa9340019851c570264d93092ef829335ba4b293",
            "adc592846fd4c83208d16a0ab99f876c56c87af77552248c614f4a4d42309e74",
            "b66d64e8e402a2607e5754aa24cf3b61839b289d4af8682bfdcaf4820de78454",
            "bf5852df2e45b65b36b770f0b7ba7595fc17e69ac9d7aaef1c6d15f2095ac084",
            "d36bb2595907e20fbb7f7f86e38832f447189eb019629f6cdd8a455a3072be66",
            "d4d08a8864ec530f799a35fe867e1bf72cf37c7c59b0e2d73dc5a1735addf64a",
            "dd2e757a5e51eba20e23f9a5497010b9f38d768cef77502ae606cf96d91b4734",
            "dd73e2d0134bc6826faad5ff0d5ef794ab739d43ff65a00c0a02ab24d61b5075",
            "e157cf9e69e3e0bd5e641f30ffc55bbb19f0be3e369505ee1121155197ae03ad",
            "e1d6deb93383dca04b63a71ed497925674aed0e3a2df97880d1f159008cdb6c3",
            "e4ecb73bb9d0caf88d4eb998cda06d2ee41235a47d7a84c18052ee39deb8435a",
            "f63ebb1b9431c737845936cc92e48519e31be96c49c943f43fd5f77a0c8e70dd",
            "f931ecad064fa2856665e7065c099a1e6e75f4e1f069a21a3dc61a0753cf7322",
        }
        production_roots = (MASTER_ROOT, WEB_ROOT, SOCIAL_ROOT, PREVIEW_ROOT)
        production_files = [
            path
            for root in production_roots
            for path in root.rglob("*")
            if path.is_file()
        ]
        self.assertFalse(withdrawn_names & {path.name for path in production_files})
        self.assertFalse(withdrawn_hashes & {digest(path) for path in production_files})
        manifest_text = MANIFEST_PATH.read_text(encoding="utf-8")
        for filename in withdrawn_names:
            self.assertNotIn(filename, manifest_text)
        for old_hash in withdrawn_hashes:
            self.assertNotIn(old_hash, manifest_text)

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
