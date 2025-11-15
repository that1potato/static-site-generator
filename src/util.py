from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    '''
    convert a TextNode to an HTMLNode
    '''
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f'invalid text type: {text_node.text_type}')


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    takes a list of "old nodes", a delimiter, and a text type.
    return a new list of nodes, where any "text" type nodes in
    the input list are (potentially) split into multiple nodes based on the syntax
    '''
    pass
