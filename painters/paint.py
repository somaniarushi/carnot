from defs.box import AnonBox, BlockBox, InlineBox, Box, Rect, BoxType
from defs.css import Color

class Canvas:
    def __init__(self, width, height, pixels=[]):
        self.width = width
        self.height = height
        if pixels:
            self.pixels = pixels
        else:
            white = Color(255, 255, 255, 255)
            self.pixels = [white for _ in range(self.width * self.height)]

    def paint_item(self, item):
        x0 = min(item.rect.x, self.width)
        y0 = min(item.rect.y, self.height)

        x1 = min(item.rect.x + item.rect.width, self.width)
        y1 = min(item.rect.y + item.rect.height, self.height)

        for y in [y0, y1]:
            for x in [x0, x1]:
                self.pixels[y * self.width + x] = item.color


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
    canvas = Canvas(bounds.width, bounds.height)
    for item in display:
        canvas.paint_item(item)
    return canvas

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
    # Adding borders
    list = [
        DisplayCommand(color, Rect(bbox.x, bbox.y, d.border.left, bbox.height)),
        DisplayCommand(color, Rect(bbox.x + bbox.width - d.border.right, bbox.y, d.border.right, bbox.height)),
        DisplayCommand(color, Rect(bbox.x, bbox.y, bbox.width, d.border.top)),
        DisplayCommand(color, Rect(bbox.x, bbox.y + bbox.height - d.border.bottom, bbox.width, d.border.bottom))
    ]
    return list

def get_color(root, name):
    if root.type == BoxType.BLOCK_NODE or root.type == BoxType.INLINE_NODE:
        if root.get_style_node().value(name):
            return root.get_style_node().value(name)
    return None



