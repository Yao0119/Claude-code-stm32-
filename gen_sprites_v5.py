r"""
Generate animated bold iconic cat sprites for SSD1306 OLED.
Each state has 2-3 frames for animation. Format: 72x48 pixels.
"""

W, H = 72, 48

def blank():
    return [[0]*W for _ in range(H)]

def set_px(p, r, c, v=1):
    if 0 <= r < H and 0 <= c < W:
        p[r][c] = v

def line_h(p, r, c1, c2, v=1):
    for c in range(c1, c2+1):
        set_px(p, r, c, v)

def line_v(p, c, r1, r2, v=1):
    for r in range(r1, r2+1):
        set_px(p, r, c, v)

def rect(p, r1, c1, r2, c2, v=1):
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            set_px(p, r, c, v)

def circle(p, cr, cc, radius, v=1):
    for r in range(H):
        for c in range(W):
            if (r-cr)**2 + (c-cc)**2 <= radius**2:
                set_px(p, r, c, v)

def ellipse(p, cr, cc, rh, rw, v=1):
    for r in range(H):
        for c in range(W):
            if (r-cr)**2/(rh*rh) + (c-cc)**2/(rw*rw) <= 1.0:
                set_px(p, r, c, v)

def triangle_up(p, x, y, bw, h, v=1):
    for r in range(h):
        cur_w = int(bw * (r + 1) / h)
        start = x + (bw - cur_w) // 2
        for c in range(start, start + cur_w):
            set_px(p, y + h - 1 - r, c, v)

def triangle_down(p, x, y, bw, h, v=1):
    for r in range(h):
        cur_w = int(bw * r / h)
        start = x + (bw - cur_w) // 2
        for c in range(start, start + cur_w):
            set_px(p, y + r, c, v)

def copy_px(p):
    return [row[:] for row in p]

# =========== BASE CAT ===========
def base_cat():
    p = blank()
    # Ears
    triangle_up(p, 8, 0, 18, 14, 1)
    triangle_up(p, 11, 3, 12, 9, 0)
    triangle_up(p, 46, 0, 18, 14, 1)
    triangle_up(p, 49, 3, 12, 9, 0)
    # Head
    ellipse(p, 18, 36, 15, 28, 1)
    rect(p, 5, 18, 8, 54, 1)
    # Eyes
    circle(p, 19, 24, 6, 1)
    circle(p, 19, 24, 3, 0)
    set_px(p, 17, 22, 1)
    set_px(p, 17, 21, 1)
    circle(p, 19, 48, 6, 1)
    circle(p, 19, 48, 3, 0)
    set_px(p, 17, 46, 1)
    set_px(p, 17, 45, 1)
    # Nose
    triangle_down(p, 34, 24, 6, 4, 1)
    set_px(p, 25, 36, 1)
    # Mouth
    set_px(p, 28, 30, 0)
    set_px(p, 28, 36, 0)
    set_px(p, 28, 42, 0)
    set_px(p, 29, 32, 0)
    set_px(p, 29, 38, 0)
    # Whiskers
    for r in [22, 24, 26]:
        line_h(p, r, 2, 14, 0)
        line_h(p, r, 58, 70, 0)
    # Body
    ellipse(p, 39, 38, 9, 18, 1)
    # Paws
    circle(p, 46, 30, 3, 1)
    circle(p, 46, 46, 3, 1)
    return p

# =========== ANIMATED STATE FUNCTIONS ===========

# --- INIT: Waving paw (3 frames) ---
def cat_init_frames():
    frames = []
    # F0: paw high
    p = base_cat()
    rect(p, 4, 56, 12, 66, 1)
    circle(p, 4, 61, 4, 1)
    line_h(p, 1, 52, 70, 1)
    line_h(p, 6, 52, 70, 1)
    frames.append(p)
    # F1: paw mid
    p = base_cat()
    rect(p, 6, 56, 14, 66, 1)
    circle(p, 6, 61, 4, 1)
    line_h(p, 3, 52, 70, 1)
    line_h(p, 8, 52, 70, 1)
    frames.append(p)
    # F2: paw low (near base cat, small wave)
    p = base_cat()
    rect(p, 10, 56, 18, 66, 1)
    circle(p, 10, 61, 4, 1)
    frames.append(p)
    return frames

# --- IDLE: Breathing (2 frames) ---
def cat_idle_frames():
    frames = []
    for f in range(2):
        p = base_cat()
        # Closed eyes
        line_h(p, 18, 18, 30, 1)
        line_h(p, 17, 20, 28, 1)
        rect(p, 19, 18, 20, 30, 0)
        line_h(p, 19, 18, 30, 0)
        line_h(p, 18, 42, 54, 1)
        line_h(p, 17, 44, 52, 1)
        rect(p, 19, 42, 20, 54, 0)
        line_h(p, 19, 42, 54, 0)
        # Zzz
        line_h(p, 3, 58, 64, 1)
        line_v(p, 56, 1, 3, 1)
        line_h(p, 5, 54, 64, 1)
        line_v(p, 64, 3, 5, 1)
        line_h(p, 9, 62, 68, 1)
        line_v(p, 60, 7, 9, 1)
        line_h(p, 11, 58, 68, 1)
        line_v(p, 68, 9, 11, 1)
        # Body wider on frame 1 (inhale)
        if f == 1:
            ellipse(p, 39, 38, 9, 20, 1)
        frames.append(p)
    return frames

# --- CODE: Typing (3 frames) ---
def cat_code_frames():
    frames = []
    for f in range(3):
        p = base_cat()
        # Focused eyes
        circle(p, 19, 24, 6, 1)
        ellipse(p, 20, 24, 2, 3, 0)
        set_px(p, 17, 22, 1)
        circle(p, 19, 48, 6, 1)
        ellipse(p, 20, 48, 2, 3, 0)
        set_px(p, 17, 46, 1)
        # Keyboard
        rect(p, 44, 16, 47, 56, 1)
        # Alternating lit rows
        if f == 0:
            line_h(p, 45, 17, 55, 0)  # row 1 lit
        elif f == 1:
            line_h(p, 46, 17, 55, 0)  # row 2 lit
        else:
            line_h(p, 45, 17, 55, 0)  # both
            line_h(p, 46, 17, 55, 0)
        frames.append(p)
    return frames

# --- DOCS: Reading (2 frames) ---
def cat_docs_frames():
    frames = []
    for f in range(2):
        p = base_cat()
        circle(p, 19, 24, 5, 1)
        circle(p, 19, 24 + f*2, 2, 0)  # pupil shifts right
        set_px(p, 17, 22, 1)
        circle(p, 19, 48, 5, 1)
        circle(p, 19, 48 + f*2, 2, 0)
        set_px(p, 17, 46, 1)
        # Paper
        rect(p, 33, 56, 45, 70, 1)
        line_h(p, 36, 57, 69, 0)
        line_h(p, 38, 57, 69, 0)
        line_h(p, 40, 57, 69, 0)
        line_h(p, 42, 57, 69, 0)
        frames.append(p)
    return frames

# --- THINK: Thought bubble pulsing (3 frames) ---
def cat_think_frames():
    frames = []
    sizes = [3, 5, 4]  # Small → big → medium (oscillate)
    for i, sz in enumerate(sizes):
        p = base_cat()
        circle(p, 19, 24, 5, 1)
        circle(p, 17, 24, 2, 0)  # pupil high
        set_px(p, 20, 22, 1)
        circle(p, 19, 48, 5, 1)
        circle(p, 17, 48, 2, 0)
        set_px(p, 20, 46, 1)
        # Thought bubbles
        circle(p, 7, 56, sz, 1)
        circle(p, 3, 62, max(1, sz-2), 1)
        circle(p, 0, 66, max(1, sz-3), 1)
        # Paw on chin
        circle(p, 30, 32, 4, 1)
        frames.append(p)
    return frames

# --- SEARCH: Eye scanning (2 frames) ---
def cat_search_frames():
    frames = []
    offsets = [-2, 2]  # left, right
    for off in offsets:
        p = base_cat()
        circle(p, 19, 24, 5, 1)
        circle(p, 19, 21 + off, 2, 0)  # pupil shift
        set_px(p, 17, 26, 1)
        circle(p, 19, 48, 5, 1)
        circle(p, 19, 45 + off, 2, 0)
        set_px(p, 17, 50, 1)
        # Magnifying glass
        circle(p, 39, 62, 5, 1)
        circle(p, 39, 62, 4, 0)
        rect(p, 41, 65, 46, 67, 1)
        frames.append(p)
    return frames

# --- EXPER: Bubbles rising (3 frames) ---
def cat_exper_frames():
    frames = []
    bubble_positions = [(37, 7, 35, 5), (34, 8, 32, 6), (31, 9, 29, 7)]
    for (b1r, b1c, b2r, b2c) in bubble_positions:
        p = base_cat()
        circle(p, 19, 24, 6, 1)
        circle(p, 19, 24, 2, 0)
        set_px(p, 16, 21, 1)
        set_px(p, 16, 22, 1)
        circle(p, 19, 48, 6, 1)
        circle(p, 19, 48, 2, 0)
        set_px(p, 16, 45, 1)
        set_px(p, 16, 46, 1)
        # Beaker
        rect(p, 38, 6, 39, 14, 1)
        rect(p, 40, 2, 45, 18, 1)
        rect(p, 41, 4, 44, 16, 0)
        # Rising bubbles
        circle(p, b1r, b1c, 2, 1)
        circle(p, b2r, b2c, 2, 1)
        frames.append(p)
    return frames

# --- ERROR: Shaking (3 frames) ---
def cat_error_frames():
    frames = []
    offsets = [0, -2, 2]  # normal, left shake, right shake
    for off in offsets:
        p = base_cat()
        circle(p, 19, 24, 6, 1)
        circle(p, 19, 24, 1, 0)
        set_px(p, 16, 21, 1)
        circle(p, 19, 48, 6, 1)
        circle(p, 19, 48, 1, 0)
        set_px(p, 16, 45, 1)
        circle(p, 30, 36, 3, 0)  # open mouth
        # Shaking exclamation mark
        rect(p, 12, 63 + off, 16, 65 + off, 1)
        rect(p, 18, 63 + off, 19, 65 + off, 1)
        frames.append(p)
    return frames

# =========== Convert to vertical-byte format ===========
def to_vbytes(pixels):
    pages = [[0]*W for _ in range(6)]
    for page in range(6):
        for col in range(W):
            b = 0
            for bit in range(8):
                row = page * 8 + bit
                if row < H and pixels[row][col]:
                    b |= (1 << bit)
            pages[page][col] = b
    return pages

# =========== Output C header ===========
def gen_header():
    states = [
        ("INIT",  cat_init_frames()),
        ("IDLE",  cat_idle_frames()),
        ("CODE",  cat_code_frames()),
        ("DOCS",  cat_docs_frames()),
        ("THINK", cat_think_frames()),
        ("SEARCH", cat_search_frames()),
        ("EXPER", cat_exper_frames()),
        ("ERROR", cat_error_frames()),
    ]

    lines = []
    lines.append("// Animated bold iconic cat sprites for Claude Code OLED")
    lines.append("// Format: 72x48 pixels, 6 pages x 72 cols")
    lines.append("")

    # Track total bytes
    total = 0

    for name, frames in states:
        n = len(frames)
        lines.append(f"/* === {name} — {n} frames === */")
        for fi, pixels in enumerate(frames):
            data = to_vbytes(pixels)
            total += 6 * 72
            lines.append(f"static const uint8_t sprite_{name}_F{fi}[6][72] = {{")
            for page in range(6):
                bs = ",".join(f"0x{b:02X}" for b in data[page])
                lines.append(f"    {{{bs}}},")
            lines.append("};")
        # Frame pointer array
        ptrs = ", ".join(f"(const uint8_t(*)[72])sprite_{name}_F{fi}" for fi in range(n))
        lines.append(f"static const uint8_t (*sprite_{name}_frames[{n}])[72] = {{{ptrs}}};")
        lines.append("")

    lines.append(f"// Total sprite data: {total} bytes")

    # Sprite descriptor struct
    lines.append("")
    lines.append("typedef struct {")
    lines.append("    const uint8_t (**frames)[72];")
    lines.append("    uint8_t count;")
    lines.append("} CatSprite;")
    lines.append("")

    # Master lookup table
    lines.append(f"static const CatSprite cat_sprites[{len(states)}] = {{")
    for name, frames in states:
        n = len(frames)
        lines.append(f"    {{sprite_{name}_frames, {n}}},")
    lines.append("};")
    lines.append("")

    # Name table
    lines.append("static const char *cat_sprite_names[] = {")
    for name, _ in states:
        lines.append(f'    "{name}",')
    lines.append("};")

    return "\n".join(lines)

if __name__ == '__main__':
    print("#ifndef __CAT_SPRITES_H")
    print("#define __CAT_SPRITES_H")
    print("")
    print('#include "stm32f10x.h"')
    print("")
    print(gen_header())
    print("")
    print("#endif")
