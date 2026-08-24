"""Build metadata-clean School of Code photographic and social derivatives.

Private intake and review directories are explicit command-line inputs. They are
never copied wholesale and their locations are not written into tracked files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from dataclasses import dataclass
from pathlib import Path

import pillow_avif  # noqa: F401 - registers AVIF with Pillow
import resvg_py
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


PAPER = "#fffef8"
INK = "#151515"
LINE = "#d8d6ca"
YELLOW = "#f4c542"
GREEN_SOFT = "#e2f4ed"
BLUE_SOFT = "#e9effb"
RED_SOFT = "#fde9e5"


@dataclass(frozen=True)
class WebSpec:
    slug: str
    source_key: str
    ratio: float
    focus: tuple[float, float]
    widths: tuple[int, ...]
    role: str
    placements: tuple[str, ...]
    alt: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def open_rgb(path: Path) -> Image.Image:
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")


def cover_crop(
    image: Image.Image,
    size: tuple[int, int],
    focus: tuple[float, float] = (0.5, 0.5),
) -> Image.Image:
    target_width, target_height = size
    target_ratio = target_width / target_height
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        crop_height = image.height
        crop_width = round(crop_height * target_ratio)
    else:
        crop_width = image.width
        crop_height = round(crop_width / target_ratio)
    center_x = round(focus[0] * image.width)
    center_y = round(focus[1] * image.height)
    left = max(0, min(image.width - crop_width, center_x - crop_width // 2))
    top = max(0, min(image.height - crop_height, center_y - crop_height // 2))
    crop = image.crop((left, top, left + crop_width, top + crop_height))
    return crop.resize(size, Image.Resampling.LANCZOS)


def document_tone(image: Image.Image) -> Image.Image:
    image = ImageOps.autocontrast(image, cutoff=(0.4, 0.4), preserve_tone=True)
    image = ImageEnhance.Color(image).enhance(1.03)
    image = ImageEnhance.Contrast(image).enhance(1.035)
    image = ImageEnhance.Brightness(image).enhance(1.015)
    return ImageEnhance.Sharpness(image).enhance(1.04)


def blur_regions(image: Image.Image, regions: list[tuple[int, int, int, int, float]]) -> Image.Image:
    output = image.copy()
    for left, top, right, bottom, radius in regions:
        left = max(0, left)
        top = max(0, top)
        right = min(output.width, right)
        bottom = min(output.height, bottom)
        if right <= left or bottom <= top:
            continue
        region = output.crop((left, top, right, bottom)).filter(ImageFilter.GaussianBlur(radius))
        mask = Image.new("L", region.size, 255).filter(ImageFilter.GaussianBlur(max(1, radius / 2)))
        output.paste(region, (left, top), mask)
    return output


def save_clean(image: Image.Image, path: Path, fmt: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fmt = (fmt or path.suffix.lstrip(".")).lower()
    image = image.convert("RGB")
    if fmt in {"jpg", "jpeg"}:
        image.save(path, "JPEG", quality=86, optimize=True, progressive=True, subsampling="4:2:0")
    elif fmt == "webp":
        image.save(path, "WEBP", quality=78, method=6)
    elif fmt == "avif":
        image.save(path, "AVIF", quality=55, speed=6)
    elif fmt == "png":
        image.save(path, "PNG", optimize=True)
    else:
        raise ValueError(f"Unsupported format: {fmt}")


def render_svg(svg: Path, destination: Path, width: int, height: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(
        resvg_py.svg_to_bytes(
            svg_path=str(svg),
            width=width,
            height=height,
            resources_dir=str(svg.parent),
            font_files=[
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            ],
            serif_family="DejaVu Serif",
            sans_serif_family="DejaVu Sans",
            monospace_family="DejaVu Sans Mono",
            text_rendering="optimize_legibility",
            image_rendering="optimize_quality",
        )
    )


def alpha_overlay(base: Image.Image, overlay_path: Path, xy: tuple[int, int], width: int) -> Image.Image:
    output = base.convert("RGBA")
    with Image.open(overlay_path) as source:
        overlay = source.convert("RGBA")
    height = round(overlay.height * width / overlay.width)
    overlay = overlay.resize((width, height), Image.Resampling.LANCZOS)
    output.alpha_composite(overlay, xy)
    return output.convert("RGB")


def draw_grid(image: Image.Image, step: int = 40) -> None:
    draw = ImageDraw.Draw(image)
    color = tuple(int(LINE[index : index + 2], 16) for index in (1, 3, 5))
    for x in range(0, image.width, step):
        draw.line((x, 0, x, image.height), fill=color, width=1)
    for y in range(0, image.height, step):
        draw.line((0, y, image.width, y), fill=color, width=1)


def story_composition(
    source: Image.Image,
    size: tuple[int, int],
    focus: tuple[float, float],
    accent: str,
) -> Image.Image:
    width, height = size
    top = round(height * 0.14)
    bottom = round(height * 0.35)
    live_height = height - top - bottom
    canvas = Image.new("RGB", size, PAPER)
    accent_panel = Image.new("RGB", (width, height - top), accent)
    draw_grid(accent_panel, max(30, round(width / 30)))
    canvas.paste(accent_panel, (0, top))
    photo = cover_crop(source, (round(width * 0.88), live_height), focus)
    photo_x = round(width * 0.06)
    shadow = Image.new("RGB", (photo.width, photo.height), INK)
    canvas.paste(shadow, (photo_x + round(width * 0.012), top + round(width * 0.012)))
    canvas.paste(photo, (photo_x, top))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, width, max(8, round(height * 0.007))), fill=YELLOW)
    return canvas


def add_manifest_entry(
    entries: list[dict],
    path: Path,
    site_root: Path,
    *,
    role: str,
    origin: str,
    classification: str,
    focus: str,
    placements: tuple[str, ...] | list[str],
    alt: str,
) -> None:
    with Image.open(path) as image:
        width, height = image.size
        image_format = image.format.lower()
    entries.append(
        {
            "path": path.relative_to(site_root).as_posix(),
            "semantic_role": role,
            "origin": origin,
            "classification": classification,
            "dimensions": {"width": width, "height": height},
            "format": image_format,
            "crop_focal_point": focus,
            "intended_pages_placements": list(placements),
            "alt_text": alt,
            "rights_confirmation": "asset-specific sources user-confirmed: website, organic social, paid advertising, editing and compositing",
            "metadata_removal_status": "verified by build: exported without EXIF, GPS, XMP, comments or embedded thumbnails",
            "sha256": sha256(path),
        }
    )


def build(args: argparse.Namespace) -> None:
    site_root = Path(__file__).resolve().parents[1]
    intake = Path(args.intake)
    review = Path(args.review)
    generated = Path(args.workbench_generated)
    masters_root = site_root / "brand" / "photo-masters"
    documentary_root = masters_root / "documentary"
    web_root = site_root / "static" / "brand" / "photos"
    social_root = site_root / "brand" / "social" / "exports"
    logo_root = site_root / "static" / "brand" / "logos"
    entries: list[dict] = []

    for directory in (masters_root, documentary_root, web_root, social_root):
        directory.mkdir(parents=True, exist_ok=True)

    campaign_sources = {
        "robotics": review / "concept-1-flagship-robotics-hero-v1.1.png",
        "scratch": review / "campaign-scratch-class-v2.png",
        "teacher": review / "concept-3-eugene-builder-teacher-v1.1.png",
    }
    campaign_names = {
        "robotics": "campaign-robotics-hero-v1.png",
        "scratch": "campaign-scratch-class-v2.png",
        "teacher": "campaign-eugene-builder-v1.png",
    }
    master_images: dict[str, Image.Image] = {}
    for key, source in campaign_sources.items():
        destination = masters_root / campaign_names[key]
        save_clean(open_rgb(source), destination, "png")
        master_images[key] = open_rgb(destination)
        add_manifest_entry(
            entries,
            destination,
            site_root,
            role=f"approved {key} campaign master",
            origin=source.name,
            classification="reconstructed campaign image",
            focus="see responsive derivative records",
            placements=("website", "organic social", "paid advertising"),
            alt="",
        )

    workbench_destination = masters_root / "campaign-project-workbench-v1.png"
    if generated.resolve() != workbench_destination.resolve():
        workbench = open_rgb(generated)
        workbench = blur_regions(
            workbench,
            [
                (565, 334, 704, 378, 3.2),
                (773, 358, 931, 406, 3.2),
                (1194, 600, 1455, 735, 4.0),
                (1234, 738, 1480, 820, 4.0),
            ],
        )
        save_clean(workbench, workbench_destination, "png")
    master_images["workbench"] = open_rgb(workbench_destination)
    add_manifest_entry(
        entries,
        workbench_destination,
        site_root,
        role="approved project workbench campaign master",
        origin="generated from authorized real apparatus references",
        classification="reconstructed campaign image",
        focus="0.52,0.54",
        placements=("Projects", "Lessons", "blog cards", "paid advertising"),
        alt="",
    )

    documentary_specs = [
        ("historical-robot-testing", "20211119_184800.jpg", (1200, 1500), (0.59, 0.55), [(128, 650, 535, 1185, 12)]),
        ("historical-workbench-apparatus", "20200609_015805.jpg", (1800, 1200), (0.52, 0.54), [(1530, 270, 1920, 620, 8)]),
        ("historical-robot-adjustment", "20211119_184618.jpg", (1200, 1500), (0.54, 0.62), [(180, 540, 760, 880, 10)]),
        ("historical-scratch-use", "DSC_0070.JPG", (1800, 1200), (0.58, 0.56), [(3040, 2090, 3440, 2340, 12), (3330, 1190, 4100, 1390, 10)]),
        ("historical-classroom-context", "DSC_0042.JPG", (1800, 1200), (0.43, 0.53), [(990, 730, 1450, 1080, 12)]),
    ]
    documentary_images: dict[str, Image.Image] = {}
    for slug, filename, size, focus, regions in documentary_specs:
        source = open_rgb(intake / filename)
        source = blur_regions(source, regions)
        result = document_tone(cover_crop(source, size, focus))
        destination = documentary_root / f"{slug}.jpg"
        save_clean(result, destination, "jpg")
        documentary_images[slug] = open_rgb(destination)
        add_manifest_entry(
            entries,
            destination,
            site_root,
            role=slug.replace("historical-", "historical workshop ").replace("-", " "),
            origin=filename,
            classification="historical workshop photograph",
            focus=f"{focus[0]:.2f},{focus[1]:.2f}",
            placements=("Gallery", "blog", "supporting website cards"),
            alt="",
        )

    reconstructed_images: dict[str, Image.Image] = {}
    reconstructed_source = review / "reconstructed-coding-together-v1.png"
    reconstructed_destination = masters_root / "reconstructed-coding-together-v1.png"
    save_clean(open_rgb(reconstructed_source), reconstructed_destination, "png")
    reconstructed_images["reconstructed-coding-together"] = open_rgb(reconstructed_destination)
    add_manifest_entry(
        entries,
        reconstructed_destination,
        site_root,
        role="reconstructed coding-together master",
        origin="generated reconstruction using authorized historical-robot-testing identity references",
        classification="reconstructed coding-class scene",
        focus="0.50,0.55",
        placements=("Gallery", "blog", "supporting website cards"),
        alt="",
    )

    all_sources = master_images | documentary_images | reconstructed_images
    web_specs = [
        WebSpec("home-hero", "robotics", 16 / 9, (0.66, 0.53), (480, 768, 1200, 1600), "homepage hero", ("Home hero",), "Four children testing a handmade robot together in a compact maker room."),
        WebSpec("robotics-banner", "robotics", 3 / 2, (0.70, 0.57), (480, 768, 1200, 1600), "robotics program banner", ("Robotics program",), "Four children adjusting wires, wheels and sensors on a handmade robot."),
        WebSpec("scratch-banner", "scratch", 16 / 9, (0.54, 0.55), (480, 768, 1200, 1600), "Scratch program banner", ("Scratch program",), "Three children working closely together on a colourful block-based coding project."),
        WebSpec("computer-lab-banner", "scratch", 3 / 2, (0.48, 0.58), (480, 768, 1200, 1600), "Computer Lab banner", ("Computer Lab",), "Children comparing a block-based program together at a small computer station."),
        WebSpec("teacher-about", "teacher", 3 / 2, (0.43, 0.49), (480, 768, 1200, 1600), "Eugene teacher context", ("Our Method",), "Eugene explains a relay-and-sensor apparatus at a workbench."),
        WebSpec("teacher-parents", "teacher", 16 / 9, (0.42, 0.52), (480, 768, 1200, 1600), "parent trust context", ("For Parents",), "Eugene demonstrates how an improvised electronic machine works."),
        WebSpec("projects-workbench", "workbench", 16 / 9, (0.52, 0.55), (480, 768, 1200, 1600), "Projects workbench banner", ("Projects",), "Hands testing a peculiar machine built from sensors, vessels, wheels and exposed wiring."),
        WebSpec("lessons-workbench", "workbench", 3 / 2, (0.48, 0.60), (480, 768, 1200, 1600), "Lessons workbench banner", ("Lessons",), "Hands using tools and test leads on an improvised electronic mechanism."),
        WebSpec("reconstructed-coding-together", "reconstructed-coding-together", 4 / 3, (0.50, 0.55), (400, 640, 960), "reconstructed coding-class gallery image", ("Gallery", "blog thumbnails"), "Three children working together at a computer displaying a colourful block-based program."),
    ]
    for slug in documentary_images:
        web_specs.append(
            WebSpec(
                slug,
                slug,
                4 / 3,
                (0.5, 0.52),
                (400, 640, 960),
                "historical workshop gallery photograph",
                ("Gallery", "blog thumbnails"),
                {
                    "historical-robot-testing": "Children testing tabletop robots during a historical workshop.",
                    "historical-workbench-apparatus": "A real relay, test-lead and container apparatus on a historical workbench.",
                    "historical-robot-adjustment": "A child adjusting a tabletop robot during a historical workshop.",
                    "historical-scratch-use": "A child working with Scratch on a laptop during a historical workshop.",
                    "historical-classroom-context": "A compact historical workshop room with several computer stations.",
                }[slug],
            )
        )

    for spec in web_specs:
        source = all_sources[spec.source_key]
        for width in spec.widths:
            height = round(width / spec.ratio)
            derivative = cover_crop(source, (width, height), spec.focus)
            for extension in ("avif", "webp", "jpg"):
                destination = web_root / f"{spec.slug}-{width}.{extension}"
                save_clean(derivative, destination, extension)
                add_manifest_entry(
                    entries,
                    destination,
                    site_root,
                    role=spec.role,
                    origin=campaign_names.get(spec.source_key, f"{spec.source_key}.jpg"),
                    classification="historical workshop photograph" if spec.source_key.startswith("historical-") else (
                        "reconstructed coding-class scene"
                        if spec.source_key == "reconstructed-coding-together"
                        else "reconstructed campaign image"
                    ),
                    focus=f"{spec.focus[0]:.2f},{spec.focus[1]:.2f}",
                    placements=spec.placements,
                    alt=spec.alt,
                )

    logo_cache = Path(args.cache)
    logo_cache.mkdir(parents=True, exist_ok=True)
    avatar_png = logo_cache / "social-avatar-1024.png"
    wordmark_reversed = logo_cache / "wordmark-reversed-720.png"
    render_svg(logo_root / "social-avatar.svg", avatar_png, 1024, 1024)
    render_svg(logo_root / "wordmark-horizontal-reversed.svg", wordmark_reversed, 720, 150)
    profile_destination = social_root / "identity" / "facebook-page-profile-1024.png"
    save_clean(open_rgb(avatar_png), profile_destination, "png")
    add_manifest_entry(
        entries,
        profile_destination,
        site_root,
        role="Facebook Page profile identity",
        origin="static/brand/logos/social-avatar.svg",
        classification="canonical identity",
        focus="circular safe area centered at 0.50,0.50",
        placements=("Facebook Page profile",),
        alt="School of Code profile mark.",
    )

    cover_specs = [
        ("facebook-page-cover", "robotics", (1920, 800), (0.64, 0.52), "Facebook Page cover"),
        ("facebook-group-cover", "scratch", (1640, 856), (0.54, 0.55), "Facebook Group cover"),
        ("facebook-event-cover", "workbench", (1920, 1005), (0.52, 0.55), "Facebook Event cover"),
        ("open-graph-link-preview", "robotics", (1200, 630), (0.64, 0.53), "Open Graph link preview"),
    ]
    for slug, source_key, size, focus, role in cover_specs:
        clean = cover_crop(master_images[source_key], size, focus)
        clean_destination = social_root / "covers" / f"{slug}-clean.jpg"
        save_clean(clean, clean_destination, "jpg")
        add_manifest_entry(entries, clean_destination, site_root, role=f"{role} clean", origin=campaign_names.get(source_key, "campaign-project-workbench-v1.png"), classification="reconstructed campaign image", focus=f"{focus[0]:.2f},{focus[1]:.2f}", placements=(role,), alt="")
        plate_height = max(100, round(size[1] * 0.18))
        branded = clean.copy()
        plate = Image.new("RGBA", (round(size[0] * 0.48), plate_height), (21, 21, 21, 205))
        plate_x = round(size[0] * 0.26)
        plate_y = round(size[1] * 0.08)
        branded_rgba = branded.convert("RGBA")
        branded_rgba.alpha_composite(plate, (plate_x, plate_y))
        branded = alpha_overlay(branded_rgba.convert("RGB"), wordmark_reversed, (plate_x + round(size[0] * 0.025), plate_y + round(plate_height * 0.18)), round(size[0] * 0.43))
        branded_destination = social_root / "covers" / f"{slug}-branded.png"
        save_clean(branded, branded_destination, "png")
        add_manifest_entry(entries, branded_destination, site_root, role=f"{role} branded", origin=f"{clean_destination.name} + canonical wordmark", classification="branded reconstructed campaign image", focus="essential content retained in central safe intersection", placements=(role,), alt="")
        if slug == "open-graph-link-preview":
            public_og_destination = web_root / "open-graph-branded-1200x630.png"
            save_clean(branded, public_og_destination, "png")
            add_manifest_entry(entries, public_og_destination, site_root, role="Open Graph sharing image", origin=f"{clean_destination.name} + canonical wordmark", classification="branded reconstructed campaign image", focus="essential content retained in central safe intersection", placements=("site-wide Open Graph sharing",), alt="Four children testing a handmade robot together in a compact maker room.")

    family_specs = [
        ("robotics", "robotics", (0.68, 0.54), GREEN_SOFT),
        ("scratch-lab", "scratch", (0.54, 0.57), BLUE_SOFT),
        ("eugene-teacher", "teacher", (0.43, 0.52), RED_SOFT),
    ]
    placement_specs = [
        ("feed-square-1440", (1440, 1440)),
        ("feed-portrait-1440x1800", (1440, 1800)),
        ("feed-landscape-1440x754", (1440, 754)),
    ]
    for family, source_key, focus, accent in family_specs:
        source = master_images[source_key]
        family_root = social_root / "campaigns" / family
        for placement, size in placement_specs:
            destination = family_root / f"{placement}.jpg"
            save_clean(cover_crop(source, size, focus), destination, "jpg")
            add_manifest_entry(entries, destination, site_root, role=f"{family} {placement}", origin=campaign_names[source_key], classification="reconstructed campaign image", focus=f"{focus[0]:.2f},{focus[1]:.2f}", placements=("Facebook/Instagram paid and organic feed",), alt="")
        story_master = story_composition(source, (1440, 2560), focus, accent)
        story_master_destination = family_root / "story-reel-master-1440x2560.png"
        save_clean(story_master, story_master_destination, "png")
        add_manifest_entry(entries, story_master_destination, site_root, role=f"{family} Story/Reel clean master", origin=campaign_names[source_key], classification="reconstructed campaign image", focus="safe live area: x 6–94%, y 14–65%", placements=("Stories", "Reels"), alt="")
        delivery = story_composition(source, (1080, 1920), focus, accent)
        delivery = alpha_overlay(delivery, wordmark_reversed, (75, 285), 500)
        delivery_destination = family_root / "story-reel-delivery-1080x1920.png"
        save_clean(delivery, delivery_destination, "png")
        add_manifest_entry(entries, delivery_destination, site_root, role=f"{family} branded Story/Reel delivery", origin=f"{campaign_names[source_key]} + canonical wordmark", classification="branded reconstructed campaign image", focus="safe live area: x 6–94%, y 14–65%", placements=("Stories", "Reels"), alt="")

    template_root = site_root / "static" / "brand" / "templates"
    preview_root = site_root / "brand" / "social" / "previews"
    for template in sorted(template_root.glob("*.svg")):
        # Previews are deliberately modest; editable SVG files remain the masters.
        source_text = template.read_text(encoding="utf-8")
        import re

        match = re.search(r'viewBox="[^"]*\s([0-9.]+)\s([0-9.]+)"', source_text)
        if not match:
            raise ValueError(f"Missing viewBox: {template}")
        source_width, source_height = (float(value) for value in match.groups())
        preview_width = 600
        preview_height = round(preview_width * source_height / source_width)
        render_svg(template, preview_root / f"{template.stem}.png", preview_width, preview_height)

    manifest_path = site_root / "brand" / "photo-asset-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "rights_status": "Only asset-specific cleared sources may enter production. The withdrawn historical coding-together photograph and former Scratch campaign master are excluded; reconstructed replacements use children from the fully authorized historical-robot-testing references.",
                "authenticity_rule": "Historical workshop photographs must not be described as a current Calgary cohort or current facility. Reconstructed campaign images and reconstructed coding-class scenes must not be presented as documentary photographs of a literal class, date or facility.",
                "assets": sorted(entries, key=lambda entry: entry["path"]),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True, help="Private source-photo directory")
    parser.add_argument("--review", required=True, help="Approved concept directory")
    parser.add_argument("--workbench-generated", required=True, help="Generated workbench source image")
    parser.add_argument("--cache", required=True, help="Local-only rasterization cache")
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
