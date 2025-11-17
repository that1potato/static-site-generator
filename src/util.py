import re

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
	pattern = re.compile(
	    r'!\[([^\]]*)\]\(\s*'               # alt text in [...]
	    r'(?:<([^>]+)>|([^)\s]+))\s*'       # either <url> (group 2) or url (group 3)
	    r'(?:["\']([^"\']*)["\']\s*)?'      # optional title in " or ' (group 4)
	    r'\)'
	)
	matches = re.findall(pattern, text)
	return [(alt, (u_br or u_plain)) for alt, u_br, u_plain, _title in matches]


def extract_markdown_links(text):
	'''
	text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
	-> [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
	'''
	pattern = re.compile(r'''
	    \[([^\]]*)\]                	# 1: link text (between [])
	    \(
	      \s*
	      (?:<([^>]+)>|([^\s)]+))  		# 2: url if <...> OR 3: url without brackets
	      \s*
	      (?:["']([^"']*)["']\s*)? 		# 4: optional title in " or '
	    \)
	''', re.VERBOSE)
	matches = re.findall(pattern, text)
	return [
	    (link_text, (u_bracketed or u_plain))
	    for link_text, u_bracketed, u_plain, _title in matches
	    if (u_bracketed or u_plain)
	]
