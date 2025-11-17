import unittest
import textwrap


from block_util import markdown_to_blocks


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
