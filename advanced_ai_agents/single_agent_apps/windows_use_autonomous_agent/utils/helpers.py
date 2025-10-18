"""Helper utility functions."""


def shade_color(hex_color: str, factor: float = 0.2) -> str:
    """
    Lighten or darken a hex color.
    
    Args:
        hex_color: Hex color string (e.g., "#2563eb")
        factor: Positive to lighten, negative to darken (-1.0 to 1.0)
        
    Returns:
        Modified hex color string
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    
    if factor > 0:
        # Lighten
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
    else:
        # Darken
        factor = abs(factor)
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
    
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"
