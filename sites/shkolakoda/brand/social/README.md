# School of Code social production package

The upload-ready files in `exports/` are sRGB, metadata-clean derivatives. The editable canonical templates remain in `static/brand/templates/`; this directory does not introduce a second visual system.

## Selection

- Robotics family: group energy, handmade machines, wires and tools.
- Scratch/Lab family: close collaboration around a real block-based project.
- Eugene/Teacher family: identity-approved builder-teacher context and parent trust.
- Page cover: Robotics. Group cover: Scratch/Lab. Event cover: project workbench.
- Profile: the canonical `</>` mark rendered from `static/brand/logos/social-avatar.svg`.

Clean cover files contain only the photograph. Branded cover and Story delivery files use the canonical repository wordmark. No generated or approximated logo is permitted.

## Dimensions

| Placement | Production size |
| --- | ---: |
| Page profile | 1024 × 1024 PNG |
| Page cover | 1920 × 800 |
| Group cover | 1640 × 856 |
| Event cover | 1920 × 1005 |
| Open Graph | 1200 × 630 |
| Feed square | 1440 × 1440 |
| Feed portrait | 1440 × 1800 |
| Feed landscape | 1440 × 754 |
| Story/Reel master | 1440 × 2560 |
| Story/Reel delivery | 1080 × 1920 |

## Story and Reel safe area

Checked 2026-08-17 against official Meta guidance:

- Meta recommends fullscreen 9:16 Reels with key creative elements inside the safe zone: <https://www.facebook.com/business/ads/facebook-instagram-reels-ads>
- Meta's Story CTA guidance says to leave roughly 14% at the top and 20% at the bottom free of key elements: <https://www.facebook.com/help/instagram/192168966243613>

This package deliberately uses the more conservative approved production zone:

- 6% clear on each side;
- 14% clear at the top;
- 35% clear at the bottom.

For 1080 × 1920 that means the essential live region is `x=65–1015`, `y=269–1248`. Faces, the canonical logo and editable headline areas must stay within it. The larger bottom reserve anticipates platform controls, captions, CTA treatments and account UI. The guide group in `social-story-1080x1920.svg` is editor-only and must be removed with `brand/export_story.py` before delivery.

## Editable templates

- `photo-plus-caption.svg`: photo announcement and permission-safe historical workshop caption.
- `project-illustration-frame.svg`: project spotlight.
- `social-card-1200x630.svg`: blog/link card and Open Graph composition.
- `social-event-1920x1005.svg`: event announcement.
- `social-post-1080-square.svg`: square post.
- `social-post-1080x1350.svg`: 4:5 feed post.
- `social-story-1080x1920.svg`: Story/Reel with conservative live-area guide.
- `social-bilingual-1080x1350.svg`: separate editable English and Russian copy groups.

All copy remains editable text. Do not outline it unless a printer or platform explicitly requires it. Photographic masters remain text-free; delivery templates may add confirmed copy, the canonical logo and `shkolakoda.com`.

## Export checklist

1. Choose a campaign image or a truthfully captioned historical workshop photograph.
2. Keep current-cohort and facility claims out of historical captions.
3. Replace editable text without changing its meaning between English and Russian.
4. Remove editor-only guides.
5. Export sRGB at the exact placement dimensions.
6. Remove EXIF, GPS, XMP, comments and thumbnails.
7. Inspect circle crops, cover intersections and Story controls in the destination platform preview before publishing.

The reproducible raster pipeline is `../build_photo_assets.py`; install its isolated production dependencies from `../requirements-assets.txt`. These packages are not application runtime dependencies.
