from io import BytesIO

import cairo
import numpy as np
from PIL import Image, ImageDraw

from pil_cairo import (
    to_cairo,
    to_cairo_rgb16,
    to_cairo_rgb30,
    to_cairo_rgb96f,
    to_cairo_rgba128f,
    to_pil,
    to_pil_rgb30,
    to_pil_rgb96f,
    to_pil_rgba128f,
)


def image_same(im1: Image.Image, im2: Image.Image, threshold: int = 0) -> bool:
    if im1.size != im2.size or im1.mode != im2.mode:
        return False
    arr1 = np.asarray(im1).astype(np.int8)
    arr2 = np.asarray(im2).astype(np.int8)
    return (abs(arr1 - arr2) <= threshold).all().item()


def i_to_l(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, np.uint32).astype(np.uint64)
    arr = arr * 0xFF / 0xFFFFFFFF
    return Image.fromarray(arr.astype(np.uint8))


def l_to_i(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, np.uint8).astype(np.uint64)
    arr = arr * 0xFFFFFFFF / 0xFF
    return Image.fromarray(arr.astype(np.uint32))


def f_to_l(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, np.float32)
    arr = arr * 0xFF
    return Image.fromarray(arr.astype(np.uint8))


def l_to_f(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, np.uint8).astype(np.float32)
    arr = arr / 0xFF
    return Image.fromarray(arr)


SIZES = [1, 32, 99]
# Due to some reason (premultiplied alpha, rounding, etc.), there may be tiny difference.
THRESHOLD = 1
# Formats without alpha and rounding.
A1_A8_RGB24_THRESHOLD = 0
# max(abs(x - x * 31 // 255 * 255 // 31) for x in range(256))
RGB_TO_RGB16_THRESHOLD = 9


def test_to_cairo__1() -> None:
    for size in SIZES:
        im = Image.new("1", (size, size))
        draw = ImageDraw.Draw(im)
        draw.line((0, 0, size, size), 1)
        surface = to_cairo(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im.convert("L"), im2, A1_A8_RGB24_THRESHOLD), size


def test_to_cairo__l() -> None:
    l = Image.linear_gradient("L")
    for size in SIZES:
        im = l.resize((size, size))
        surface = to_cairo(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, A1_A8_RGB24_THRESHOLD), size


def test_to_cairo__rgb() -> None:
    r = Image.linear_gradient("L")
    g = Image.new("L", (256, 256))
    b = Image.radial_gradient("L")
    rgb = Image.merge("RGB", (r, g, b))
    for size in SIZES:
        im = rgb.resize((size, size))
        surface = to_cairo(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, A1_A8_RGB24_THRESHOLD), size


def test_to_cairo__rgba() -> None:
    r = Image.linear_gradient("L")
    g = Image.new("L", (256, 256))
    b = Image.radial_gradient("L")
    a = Image.linear_gradient("L")
    rgba = Image.merge("RGBA", (r, g, b, a))
    for size in SIZES:
        im = rgba.resize((size, size))
        surface = to_cairo(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_cairo_rgb16() -> None:
    r = Image.linear_gradient("L")
    g = Image.new("L", (256, 256))
    b = Image.radial_gradient("L")
    rgb = Image.merge("RGB", (r, g, b))
    for size in SIZES:
        im = rgb.resize((size, size))
        surface = to_cairo_rgb16(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, RGB_TO_RGB16_THRESHOLD), size


def test_to_cairo_rgb30__rgb() -> None:
    r = Image.linear_gradient("L")
    g = Image.new("L", (256, 256))
    b = Image.radial_gradient("L")
    rgb = Image.merge("RGB", (r, g, b))
    for size in SIZES:
        im = rgb.resize((size, size))
        surface = to_cairo_rgb30(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_cairo_rgb30__i() -> None:
    r = l_to_i(Image.linear_gradient("L"))
    g = Image.new("I", (256, 256))
    b = l_to_i(Image.radial_gradient("L"))
    for size in range(1, 128):
        im1 = r.resize((size, size))
        im2 = g.resize((size, size))
        im3 = b.resize((size, size))
        surface = to_cairo_rgb30((im1, im2, im3))
        f = BytesIO()
        surface.write_to_png(f)
        im = Image.merge("RGB", (i_to_l(im1), i_to_l(im2), i_to_l(im3)))
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_cairo_rgb96f__rgb() -> None:
    r = Image.linear_gradient("L")
    g = Image.new("L", (256, 256))
    b = Image.radial_gradient("L")
    rgb = Image.merge("RGB", (r, g, b))
    for size in SIZES:
        im = rgb.resize((size, size))
        surface = to_cairo_rgb96f(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_cairo_rgb96f__f() -> None:
    r = l_to_f(Image.linear_gradient("L"))
    g = Image.new("F", (256, 256))
    b = l_to_f(Image.radial_gradient("L"))
    for size in SIZES:
        im1 = r.resize((size, size))
        im2 = g.resize((size, size))
        im3 = b.resize((size, size))
        surface = to_cairo_rgb96f((im1, im2, im3))
        f = BytesIO()
        surface.write_to_png(f)
        im = Image.merge("RGB", (f_to_l(im1), f_to_l(im2), f_to_l(im3)))
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_cairo_rgba128f__rgba() -> None:
    r = Image.linear_gradient("L")
    g = Image.new("L", (256, 256))
    b = Image.radial_gradient("L")
    a = Image.linear_gradient("L")
    rgb = Image.merge("RGBA", (r, g, b, a))
    for size in SIZES:
        im = rgb.resize((size, size))
        surface = to_cairo_rgba128f(im)
        f = BytesIO()
        surface.write_to_png(f)
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_cairo_rgba128f__f() -> None:
    r = l_to_f(Image.linear_gradient("L"))
    g = Image.new("F", (256, 256))
    b = l_to_f(Image.radial_gradient("L"))
    a = l_to_f(Image.linear_gradient("L"))
    for size in SIZES:
        im1 = r.resize((size, size))
        im2 = g.resize((size, size))
        im3 = b.resize((size, size))
        im4 = a.resize((size, size))
        surface = to_cairo_rgba128f((im1, im2, im3, im4))
        f = BytesIO()
        surface.write_to_png(f)
        im = Image.merge("RGBA", (f_to_l(im1), f_to_l(im2), f_to_l(im3), f_to_l(im4)))
        im2 = Image.open(f)
        assert image_same(im, im2, THRESHOLD), size


def test_to_pil__a1() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.A1, size, size) as surface:
            cr = cairo.Context(surface)
            cr.move_to(0, 0)
            cr.line_to(size, size)
            cr.stroke()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im.convert("L"), im2, A1_A8_RGB24_THRESHOLD), size


def test_to_pil__a8() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.A8, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgba(0, 0, 0, 0, 0)
            gradient.add_color_stop_rgba(1, 0, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, A1_A8_RGB24_THRESHOLD), size


def test_to_pil__rgb24() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGB24, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgb(0, 1, 0, 0)
            gradient.add_color_stop_rgb(1, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, A1_A8_RGB24_THRESHOLD), size


def test_to_pil__argb32() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.ARGB32, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgba(0, 1, 0, 0, 0)
            gradient.add_color_stop_rgba(1, 0, 0, 1, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil__rgb16() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGB16_565, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgb(0, 1, 0, 0)
            gradient.add_color_stop_rgb(1, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil__rgb30() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGB30, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgb(0, 1, 0, 0)
            gradient.add_color_stop_rgb(1, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil__rgb96f() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGB96F, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgb(0, 1, 0, 0)
            gradient.add_color_stop_rgb(1, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil__rgba128f() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGBA128F, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgba(0, 1, 0, 0, 0)
            gradient.add_color_stop_rgba(1, 0, 0, 1, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil(surface)
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil_rgb30() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGB30, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgb(0, 1, 0, 0)
            gradient.add_color_stop_rgb(1, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil_rgb30(surface)
            im = Image.merge("RGB", (i_to_l(im[0]), i_to_l(im[1]), i_to_l(im[2])))
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil_rgb96f() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGB96F, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgb(0, 1, 0, 0)
            gradient.add_color_stop_rgb(1, 0, 0, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil_rgb96f(surface)
            im = Image.merge("RGB", (f_to_l(im[0]), f_to_l(im[1]), f_to_l(im[2])))
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size


def test_to_pil_rgba128f() -> None:
    for size in SIZES:
        with cairo.ImageSurface(cairo.Format.RGBA128F, size, size) as surface:
            cr = cairo.Context(surface)
            gradient = cairo.LinearGradient(0, 0, size, size)
            gradient.add_color_stop_rgba(0, 1, 0, 0, 0)
            gradient.add_color_stop_rgba(1, 0, 0, 1, 1)
            cr.set_source(gradient)
            cr.rectangle(0, 0, size, size)
            cr.fill()
            im = to_pil_rgba128f(surface)
            im = Image.merge(
                "RGBA", (f_to_l(im[0]), f_to_l(im[1]), f_to_l(im[2]), f_to_l(im[3]))
            )
            f = BytesIO()
            surface.write_to_png(f)
            im2 = Image.open(f)
            assert image_same(im, im2, THRESHOLD), size
