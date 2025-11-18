'''
Block-level markdown is the separation of different sections of an entire document. This assumes blocks are separated by a single blank line.
'''

from enum import Enum


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
