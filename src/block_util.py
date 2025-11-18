'''
Block-level markdown is the separation of different sections of an entire document. This assumes blocks are separated by a single blank line.
'''

from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_util import text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
	PARAGRAPH = 'paragraph'
	HEADING = 'heading'
	CODE = 'code'
	QUOTE = 'quote'
	UNORDERED_LIST = 'unordered_list'
	ORDERED_LIST = 'ordered_list'


def markdown_to_blocks(markdown):
    '''
    takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings.
    Separation is strictly by exactly two newlines ("\n\n").
    '''
    if markdown is None:
        return []
    text = markdown.strip()
    if not text:
        return []
    parts = text.split("\n\n")
    blocks = [p.strip() for p in parts if p.strip()]
    return blocks


def block_to_block_type(block):
	lines = block.split("\n")

	if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
		return BlockType.HEADING
	if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
		return BlockType.CODE
	if block.startswith(">"):
		for line in lines:
			if not line.startswith(">"):
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	if block.startswith("- "):
		for line in lines:
			if not line.startswith("- "):
				return BlockType.PARAGRAPH
		return BlockType.UNORDERED_LIST
	if block.startswith("1. "):
		i = 1
		for line in lines:
			if not line.startswith(f"{i}. "):
				return BlockType.PARAGRAPH
			i += 1
		return BlockType.ORDERED_LIST
	return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
	'''
	converts a full markdown document into a single parent HTMLNode, containing many child HTMLNode objects representing the nested elements.
	'''
	blocks = markdown_to_blocks(markdown)
	block_nodes = [_block_to_html_node(block) for block in blocks]
	if not block_nodes:
		block_nodes = [LeafNode(None, "")]
	return ParentNode("div", block_nodes)


def _block_to_html_node(block):
	block_type = block_to_block_type(block)
	if block_type == BlockType.PARAGRAPH:
		return _paragraph_block_to_node(block)
	if block_type == BlockType.HEADING:
		return _heading_block_to_node(block)
	if block_type == BlockType.CODE:
		return _code_block_to_node(block)
	if block_type == BlockType.QUOTE:
		return _quote_block_to_node(block)
	if block_type == BlockType.UNORDERED_LIST:
		return _unordered_list_block_to_node(block)
	if block_type == BlockType.ORDERED_LIST:
		return _ordered_list_block_to_node(block)
	raise ValueError(f"Unsupported block type: {block_type}")


def _paragraph_block_to_node(block):
	text = block.replace("\n", " ")
	return ParentNode("p", text_to_children(text))


def _heading_block_to_node(block):
	level = 0
	while level < len(block) and block[level] == "#":
		level += 1
	text = block[level:].strip()
	return ParentNode(f"h{level}", text_to_children(text))


def _code_block_to_node(block):
	lines = block.split("\n")
	has_fence = len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```")
	if has_fence:
		lines = lines[1:-1]
	code_text = "\n".join(lines)
	if has_fence and block.endswith("\n```") and not code_text.endswith("\n"):
		code_text += "\n"
	code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
	return ParentNode("pre", [code_node])


def _quote_block_to_node(block):
	lines = block.split("\n")
	stripped = [_strip_quote_prefix(line) for line in lines]
	quote_text = "\n".join(stripped).strip()
	return ParentNode("blockquote", text_to_children(quote_text))


def _unordered_list_block_to_node(block):
	items = []
	for line in block.split("\n"):
		if not line:
			continue
		item_text = line[2:] if line.startswith("- ") else line
		items.append(ParentNode("li", text_to_children(item_text.strip())))
	return ParentNode("ul", items)


def _ordered_list_block_to_node(block):
	items = []
	for line in block.split("\n"):
		if not line:
			continue
		item_text = _strip_ordered_list_marker(line)
		items.append(ParentNode("li", text_to_children(item_text)))
	return ParentNode("ol", items)


def _strip_quote_prefix(line):
	if not line.startswith(">"):
		return line.strip()
	text = line[1:]
	if text.startswith(" "):
		text = text[1:]
	return text.strip()


def _strip_ordered_list_marker(line):
	i = 0
	while i < len(line) and line[i].isdigit():
		i += 1
	if i < len(line) and line[i] == ".":
		i += 1
	while i < len(line) and line[i] == " ":
		i += 1
	return line[i:].strip()


def text_to_children(text):
	if text is None:
		text = ""
	text_nodes = text_to_textnodes(text)
	return [text_node_to_html_node(node) for node in text_nodes]
