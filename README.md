# pil-cairo

Fast conversion between Pillow `Image` and PyCairo `ImageSurface` powered by Rust.

This library won't perform dithering when downsampling, e.g. "RGB" --> RGB16_565. (PyCairo won't perform dithering when using RGB16_565 format either.)

## API documentation

### `def to_cairo(im: Image.Image) -> cairo.ImageSurface: ...`

Converting a Pillow `Image` to a PyCairo `ImageSurface` follows these rules:

```plaintext
"1" --> cairo.Format.A1
"L" --> cairo.Format.A8
"RGB" --> cairo.Format.RGB24
"RGBA" --> cairo.Format.ARGB32
```

### `def to_cairo_rgb16(im: Image.Image) -> cairo.ImageSurface: ...`

Convert a Pillow `Image` in "RGB" mode to a PyCairo `ImageSurface` in RGB16_565 format.

### `def to_cairo_rgb30(im: Image.Image | RGB30) -> cairo.ImageSurface: ...`

Convert a Pillow `Image` in "RGB" mode or three Pillow `Image`s in "I" mode within a tuple to a PyCairo `ImageSurface` in RGB30 format.

### `def to_cairo_rgb96f(im: Image.Image | RGB96F) -> cairo.ImageSurface: ...`

Convert a Pillow `Image` in "RGB" mode or three Pillow `Image`s in "F" mode within a tuple to a PyCairo `ImageSurface` in RGB96F format.

### `def to_cairo_rgba128f(im: Image.Image | RGBA128F) -> cairo.ImageSurface: ...`

Convert a Pillow `Image` in "RGBA" mode or four Pillow `Image`s in "F" mode within a tuple to a PyCairo `ImageSurface` in RGBA128F format.

### `def to_pil(surface: cairo.ImageSurface) -> Image.Image: ...`

Converting a PyCairo `ImageSurface` to a Pillow `Image` follows these rules:

```plaintext
cairo.Format.A1 --> "1"
cairo.Format.A8 --> "L"
cairo.Format.RGB24 --> "RGB"
cairo.Format.ARGB32 --> "RGBA"
cairo.Format.RGB16_565 --> "RGB"
cairo.Format.RGB30 --> "RGB" (Lossy)
cairo.Format.RGB96F --> "RGB" (Lossy)
cairo.Format.RGBA128F --> "RGB" (Lossy)
```

### `def to_pil_rgb30(surface: cairo.ImageSurface) -> RGB30: ...`

Convert a PyCairo `ImageSurface` in RGB30 format to three Pillow `Image`s in "I" mode within a tuple.

### `def to_pil_rgb96f(surface: cairo.ImageSurface) -> RGB96F: ...`

Convert a PyCairo `ImageSurface` in RGB96F format to three Pillow `Image`s in "F" mode within a tuple.

### `def to_pil_rgba128f(surface: cairo.ImageSurface) -> RGBA128F: ...`

Convert a PyCairo `ImageSurface` in RGBA128F format to four Pillow `Image`s in F mode within a tuple.
