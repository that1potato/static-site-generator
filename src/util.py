import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


IMAGE_PATTERN = re.compile(
    r'!\[([^\]]*)\]\(\s*'
    r'(?:<([^>]+)>|([^)\s]+))\s*'
    r'(?:["\']([^"\']*)["\']\s*)?'
    r'\)'
)

LINK_PATTERN = re.compile(
    r'''
    \[([^\]]*)\]
    \(
      \s*
      (?:<([^>]+)>|([^\s)]+))
      \s*
      (?:["']([^"']*)["']\s*)?
    \)
    ''',
    re.VERBOSE,
)


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
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError('invalid markdown, formatted section not closed')
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
	'''
	text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
	-> [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
	'''
	matches = IMAGE_PATTERN.findall(text)
	return [(alt, (u_br or u_plain)) for alt, u_br, u_plain, _title in matches]


def extract_markdown_links(text):
	'''
	text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
	-> [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
	'''
	matches = LINK_PATTERN.findall(text)
	return [
	    (link_text, (u_bracketed or u_plain))
	    for link_text, u_bracketed, u_plain, _title in matches
	    if (u_bracketed or u_plain)
	]


def split_nodes_image(old_nodes):
    return _split_nodes_by_pattern(old_nodes, IMAGE_PATTERN, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return _split_nodes_by_pattern(old_nodes, LINK_PATTERN, TextType.LINK)


def _split_nodes_by_pattern(old_nodes, pattern, new_text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        last_index = 0
        found_match = False
        for match in pattern.finditer(text):
            found_match = True
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
            match_text = match.group(1)
            url = match.group(2) or match.group(3)
            new_nodes.append(TextNode(match_text, new_text_type, url))
            last_index = end
        if not found_match:
            new_nodes.append(old_node)
            continue
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes
