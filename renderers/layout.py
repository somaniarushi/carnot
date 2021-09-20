from defs.box import Box, BoxType



def build_layout_tree(style_node):
    """
    Build the layout tree with displays but without dimensions.
    """
    def get_box_type(node):
        """
        Returns the type of box based on the display value
        """
        disp = node.display()
        if disp == 'block':
            return BoxType.BLOCK_NODE
        elif disp == 'inline':
            return BoxType.INLINE_NODE
        elif disp == 'none':
            raise Exception("Root node can't have display none")

    disp = get_box_type(style_node)
    root = Box(None, disp, [])

    for child in style_node.children:
        if get_box_type(child) == BoxType.BLOCK_NODE:
            root.children.append(build_layout_tree(child))
        elif get_box_type(child) == BoxType.INLINE_NODE:
            root.get_inline_container().children.append(build_layout_tree(child))
        else:
            continue

    return root




