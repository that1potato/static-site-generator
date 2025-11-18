import unittest
import textwrap


from block_util import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = textwrap.dedent(
			"""
			This is **bolded** paragraph

			This is another paragraph with _italic_ text and `code` here
			This is the same paragraph on a new line

			- This is a list
			- with items
			"""
		).strip()
		blocks = markdown_to_blocks(md)
		self.assertEqual(
            blocks,
            [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
        )

	def test_single_newline_does_not_split(self):
		md = "First line\nSecond line"
		self.assertEqual(
			markdown_to_blocks(md), ["First line\nSecond line"]
		)

	def test_leading_trailing_blanklines_ignored(self):
		md = "\n\nA\n\nB\n\n"
		self.assertEqual(markdown_to_blocks(md), ["A", "B"])

	def test_two_separators_three_blocks(self):
		md = "A\n\nB\n\nC"
		self.assertEqual(markdown_to_blocks(md), ["A", "B", "C"])

	def test_empty_or_whitespace_only_yields_empty_list(self):
		self.assertEqual(markdown_to_blocks(""), [])
		self.assertEqual(markdown_to_blocks(" \n\t \n\n  \n"), [])


class TestBlockToBlockType(unittest.TestCase):
	def test_block_to_block_types(self):
		block = '# heading'
		self.assertEqual(block_to_block_type(block), BlockType.HEADING)
		block = '```\ncode\n```'
		self.assertEqual(block_to_block_type(block), BlockType.CODE)
		block = '> quote\n> more quote'
		self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
		block = '- list\n- items'
		self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
		block = '1. list\n2. items'
		self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
		block = 'paragraph'
		self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
	def test_paragraphs(self):
		md = textwrap.dedent(
			"""
			This is **bolded** paragraph
			text in a p
			tag here

			This is another paragraph with _italic_ text and `code` here

			"""
		)


		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
	        html,
	        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
	    )

	def test_codeblock(self):
		md = textwrap.dedent(
			"""
			```
			This is text that _should_ remain
			the **same** even with inline stuff
			```
			"""
		)

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
	        html,
	        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
	    )
