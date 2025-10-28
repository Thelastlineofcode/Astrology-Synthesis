# Simple WCAG contrast checker
# Prints contrast ratios for a set of color pairs

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0,2,4))


def linearize(c):
    if c <= 0.03928:
        return c/12.92
    return ((c+0.055)/1.055) ** 2.4


def rel_lum(hexcolor):
    r,g,b = hex_to_rgb(hexcolor)
    return 0.2126*linearize(r) + 0.7152*linearize(g) + 0.0722*linearize(b)


def contrast(a,b):
    la = rel_lum(a)
    lb = rel_lum(b)
    L1 = max(la, lb)
    L2 = min(la, lb)
    return (L1+0.05)/(L2+0.05)

if __name__ == '__main__':
    pairs = [
        ("Primary on light bg", "#3E4B6E", "#F5F3EE"),
        ("Text primary on light bg", "#2D3142", "#F5F3EE"),
        ("Text primary on dark bg", "#F5F3EE", "#2D3142"),
        ("CTA on light bg", "#C17B5C", "#F5F3EE"),
        ("Accent on light bg", "#B296CA", "#F5F3EE"),
        ("Primary on dark bg", "#3E4B6E", "#2D3142"),
        ("Neutral-700 on light bg", "#4A4E5C", "#F5F3EE"),
        ("Text on CTA background", "#F5F3EE", "#C17B5C"),
        ("Text on Accent background", "#F5F3EE", "#B296CA"),
        ("White text on CTA background", "#ffffff", "#C17B5C"),
        ("White text on Accent background", "#ffffff", "#B296CA"),
        ("Dark text on CTA background", "#2D3142", "#C17B5C"),
    ]

    print("Contrast check results (WCAG ratios):")
    for name, fg, bg in pairs:
        r = contrast(fg, bg)
        print(f"{name}: fg={fg} bg={bg} -> {r:.2f}:1")
