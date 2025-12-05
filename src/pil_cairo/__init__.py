import cairo
from PIL import Image

from pil_cairo._core import a1_swap as _a1_swap
from pil_cairo._core import cairo_rgb30_to_pil_bgrx as _cario_rgb30_to_pil_bgrx
from pil_cairo._core import cairo_rgb30_to_pil_i as _cairo_rgb30_to_pil_i
from pil_cairo._core import cairo_rgb96f_to_pil_f as _cairo_rgb96f_to_pil_f
from pil_cairo._core import cairo_rgb96f_to_pil_rgb as _cairo_rgb96f_to_pil_rgb
from pil_cairo._core import cairo_rgba128f_to_pil_f as _cairo_rgba128f_to_pil_f
from pil_cairo._core import cairo_rgba128f_to_pil_rgba as _cairo_rgba128f_to_pil_rgba
from pil_cairo._core import pil_f_to_cairo_rgb96f as _pil_f_to_cairo_rgb96f
from pil_cairo._core import pil_f_to_cairo_rgba128f as _pil_f_to_cairo_rgba128f
from pil_cairo._core import pil_i_to_cairo_rgb30 as _pil_i_to_cairo_rgb30
from pil_cairo._core import pil_rgb_to_cairo_rgb16 as _pil_rgb_to_cairo_rgb16
from pil_cairo._core import pil_rgb_to_cairo_rgb30 as _pil_rgb_to_cairo_rgb30
from pil_cairo._core import pil_rgb_to_cairo_rgb96f as _pil_rgb_to_cairo_rgb96f
from pil_cairo._core import pil_rgba_to_cairo_rgba128f as _pil_rgba_to_cairo_rgba128f

__all__ = [
    "RGB30",
    "RGB96F",
    "RGBA128F",
    "to_cairo",
    "to_cairo_rgb16",
    "to_cairo_rgb30",
    "to_cairo_rgb96f",
    "to_cairo_rgba128f",
    "to_pil",
    "to_pil_rgb30",
    "to_pil_rgb96f",
    "to_pil_rgba128f",
]
RGB30 = tuple[Image.Image, Image.Image, Image.Image]
RGB96F = tuple[Image.Image, Image.Image, Image.Image]
RGBA128F = tuple[Image.Image, Image.Image, Image.Image, Image.Image]


def to_cairo(im: Image.Image) -> cairo.ImageSurface:
    w, h = im.size
    if im.mode == "1":
        stride = cairo.Format.A1.stride_for_width(w)
        data = bytearray(im.tobytes("raw", "1", stride))
        _a1_swap(data, w, h, stride)
        return cairo.ImageSurface.create_for_data(
            data,
            cairo.Format.A1,
            w,
            h,
            stride,
        )
    if im.mode == "L":
        stride = cairo.Format.A8.stride_for_width(w)
        data = bytearray(im.tobytes("raw", "L", stride))
        return cairo.ImageSurface.create_for_data(
            data,
            cairo.Format.A8,
            w,
            h,
            stride,
        )
    if im.mode == "RGB":
        stride = cairo.Format.RGB24.stride_for_width(w)
        data = bytearray(im.tobytes("raw", "BGRX", stride))
        return cairo.ImageSurface.create_for_data(
            data,
            cairo.Format.RGB24,
            w,
            h,
            stride,
        )
    if im.mode == "RGBA":
        stride = cairo.Format.ARGB32.stride_for_width(w)
        data = bytearray(im.tobytes("raw", "BGRa", stride))
        return cairo.ImageSurface.create_for_data(
            data,
            cairo.Format.ARGB32,
            w,
            h,
            stride,
        )
    raise NotImplementedError(f"Unsupported mode: {im.mode}")


def to_cairo_rgb16(im: Image.Image) -> cairo.ImageSurface:
    if im.mode != "RGB":
        raise ValueError("Wrong mode")
    data = im.tobytes()
    w, h = im.size
    stride = cairo.Format.RGB16_565.stride_for_width(w)
    out_data = bytearray(stride * h)
    _pil_rgb_to_cairo_rgb16(data, out_data, w, h, stride)
    return cairo.ImageSurface.create_for_data(
        out_data,
        cairo.Format.RGB16_565,
        w,
        h,
        stride,
    )


def to_cairo_rgb30(im: Image.Image | RGB30) -> cairo.ImageSurface:
    if isinstance(im, Image.Image):
        if im.mode != "RGB":
            raise ValueError("Wrong mode")
        data = im.tobytes()
        w, h = im.size
        stride = cairo.Format.RGB30.stride_for_width(w)
        out_data = bytearray(stride * h)
        _pil_rgb_to_cairo_rgb30(data, out_data, w, h, stride)
        return cairo.ImageSurface.create_for_data(
            out_data,
            cairo.Format.RGB30,
            w,
            h,
            stride,
        )

    im0, im1, im2 = im
    if not (im0.mode == im1.mode == im2.mode == "I"):
        raise ValueError("Wrong mode")
    if not (im0.size == im1.size == im2.size):
        raise ValueError("Size mismatch")
    data0 = im0.tobytes()
    data1 = im1.tobytes()
    data2 = im2.tobytes()
    w, h = im0.size
    stride = cairo.Format.RGB30.stride_for_width(w)
    out_data = bytearray(stride * h)
    _pil_i_to_cairo_rgb30(data0, data1, data2, out_data, w, h, stride)
    return cairo.ImageSurface.create_for_data(out_data, cairo.Format.RGB30, w, h)


def to_cairo_rgb96f(im: Image.Image | RGB96F) -> cairo.ImageSurface:
    if isinstance(im, Image.Image):
        if im.mode != "RGB":
            raise ValueError("Wrong mode")
        data = im.tobytes()
        w, h = im.size
        stride = cairo.Format.RGB96F.stride_for_width(w)
        out_data = bytearray(stride * h)
        _pil_rgb_to_cairo_rgb96f(data, out_data, w, h, stride)
        return cairo.ImageSurface.create_for_data(
            out_data,
            cairo.Format.RGB96F,
            w,
            h,
            stride,
        )

    im0, im1, im2 = im
    if not (im0.mode == im1.mode == im2.mode == "F"):
        raise ValueError("Wrong mode")
    if not (im0.size == im1.size == im2.size):
        raise ValueError("Size mismatch")
    data0 = im0.tobytes()
    data1 = im1.tobytes()
    data2 = im2.tobytes()
    w, h = im0.size
    stride = cairo.Format.RGB96F.stride_for_width(w)
    out_data = bytearray(stride * h)
    _pil_f_to_cairo_rgb96f(data0, data1, data2, out_data, w, h, stride)
    return cairo.ImageSurface.create_for_data(out_data, cairo.Format.RGB96F, w, h)


def to_cairo_rgba128f(im: Image.Image | RGBA128F) -> cairo.ImageSurface:
    if isinstance(im, Image.Image):
        if im.mode != "RGBA":
            raise ValueError("Wrong mode")
        data = im.tobytes()
        w, h = im.size
        stride = cairo.Format.RGBA128F.stride_for_width(w)
        out_data = bytearray(stride * h)
        _pil_rgba_to_cairo_rgba128f(data, out_data, w, h, stride)
        return cairo.ImageSurface.create_for_data(
            out_data,
            cairo.Format.RGBA128F,
            w,
            h,
            stride,
        )

    im0, im1, im2, im3 = im
    if not (im0.mode == im1.mode == im2.mode == im3.mode == "F"):
        raise ValueError("Wrong mode")
    if not (im0.size == im1.size == im2.size == im3.size):
        raise ValueError("Size mismatch")
    data0 = im0.tobytes()
    data1 = im1.tobytes()
    data2 = im2.tobytes()
    data3 = im3.tobytes()
    w, h = im0.size
    stride = cairo.Format.RGBA128F.stride_for_width(w)
    out_data = bytearray(stride * h)
    _pil_f_to_cairo_rgba128f(data0, data1, data2, data3, out_data, w, h, stride)
    return cairo.ImageSurface.create_for_data(out_data, cairo.Format.RGBA128F, w, h)


def to_pil(surface: cairo.ImageSurface) -> Image.Image:
    w = surface.get_width()
    h = surface.get_height()
    data = surface.get_data()
    stride = surface.get_stride()
    surface_format = surface.get_format()
    if surface_format == cairo.Format.A1:
        data = bytearray(data)
        _a1_swap(data, w, h, stride)
        return Image.frombuffer("1", (w, h), data, "raw", "1", stride)
    if surface_format == cairo.Format.A8:
        return Image.frombuffer("L", (w, h), data.tobytes(), "raw", "L", stride, 1)
    if surface_format == cairo.Format.RGB24:
        return Image.frombuffer("RGB", (w, h), data.tobytes(), "raw", "BGRX", stride)
    if surface_format == cairo.Format.ARGB32:
        return Image.frombuffer("RGBA", (w, h), data.tobytes(), "raw", "BGRa", stride)
    if surface_format == cairo.Format.RGB16_565:
        return Image.frombuffer("RGB", (w, h), data.tobytes(), "raw", "BGR;16", stride)
    if surface_format == cairo.Format.RGB30:
        data = bytearray(data.tobytes())
        _cario_rgb30_to_pil_bgrx(data, w, h, stride)
        return Image.frombuffer("RGB", (w, h), data, "raw", "BGRX", stride)
    if surface_format == cairo.Format.RGB96F:
        out_data = bytearray(w * h * 3)
        _cairo_rgb96f_to_pil_rgb(data.tobytes(), out_data, w, h, stride)
        return Image.frombuffer("RGB", (w, h), out_data)
    if surface_format == cairo.Format.RGBA128F:
        out_data = bytearray(w * h * 4)
        _cairo_rgba128f_to_pil_rgba(data.tobytes(), out_data, w, h, stride)
        return Image.frombuffer("RGBA", (w, h), out_data)
    raise NotImplementedError(f"Unsupported format: {surface_format}")


def to_pil_rgb30(surface: cairo.ImageSurface) -> RGB30:
    if surface.get_format() != cairo.Format.RGB30:
        raise ValueError("Wrong format")
    data = surface.get_data().tobytes()
    w = surface.get_width()
    h = surface.get_height()
    stride = surface.get_stride()
    size = w * h * 4
    r = bytearray(size)
    g = bytearray(size)
    b = bytearray(size)
    _cairo_rgb30_to_pil_i(data, r, g, b, w, h, stride)
    r = Image.frombuffer("I", (w, h), r)
    g = Image.frombuffer("I", (w, h), g)
    b = Image.frombuffer("I", (w, h), b)
    return r, g, b


def to_pil_rgb96f(surface: cairo.ImageSurface) -> RGB96F:
    if surface.get_format() != cairo.Format.RGB96F:
        raise ValueError("Wrong format")
    data = surface.get_data().tobytes()
    w = surface.get_width()
    h = surface.get_height()
    stride = surface.get_stride()
    size = w * h * 4
    r = bytearray(size)
    g = bytearray(size)
    b = bytearray(size)
    _cairo_rgb96f_to_pil_f(data, r, g, b, w, h, stride)
    r = Image.frombuffer("F", (w, h), r)
    g = Image.frombuffer("F", (w, h), g)
    b = Image.frombuffer("F", (w, h), b)
    return r, g, b


def to_pil_rgba128f(surface: cairo.ImageSurface) -> RGBA128F:
    if surface.get_format() != cairo.Format.RGBA128F:
        raise ValueError("Wrong format")
    data = surface.get_data().tobytes()
    w = surface.get_width()
    h = surface.get_height()
    stride = surface.get_stride()
    size = w * h * 4
    r = bytearray(size)
    g = bytearray(size)
    b = bytearray(size)
    a = bytearray(size)
    _cairo_rgba128f_to_pil_f(data, r, g, b, a, w, h, stride)
    r = Image.frombuffer("F", (w, h), r)
    g = Image.frombuffer("F", (w, h), g)
    b = Image.frombuffer("F", (w, h), b)
    a = Image.frombuffer("F", (w, h), a)
    return r, g, b, a
