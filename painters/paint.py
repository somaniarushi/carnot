from defs.box import AnonBox, BlockBox, InlineBox, Box, Rect, BoxType
from defs.css import Color

class Canvas:
    def __init__(self, pixels, width, height):
        self.pixels = pixels
        self.width = width
        self.height = height

class DisplayCommand:
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect

def paint(root, bounds):
    """
    Accepts the root of a layout tree and the bounds of a rect, and paints the tree of layout boxes
    to an array of pixels.
    """
    display = build_display_list(root)

def build_display_list(root):
    return render_layout_box(root)

def render_layout_box(root):
    list = []
    list += render_background(root)
    list += render_borders(root)
    for elem in root.children:
        list += render_layout_box(root)
    return list

def render_background(root):
    return list(map(lambda x: DisplayCommand(x, root.dimensions.border_box()),
                    get_color(root, "background")))


def render_borders(root):
    color = get_color(root, "border-color")
    if not color:
        return []
    d = root.dimensions
    bbox = root.border_box()
    list = []
    # Left border
    list += [DisplayCommand(color, Rect(bbox.x, bbox.y, d.border.left, bbox.height))]
    # Right border
    list += [DisplayCommand(color, Rect(bbox.x + bbox.width - d.border.right, bbox.y, d.border.right, bbox.height))]
    # Top border
    list += [DisplayCommand(color, Rect(bbox.x, bbox.y, bbox.width, d.border.top))]
    # Bottom border
    list += [DisplayCommand(color, Rect(bbox.x, bbox.y + bbox.height - d.border.bottom, bbox.width, d.border.bottom))]
    return list

def get_color(root, name):
    if root.type == BoxType.BLOCK_NODE or root.type == BoxType.INLINE_NODE:
        if root.get_style_node().value(name):
            return root.get_style_node().value(name)
    return None



