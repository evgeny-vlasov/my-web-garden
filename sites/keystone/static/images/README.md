# Image Assets for Keystone Hardscapes

This directory contains all image assets for the Keystone Hardscapes website.

## Required Images

### Homepage Images
- `hero.jpg` - Hero section background (1920x1080px min)
- `andrew-portrait.jpg` - Andrew's portrait photo (600x800px)
- `service-hardscape.jpg` - Hardscape service card image (800x600px)
- `service-snow.jpg` - Snow removal service card image (800x600px)
- `service-concrete.jpg` - Concrete restoration service card image (800x600px)
- `project-1.jpg` - Portfolio preview #1 (800x600px)
- `project-2.jpg` - Portfolio preview #2 (800x600px)
- `project-3.jpg` - Portfolio preview #3 (800x600px)
- `project-4.jpg` - Portfolio preview #4 (800x600px)
- `service-area-map.jpg` - Calgary area service map (1000x800px)

### About Page Images
- `andrew-at-work.jpg` - Andrew working on a project (1000x750px)
- `alberta-winter-hardscape.jpg` - Hardscape in Alberta winter (1000x750px)

### Hardscape Service Page
- `service-hardscape-hero.jpg` - Hero background (1920x1080px)
- `hardscape-detail.jpg` - Close-up craftsmanship shot (1000x750px)
- `winter-patio.jpg` - Patio in winter conditions (1000x750px)

### Snow Removal Service Page
- `service-snow-hero.jpg` - Hero background (1920x1080px)
- `snow-removal-action.jpg` - Snow removal in progress (1000x750px)
- `snow-equipment.jpg` - Professional equipment (1000x750px)

### Concrete Restoration Service Page
- `service-concrete-hero.jpg` - Hero background (1920x1080px)
- `concrete-before-after.jpg` - Before/after comparison (1000x750px)
- `concrete-assessment.jpg` - Assessment process (1000x750px)

### Portfolio Page Images
Create a `portfolio/` subdirectory with:
- `patio-calgary-1.jpg` - Backyard patio project (800x600px)
- `retaining-wall-airdrie.jpg` - Retaining wall project (800x600px)
- `outdoor-kitchen-cochrane.jpg` - Outdoor living space (800x600px)
- `driveway-okotoks.jpg` - Driveway restoration (800x600px)
- `front-walkway-calgary.jpg` - Front walkway project (800x600px)
- `garage-floor-chestermere.jpg` - Garage floor coating (800x600px)
- `backyard-transformation-calgary.jpg` - Full backyard transformation (800x600px)
- `commercial-parking-airdrie.jpg` - Commercial project (800x600px)
- `patio-extension-calgary.jpg` - Patio extension (800x600px)

## Image Guidelines

### Technical Specifications
- **Format:** JPG for photos
- **Compression:** 80-90% quality (optimize for web)
- **Max file size:** 500KB per image
- **Color space:** sRGB

### Content Guidelines
- Professional quality photos only
- Show completed work, not in-progress (unless specified)
- Calgary/Alberta climate visible where relevant
- No visible branding from competitors
- Client permission obtained for all project photos

### Photography Tips
- Natural lighting preferred
- Show scale (include furniture, people where appropriate)
- Multiple angles for portfolio projects
- Before/after shots for restoration work
- Seasonal variety (summer and winter conditions)

## Placeholder Images

Until real photos are available, you can use:
- Stock photos from Unsplash, Pexels (commercial use allowed)
- Placeholder services like placehold.co
- Watermarked "Placeholder" images

## Naming Convention

- Use lowercase
- Use hyphens (not underscores or spaces)
- Be descriptive: `retaining-wall-airdrie.jpg` not `img001.jpg`
- Include location in portfolio images

## Image Optimization

Before uploading, optimize all images:

```bash
# Using ImageMagick
mogrify -resize 1920x1080^ -gravity center -extent 1920x1080 -quality 85 hero.jpg

# Using online tools
# - TinyPNG (https://tinypng.com)
# - Squoosh (https://squoosh.app)
```

## Directory Structure

```
images/
├── hero.jpg
├── andrew-portrait.jpg
├── andrew-at-work.jpg
├── service-hardscape.jpg
├── service-snow.jpg
├── service-concrete.jpg
├── service-hardscape-hero.jpg
├── service-snow-hero.jpg
├── service-concrete-hero.jpg
├── hardscape-detail.jpg
├── winter-patio.jpg
├── snow-removal-action.jpg
├── snow-equipment.jpg
├── concrete-before-after.jpg
├── concrete-assessment.jpg
├── alberta-winter-hardscape.jpg
├── service-area-map.jpg
├── project-1.jpg
├── project-2.jpg
├── project-3.jpg
├── project-4.jpg
└── portfolio/
    ├── patio-calgary-1.jpg
    ├── retaining-wall-airdrie.jpg
    ├── outdoor-kitchen-cochrane.jpg
    ├── driveway-okotoks.jpg
    ├── front-walkway-calgary.jpg
    ├── garage-floor-chestermere.jpg
    ├── backyard-transformation-calgary.jpg
    ├── commercial-parking-airdrie.jpg
    └── patio-extension-calgary.jpg
```

## Updating Images

When replacing images:
1. Keep the same filename
2. Clear browser cache to see changes
3. Test on mobile and desktop
4. Verify file size is optimized

## Rights & Permissions

- Obtain client permission for all project photos
- Maintain a record of photo permissions
- Include photo credits if required by agreement
- Never use copyrighted images without permission
