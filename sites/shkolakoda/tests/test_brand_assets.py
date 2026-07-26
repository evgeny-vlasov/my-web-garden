import base64
import re
import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
BRAND_GUIDE = SITE_ROOT / "BRAND.md"
STATIC_ROOT = SITE_ROOT / "static"
BRAND_ROOT = STATIC_ROOT / "brand"
LOGO_ROOT = BRAND_ROOT / "logos"
MASCOT_ROOT = BRAND_ROOT / "mascot"
TEMPLATE_ROOT = BRAND_ROOT / "templates"
SVG_NS = "{http://www.w3.org/2000/svg}"
POINTS_PER_MM = 72 / 25.4

COMPLETE_WORDMARK_MIN_SCREEN_PX = 540
COMPLETE_WORDMARK_MIN_PRINT_MM = 120
REDUCED_WORDMARK_MIN_SCREEN_PX = 240
REDUCED_WORDMARK_MIN_PRINT_MM = 45


EXPECTED_SVGS = {
    LOGO_ROOT / "favicon.svg": (0, 0, 64, 64),
    LOGO_ROOT / "compact-badge.svg": (-6, -6, 112, 96),
    LOGO_ROOT / "compact-badge-mono.svg": (-6, -6, 112, 96),
    LOGO_ROOT / "compact-badge-reversed.svg": (-6, -6, 112, 96),
    LOGO_ROOT / "wordmark-horizontal.svg": (0, 0, 720, 150),
    LOGO_ROOT / "wordmark-horizontal-mono.svg": (0, 0, 720, 150),
    LOGO_ROOT / "wordmark-horizontal-reversed.svg": (0, 0, 720, 150),
    LOGO_ROOT / "wordmark-horizontal-reduced.svg": (0, 0, 580, 120),
    LOGO_ROOT / "wordmark-horizontal-reduced-mono.svg": (0, 0, 580, 120),
    LOGO_ROOT / "wordmark-horizontal-reduced-reversed.svg": (0, 0, 580, 120),
    LOGO_ROOT / "wordmark-stacked.svg": (0, 0, 520, 360),
    LOGO_ROOT / "wordmark-stacked-mono.svg": (0, 0, 520, 360),
    LOGO_ROOT / "wordmark-stacked-reversed.svg": (0, 0, 520, 360),
    LOGO_ROOT / "social-avatar.svg": (0, 0, 1080, 1080),
    LOGO_ROOT / "facebook-cover.svg": (0, 0, 1702, 630),
    TEMPLATE_ROOT / "social-post-1080-square.svg": (0, 0, 1080, 1080),
    TEMPLATE_ROOT / "social-post-1080x1350.svg": (0, 0, 1080, 1350),
    TEMPLATE_ROOT / "social-story-1080x1920.svg": (0, 0, 1080, 1920),
    TEMPLATE_ROOT / "social-card-1200x630.svg": (0, 0, 1200, 630),
    TEMPLATE_ROOT / "project-illustration-frame.svg": (0, 0, 1200, 900),
    TEMPLATE_ROOT / "photo-plus-caption.svg": (0, 0, 1200, 1500),
}

EXPECTED_MASCOT_RASTERS = {
    MASCOT_ROOT / "robot-avatar-500.png": ("png", 500, 500, True),
    MASCOT_ROOT / "robot-avatar-256.png": ("png", 256, 256, True),
    MASCOT_ROOT / "robot-avatar-96.png": ("png", 96, 96, True),
    MASCOT_ROOT / "robot-editorial-1024.webp": ("webp", 1024, 1024, False),
    MASCOT_ROOT / "robot-editorial-640.webp": ("webp", 640, 640, False),
}

EXPECTED_TOKENS = {
    "ink": "#151515",
    "paper": "#fffef8",
    "white": "#ffffff",
    "muted": "#5c5c57",
    "line": "#d8d6ca",
    "soft-line": "#ebe9de",
    "yellow": "#f4c542",
    "yellow-soft": "#fff4bd",
    "green": "#147d64",
    "green-soft": "#e2f4ed",
    "blue": "#2257b5",
    "blue-soft": "#e9effb",
    "red": "#c93d32",
    "red-soft": "#fde9e5",
    "violet": "#6946a4",
}


def parse_view_box(value):
    return tuple(float(part) for part in value.replace(",", " ").split())


def relative_luminance(hex_colour):
    values = [int(hex_colour[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
        for value in values
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first, second):
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def png_info(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path} is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    colour_type = data[25]
    chunks = []
    offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8].decode("ascii")
        chunks.append(chunk_type)
        offset += 12 + length
        if chunk_type == "IEND":
            break
    return width, height, colour_type in {4, 6}, chunks


def webp_info(path):
    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise AssertionError(f"{path} is not a WebP")
    chunks = []
    width = height = None
    has_alpha = False
    offset = 12
    while offset + 8 <= len(data):
        chunk_type = data[offset : offset + 4].decode("ascii")
        length = struct.unpack("<I", data[offset + 4 : offset + 8])[0]
        payload = data[offset + 8 : offset + 8 + length]
        chunks.append(chunk_type)
        if chunk_type == "VP8X":
            has_alpha = bool(payload[0] & 0x10)
            width = 1 + int.from_bytes(payload[4:7], "little")
            height = 1 + int.from_bytes(payload[7:10], "little")
        elif chunk_type == "VP8 " and len(payload) >= 10:
            width = struct.unpack("<H", payload[6:8])[0] & 0x3FFF
            height = struct.unpack("<H", payload[8:10])[0] & 0x3FFF
        elif chunk_type == "VP8L" and len(payload) >= 5:
            bits = int.from_bytes(payload[1:5], "little")
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            has_alpha = True
        offset += 8 + length + (length % 2)
    if width is None or height is None:
        raise AssertionError(f"Could not read WebP dimensions for {path}")
    return width, height, has_alpha, chunks


class BrandAssetTests(unittest.TestCase):
    def test_all_expected_svg_masters_are_valid(self):
        self.assertEqual(set(BRAND_ROOT.rglob("*.svg")), set(EXPECTED_SVGS))
        for path, expected_view_box in EXPECTED_SVGS.items():
            with self.subTest(asset=path.name):
                tree = ET.parse(path)
                root = tree.getroot()
                self.assertEqual(root.tag, f"{SVG_NS}svg")
                self.assertEqual(parse_view_box(root.attrib["viewBox"]), expected_view_box)
                self.assertIsNone(root.find(f".//{SVG_NS}script"))
                self.assertIsNone(root.find(f".//{SVG_NS}foreignObject"))
                if path.name != "favicon.svg":
                    self.assertIsNotNone(root.find(f"{SVG_NS}title"))
                    self.assertIsNotNone(root.find(f"{SVG_NS}desc"))

    def test_svg_links_are_local_and_resolve(self):
        href_names = ("href", "{http://www.w3.org/1999/xlink}href")
        for path in EXPECTED_SVGS:
            root = ET.parse(path).getroot()
            for element in root.iter():
                for name in href_names:
                    href = element.attrib.get(name)
                    if not href or href.startswith("#"):
                        continue
                    if href.startswith("data:image/png;base64,"):
                        with self.subTest(asset=path.name, href="embedded PNG"):
                            encoded = href.partition(",")[2]
                            self.assertEqual(
                                base64.b64decode(encoded),
                                (MASCOT_ROOT / "robot-avatar-256.png").read_bytes(),
                            )
                        continue
                    with self.subTest(asset=path.name, href=href):
                        self.assertNotRegex(href, r"^[a-z]+://")
                        self.assertTrue((path.parent / href).resolve().is_file())

    def test_story_template_has_unique_editable_regions_and_safe_area(self):
        path = TEMPLATE_ROOT / "social-story-1080x1920.svg"
        root = ET.parse(path).getroot()
        ids = [
            element.attrib["id"]
            for element in root.iter()
            if "id" in element.attrib
        ]
        editable = [
            element.attrib["data-edit"]
            for element in root.iter()
            if "data-edit" in element.attrib
        ]

        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(editable), len(set(editable)))
        self.assertEqual(
            set(editable),
            {"eyebrow", "headline", "supporting-points", "callout", "url"},
        )
        source = path.read_text(encoding="utf-8")
        self.assertIn("STORY SAFE AREA", source)
        self.assertIn("INPUT → RULE → OUTPUT", source)

    def test_wordmark_assets_use_the_public_name(self):
        for path in LOGO_ROOT.glob("*.svg"):
            source = path.read_text(encoding="utf-8")
            with self.subTest(asset=path.name):
                self.assertNotIn("SHKOLA CODA", source.upper())
                if "wordmark" in path.name or path.name == "facebook-cover.svg":
                    self.assertIn("School of Code", source)
                    if "reduced" in path.name:
                        self.assertNotIn("COMPUTER LAB / CALGARY", source)
                    else:
                        self.assertIn("COMPUTER LAB / CALGARY", source)

    def test_canonical_favicon_matches_the_live_favicon(self):
        self.assertEqual(
            (LOGO_ROOT / "favicon.svg").read_bytes(),
            (STATIC_ROOT / "favicon.svg").read_bytes(),
        )

    def test_brand_tokens_match_existing_css(self):
        css = (STATIC_ROOT / "css" / "styles.css").read_text(encoding="utf-8")
        for token, value in EXPECTED_TOKENS.items():
            with self.subTest(token=token):
                pattern = rf"--{re.escape(token)}:\s*{re.escape(value)}\s*;"
                self.assertRegex(css, pattern)

    def test_core_contrast_pairs_meet_wcag_aa(self):
        paper = EXPECTED_TOKENS["paper"]
        normal_text_pairs = [
            ("ink", paper),
            ("muted", paper),
            ("green", paper),
            ("blue", paper),
            ("red", paper),
            ("violet", paper),
        ]
        for token, background in normal_text_pairs:
            with self.subTest(pair=f"{token}/paper"):
                self.assertGreaterEqual(
                    contrast_ratio(EXPECTED_TOKENS[token], background), 4.5
                )
        self.assertGreaterEqual(
            contrast_ratio(EXPECTED_TOKENS["ink"], EXPECTED_TOKENS["yellow"]), 4.5
        )
        for foreground, background in (
            ("#6e5500", EXPECTED_TOKENS["yellow-soft"]),
            ("#075b47", EXPECTED_TOKENS["green-soft"]),
        ):
            with self.subTest(pair=f"{foreground}/{background}"):
                self.assertGreaterEqual(
                    contrast_ratio(foreground, background), 4.5
                )
        for token in ("green", "blue", "red", "violet"):
            with self.subTest(pair=f"white/{token}"):
                self.assertGreaterEqual(
                    contrast_ratio(EXPECTED_TOKENS["white"], EXPECTED_TOKENS[token]),
                    4.5,
                )

    def test_small_size_geometry_has_a_legible_floor(self):
        # Existing favicon: 5 SVG units become 1.25 px at a 16 px display size.
        self.assertGreaterEqual(5 * 16 / 64, 1.0)
        # Compact badge: border and live type at the existing 44 px mobile width.
        self.assertGreaterEqual(4 * 44 / 112, 1.25)
        self.assertGreaterEqual(27 * 44 / 112, 10.0)
        # Institutional avatar: transformed 5-unit mark stroke at a 36 px avatar.
        self.assertGreaterEqual((5 * 11) * 36 / 1080, 1.5)
        # The 96 px mascot is a native 2x source for the 48 px minimum.
        self.assertTrue((MASCOT_ROOT / "robot-avatar-96.png").is_file())

    def test_horizontal_wordmarks_have_legible_final_output_sizes(self):
        complete_path = LOGO_ROOT / "wordmark-horizontal.svg"
        complete_root = ET.parse(complete_path).getroot()
        complete_width = parse_view_box(complete_root.attrib["viewBox"])[2]
        descriptor = next(
            element
            for element in complete_root.iter(f"{SVG_NS}text")
            if "".join(element.itertext()).strip() == "COMPUTER LAB / CALGARY"
        )
        descriptor_size = float(descriptor.attrib["font-size"])

        descriptor_screen_px = (
            descriptor_size * COMPLETE_WORDMARK_MIN_SCREEN_PX / complete_width
        )
        descriptor_print_pt = (
            descriptor_size
            * COMPLETE_WORDMARK_MIN_PRINT_MM
            / complete_width
            * POINTS_PER_MM
        )
        self.assertGreaterEqual(descriptor_screen_px, 12)
        self.assertGreaterEqual(descriptor_print_pt, 7.5)

        for suffix in ("", "-mono", "-reversed"):
            reduced_path = (
                LOGO_ROOT / f"wordmark-horizontal-reduced{suffix}.svg"
            )
            reduced_root = ET.parse(reduced_path).getroot()
            reduced_width = parse_view_box(reduced_root.attrib["viewBox"])[2]
            texts = {
                "".join(element.itertext()).strip(): element
                for element in reduced_root.iter(f"{SVG_NS}text")
            }
            with self.subTest(asset=reduced_path.name):
                self.assertNotIn("COMPUTER LAB / CALGARY", texts)
                name = texts["School of Code"]
                name_size = float(name.attrib["font-size"])
                badge_size = float(texts["<SC/>"].attrib["font-size"])
                # Reserve nine ems for the name so common system-serif
                # fallbacks do not clip at the right edge.
                self.assertGreaterEqual(
                    (reduced_width - float(name.attrib["x"])) / name_size,
                    9,
                )
                self.assertGreaterEqual(
                    name_size * REDUCED_WORDMARK_MIN_SCREEN_PX / reduced_width,
                    20,
                )
                self.assertGreaterEqual(
                    badge_size * REDUCED_WORDMARK_MIN_SCREEN_PX / reduced_width,
                    11,
                )
                self.assertGreaterEqual(
                    name_size
                    * REDUCED_WORDMARK_MIN_PRINT_MM
                    / reduced_width
                    * POINTS_PER_MM,
                    10.5,
                )
                self.assertGreaterEqual(
                    badge_size
                    * REDUCED_WORDMARK_MIN_PRINT_MM
                    / reduced_width
                    * POINTS_PER_MM,
                    5.5,
                )

        guide = BRAND_GUIDE.read_text(encoding="utf-8")
        self.assertIn("at least 540 px wide on screen", guide)
        self.assertIn("at least 120 mm wide in print", guide)
        self.assertIn("From 240–539 px on screen or 45–119 mm in print", guide)

    def test_mascot_rasters_have_expected_dimensions_and_no_metadata(self):
        self.assertEqual(set(MASCOT_ROOT.iterdir()), set(EXPECTED_MASCOT_RASTERS))
        for path, (format_name, expected_width, expected_height, expected_alpha) in (
            EXPECTED_MASCOT_RASTERS.items()
        ):
            with self.subTest(asset=path.name):
                if format_name == "png":
                    width, height, has_alpha, chunks = png_info(path)
                    self.assertTrue(
                        {"eXIf", "iTXt", "tEXt", "zTXt"}.isdisjoint(chunks)
                    )
                else:
                    width, height, has_alpha, chunks = webp_info(path)
                    self.assertTrue({"EXIF", "XMP ", "ICCP"}.isdisjoint(chunks))
                self.assertEqual((width, height), (expected_width, expected_height))
                self.assertEqual(has_alpha, expected_alpha)

    def test_no_raw_archives_or_student_photos_enter_brand_assets(self):
        forbidden_suffixes = {".zip", ".jpg", ".jpeg"}
        committed_brand_files = [path for path in BRAND_ROOT.rglob("*") if path.is_file()]
        self.assertFalse(
            [path for path in committed_brand_files if path.suffix.lower() in forbidden_suffixes]
        )

    def test_private_reference_photo_copy_uses_confirmed_date_and_privacy_rules(self):
        manifest = (SITE_ROOT / "brand" / "PHOTO_MANIFEST.md").read_text(
            encoding="utf-8"
        )
        guide = BRAND_GUIDE.read_text(encoding="utf-8")
        template = (TEMPLATE_ROOT / "photo-plus-caption.svg").read_text(
            encoding="utf-8"
        )

        self.assertIn("19 November 2021", manifest)
        self.assertIn("ground-truth capture date", manifest)
        self.assertIn("private visual references", manifest)
        self.assertIn("separate documentary", manifest)
        self.assertIn("other student identities", manifest)
        self.assertIn("19 November 2021", guide)
        self.assertIn("separate documentary collection", guide)
        self.assertIn("PROVENANCE: KEEP PRIVATE", template)
        self.assertIn("student identities out of public copy", template)


if __name__ == "__main__":
    unittest.main()
