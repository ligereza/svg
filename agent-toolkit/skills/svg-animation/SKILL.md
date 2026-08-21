# SVG animation skill

## Use when

The request mentions animated SVG, logo animation, morphing, particles,
transitions, pulse, floating, rotation or interactive SVG.

## Tool routing

1. Use `svg.create` if no source SVG exists.
2. Use `svg.embed-image` if the raster image should remain an image.
3. Use `svg.vectorize` when true vector paths are required.
4. Use `svg.animate` for a standard transform/opacity animation.
5. Use `svg.particles` for deterministic particle scenes.
6. Run `svg.validate` before delivery.
7. Run `svg.preview` and return the HTML preview path.

## Do not assume

Vectorizing a raster image is different from embedding it. The MVP vectorizer
uses deterministic pixel-run paths and is best for icons, logos and stylized
assets; use a dedicated contour tracer later for photographic images.
