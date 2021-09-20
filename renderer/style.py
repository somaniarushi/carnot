from defs.style_tree import StyledNode
from defs.dom import NodeType

class MatchedRule:
    def __init__(self, rule=None, specificity=0):
        self.rule = rule
        self.specificity = specificity

def matches(elem, selector):
    """
    Returns true if the element consists of the selector
    and false otherwise.
    """
    if selector.tag_name != elem.tag_name or \
    selector.id != elem.id() or \
    selector.classes != elem.classes():
        return False

    return True

def match_rule(elem, rule):
    """
    Returns a tuple of the rule and its specificity score
    if it matches elem, and None otherwise.
    """
    specificity = None
    for selector in rule.selectors:
        if matches(elem, selector):
            specificity = selector.specificity()

    if specificity == None:
        return None
    else:
        return MatchedRule(rule, specificity)

def match_rules(elem, stylesheet):
    """
    Find all the CSS rules that match a given element.
    """
    rule_set = []
    for rule in stylesheet.rules:
        matcher = match_rule(elem, rule)
        if matcher:
            rule_set.append(matcher)
    return rule_set

def specified_values(elem, stylesheet):
    """
    Apply the styles to a single element, returning the specified
    values.
    """
    values={}
    matched_rules = match_rules(elem, stylesheet)
    matched_rules.sort(key=lambda x: x.specificity)
    for matched_rule in matched_rules:
        for dec in matched_rule.rule.declarations:
            values[dec.name] = dec.value()
    return values

def styled_tree(root, stylesheet):
    spec_values = specified_values(root, stylesheet) if root.node_type == NodeType.ELEMENT else {}
    children = []
    for child in root.children:
        children.append(styled_tree(child, stylesheet))
    return StyledNode(root, spec_values, children)
