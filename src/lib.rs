use pyo3::prelude::*;

#[pymodule]
mod _core {
    use pyo3::{prelude::*, types::PyByteArray};

    // "1" <-> cairo.Format.A1
    #[pyfunction]
    fn a1_swap(data: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let data = unsafe { data.as_bytes_mut() };
        for y in 0..h {
            for x in (0..w).step_by(32) {
                let i = y * stride + x / 8;
                let v = u32::from_ne_bytes([data[i], data[i + 1], data[i + 2], data[i + 3]]);
                let v = ((v & 0xaaaaaaaa) >> 1) | ((v & 0x55555555) << 1);
                let v = ((v & 0xcccccccc) >> 2) | ((v & 0x33333333) << 2);
                let v = ((v & 0xf0f0f0f0) >> 4) | ((v & 0x0f0f0f0f) << 4);
                [data[i], data[i + 1], data[i + 2], data[i + 3]] = v.to_ne_bytes();
            }
        }
    }

    // "RGB" --> cairo.Format.RGB16_565
    #[pyfunction]
    fn pil_rgb_to_cairo_rgb16(data: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 2;
                let r = data[i_in] as u16 * 0x1f / 0xff;
                let g = data[i_in + 1] as u16 * 0x3f / 0xff;
                let b = data[i_in + 2] as u16 * 0x1f / 0xff;
                let v = (r << 11) | (g << 5) | b;
                [out[i_out], out[i_out + 1]] = v.to_ne_bytes();
                i_in += 3;
            }
        }
    }

    // "RGB" --> cairo.Format.RGB30
    #[pyfunction]
    fn pil_rgb_to_cairo_rgb30(data: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 4;
                let r = data[i_in] as u32 * 0x3ff / 0xff;
                let g = data[i_in + 1] as u32 * 0x3ff / 0xff;
                let b = data[i_in + 2] as u32 * 0x3ff / 0xff;
                let v = (r << 20) | (g << 10) | b;
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = v.to_ne_bytes();
                i_in += 3;
            }
        }
    }

    // "I" * 3 --> cairo.Format.RGB30
    #[pyfunction]
    fn pil_i_to_cairo_rgb30(r: &[u8], g: &[u8], b: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out: &mut [u8] = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 4;
                let r_v = u32::from_ne_bytes([r[i_in], r[i_in + 1], r[i_in + 2], r[i_in + 3]]);
                let g_v = u32::from_ne_bytes([g[i_in], g[i_in + 1], g[i_in + 2], g[i_in + 3]]);
                let b_v = u32::from_ne_bytes([b[i_in], b[i_in + 1], b[i_in + 2], b[i_in + 3]]);
                let r_v = r_v as u64 * 0x3ff / 0xffffffff;
                let g_v = g_v as u64 * 0x3ff / 0xffffffff;
                let b_v = b_v as u64 * 0x3ff / 0xffffffff;
                let v = ((r_v as u32) << 20) | ((g_v as u32) << 10) | (b_v as u32);
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = v.to_ne_bytes();
                i_in += 4;
            }
        }
    }

    // "RGB" --> cairo.Format.RGB96F
    #[pyfunction]
    fn pil_rgb_to_cairo_rgb96f(data: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 12;
                let r = data[i_in];
                let g = data[i_in + 1];
                let b = data[i_in + 2];
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = ((r as f32) / 255.0).to_ne_bytes();
                [out[i_out + 4], out[i_out + 5], out[i_out + 6], out[i_out + 7]] = ((g as f32) / 255.0).to_ne_bytes();
                [out[i_out + 8], out[i_out + 9], out[i_out + 10], out[i_out + 11]] = ((b as f32) / 255.0).to_ne_bytes();
                i_in += 3;
            }
        }
    }

    // "F" * 3 --> cairo.Format.RGB96F
    #[pyfunction]
    fn pil_f_to_cairo_rgb96f(r: &[u8], g: &[u8], b: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out: &mut [u8] = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 12;
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = [r[i_in], r[i_in + 1], r[i_in + 2], r[i_in + 3]];
                [out[i_out + 4], out[i_out + 5], out[i_out + 6], out[i_out + 7]] = [g[i_in], g[i_in + 1], g[i_in + 2], g[i_in + 3]];
                [out[i_out + 8], out[i_out + 9], out[i_out + 10], out[i_out + 11]] = [b[i_in], b[i_in + 1], b[i_in + 2], b[i_in + 3]];
                i_in += 4;
            }
        }
    }

    // "RGBA" --> cairo.Format.RGBA128F
    #[pyfunction]
    fn pil_rgba_to_cairo_rgba128f(data: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 16;
                let mut r = (data[i_in] as f32) / 255.0;
                let mut g = (data[i_in + 1] as f32) / 255.0;
                let mut b = (data[i_in + 2] as f32) / 255.0;
                let a = (data[i_in + 3] as f32) / 255.0;
                r *= a;
                g *= a;
                b *= a;
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = r.to_ne_bytes();
                [out[i_out + 4], out[i_out + 5], out[i_out + 6], out[i_out + 7]] = g.to_ne_bytes();
                [out[i_out + 8], out[i_out + 9], out[i_out + 10], out[i_out + 11]] = b.to_ne_bytes();
                [out[i_out + 12], out[i_out + 13], out[i_out + 14], out[i_out + 15]] = a.to_ne_bytes();
                i_in += 4;
            }
        }
    }

    // "F" * 4 --> cairo.Format.RGBA128F
    #[pyfunction]
    fn pil_f_to_cairo_rgba128f(r: &[u8], g: &[u8], b: &[u8], a: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out: &mut [u8] = unsafe { out.as_bytes_mut() };
        let mut i_in: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_out = y * stride + x * 16;
                let mut r_v = f32::from_ne_bytes([r[i_in], r[i_in + 1], r[i_in + 2], r[i_in + 3]]);
                let mut g_v = f32::from_ne_bytes([g[i_in], g[i_in + 1], g[i_in + 2], g[i_in + 3]]);
                let mut b_v = f32::from_ne_bytes([b[i_in], b[i_in + 1], b[i_in + 2], b[i_in + 3]]);
                let a_v = f32::from_ne_bytes([a[i_in], a[i_in + 1], a[i_in + 2], a[i_in + 3]]);
                r_v *= a_v;
                g_v *= a_v;
                b_v *= a_v;
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = r_v.to_ne_bytes();
                [out[i_out + 4], out[i_out + 5], out[i_out + 6], out[i_out + 7]] = g_v.to_ne_bytes();
                [out[i_out + 8], out[i_out + 9], out[i_out + 10], out[i_out + 11]] = b_v.to_ne_bytes();
                [out[i_out + 12], out[i_out + 13], out[i_out + 14], out[i_out + 15]] = a_v.to_ne_bytes();
                i_in += 4;
            }
        }
    }

    // cairo.Format.RGB30 --> "BGRX"
    #[pyfunction]
    fn cairo_rgb30_to_pil_bgrx(data: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let data = unsafe { data.as_bytes_mut() };
        for y in 0..h {
            for x in 0..w {
                let i = y * stride + x * 4;
                let v = u32::from_ne_bytes([data[i], data[i + 1], data[i + 2], data[i + 3]]);
                let r = ((v >> 20) * 0xff / 0x3ff) as u8;
                let g = (((v >> 10) & 0x3ff) * 0xff / 0x3ff) as u8;
                let b = ((v & 0x3ff) * 0xff / 0x3ff) as u8;
                [data[i], data[i + 1], data[i + 2], data[i + 3]] = [b, g, r, 255];
            }
        }
    }

    // cairo.Format.RGB96F --> "RGB"
    #[pyfunction]
    fn cairo_rgb96f_to_pil_rgb(data: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out: &mut [u8] = unsafe { out.as_bytes_mut() };
        let mut i_out: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_in = y * stride + x * 12;
                let r = f32::from_ne_bytes([data[i_in], data[i_in + 1], data[i_in + 2], data[i_in + 3]]);
                let g = f32::from_ne_bytes([data[i_in + 4], data[i_in + 5], data[i_in + 6], data[i_in + 7]]);
                let b = f32::from_ne_bytes([data[i_in + 8], data[i_in + 9], data[i_in + 10], data[i_in + 11]]);
                [out[i_out], out[i_out + 1], out[i_out + 2]] = [(r * 255.0) as u8, (g * 255.0) as u8, (b * 255.0) as u8];
                i_out += 3;
            }
        }
    }

    // cairo.Format.RGB128F --> "RGB"
    #[pyfunction]
    fn cairo_rgba128f_to_pil_rgba(data: &[u8], out: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let out: &mut [u8] = unsafe { out.as_bytes_mut() };
        let mut i_out: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i_in = y * stride + x * 16;
                let mut r = f32::from_ne_bytes([data[i_in], data[i_in + 1], data[i_in + 2], data[i_in + 3]]);
                let mut g = f32::from_ne_bytes([data[i_in + 4], data[i_in + 5], data[i_in + 6], data[i_in + 7]]);
                let mut b = f32::from_ne_bytes([data[i_in + 8], data[i_in + 9], data[i_in + 10], data[i_in + 11]]);
                let a = f32::from_ne_bytes([data[i_in + 12], data[i_in + 13], data[i_in + 14], data[i_in + 15]]);
                r /= a;
                g /= a;
                b /= a;
                [out[i_out], out[i_out + 1], out[i_out + 2], out[i_out + 3]] = [(r * 255.0) as u8, (g * 255.0) as u8, (b * 255.0) as u8, (a * 255.0) as u8];
                i_out += 4;
            }
        }
    }

    // cairo.Format.RGB30 --> "I" * 3
    #[pyfunction]
    fn cairo_rgb30_to_pil_i(data: &[u8], r: &Bound<'_, PyByteArray>, g: &Bound<'_, PyByteArray>, b: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let r: &mut [u8] = unsafe { r.as_bytes_mut() };
        let g: &mut [u8] = unsafe { g.as_bytes_mut() };
        let b: &mut [u8] = unsafe { b.as_bytes_mut() };
        let mut j: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i = y * stride + x * 4;
                let v = u32::from_ne_bytes([data[i], data[i + 1], data[i + 2], data[i + 3]]);
                let r_v = ((v >> 20) as u64) * 0xffffffff / 0x3ff;
                let g_v = (((v & 0xffc00) >> 10) as u64) * 0xffffffff / 0x3ff;
                let b_v = ((v & 0x3ff) as u64) * 0xffffffff / 0x3ff;
                [r[j], r[j + 1], r[j + 2], r[j + 3]] = (r_v as u32).to_ne_bytes();
                [g[j], g[j + 1], g[j + 2], g[j + 3]] = (g_v as u32).to_ne_bytes();
                [b[j], b[j + 1], b[j + 2], b[j + 3]] = (b_v as u32).to_ne_bytes();
                j += 4;
            }
        }
    }

    // cairo.Format.RGB96F --> "F" * 3
    #[pyfunction]
    fn cairo_rgb96f_to_pil_f(data: &[u8], r: &Bound<'_, PyByteArray>, g: &Bound<'_, PyByteArray>, b: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let r: &mut [u8] = unsafe { r.as_bytes_mut() };
        let g: &mut [u8] = unsafe { g.as_bytes_mut() };
        let b: &mut [u8] = unsafe { b.as_bytes_mut() };
        let mut j: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i = y * stride + x * 12;
                [r[j], r[j + 1], r[j + 2], r[j + 3]] = [data[i], data[i + 1], data[i + 2], data[i + 3]];
                [g[j], g[j + 1], g[j + 2], g[j + 3]] = [data[i + 4], data[i + 5], data[i + 6], data[i + 7]];
                [b[j], b[j + 1], b[j + 2], b[j + 3]] = [data[i + 8], data[i + 9], data[i + 10], data[i + 11]];
                j += 4;
            }
        }
    }

    // cairo.Format.RGBA128F --> "F" * 4
    #[pyfunction]
    fn cairo_rgba128f_to_pil_f(data: &[u8], r: &Bound<'_, PyByteArray>, g: &Bound<'_, PyByteArray>, b: &Bound<'_, PyByteArray>, a: &Bound<'_, PyByteArray>, w: usize, h: usize, stride: usize) {
        let r: &mut [u8] = unsafe { r.as_bytes_mut() };
        let g: &mut [u8] = unsafe { g.as_bytes_mut() };
        let b: &mut [u8] = unsafe { b.as_bytes_mut() };
        let a: &mut [u8] = unsafe { a.as_bytes_mut() };
        let mut j: usize = 0;
        for y in 0..h {
            for x in 0..w {
                let i = y * stride + x * 16;
                let mut r_v = f32::from_ne_bytes([data[i], data[i + 1], data[i + 2], data[i + 3]]);
                let mut g_v = f32::from_ne_bytes([data[i + 4], data[i + 5], data[i + 6], data[i + 7]]);
                let mut b_v = f32::from_ne_bytes([data[i + 8], data[i + 9], data[i + 10], data[i + 11]]);
                let a_v = f32::from_ne_bytes([data[i + 12], data[i + 13], data[i + 14], data[i + 15]]);
                r_v = if a_v == 0.0 { 0.0 } else { r_v / a_v };
                g_v = if a_v == 0.0 { 0.0 } else { g_v / a_v };
                b_v = if a_v == 0.0 { 0.0 } else { b_v / a_v };
                [r[j], r[j + 1], r[j + 2], r[j + 3]] = r_v.to_ne_bytes();
                [g[j], g[j + 1], g[j + 2], g[j + 3]] = g_v.to_ne_bytes();
                [b[j], b[j + 1], b[j + 2], b[j + 3]] = b_v.to_ne_bytes();
                [a[j], a[j + 1], a[j + 2], a[j + 3]] = a_v.to_ne_bytes();
                j += 4;
            }
        }
    }
}
