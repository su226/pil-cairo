def a1_swap(
    data: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_rgb_to_cairo_rgb16(
    data: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_rgb_to_cairo_rgb30(
    data: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_i_to_cairo_rgb30(
    r: bytes,
    g: bytes,
    b: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_rgb_to_cairo_rgb96f(
    data: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_f_to_cairo_rgb96f(
    r: bytes,
    g: bytes,
    b: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_rgba_to_cairo_rgba128f(
    data: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def pil_f_to_cairo_rgba128f(
    r: bytes,
    g: bytes,
    b: bytes,
    a: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def cairo_rgb30_to_pil_bgrx(
    data: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def cairo_rgb96f_to_pil_rgb(
    data: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def cairo_rgba128f_to_pil_rgba(
    data: bytes,
    out: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def cairo_rgb30_to_pil_i(
    data: bytes,
    r: bytearray,
    g: bytearray,
    b: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def cairo_rgb96f_to_pil_f(
    data: bytes,
    r: bytearray,
    g: bytearray,
    b: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
def cairo_rgba128f_to_pil_f(
    data: bytes,
    r: bytearray,
    g: bytearray,
    b: bytearray,
    a: bytearray,
    w: int,
    h: int,
    stride: int,
) -> None: ...
