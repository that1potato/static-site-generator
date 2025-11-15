import unittest

from textnode import TextNode, TextType
from util import text_node_to_html_node, split_nodes_delimiter


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_bold_split(self):
        nodes = [TextNode("hello **bold** world", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def test_multiple_formatted_sections(self):
        nodes = [TextNode("a **x** b **y** c", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("x", TextType.BOLD),
                TextNode(" b ", TextType.TEXT),
                TextNode("y", TextType.BOLD),
                TextNode(" c", TextType.TEXT),
            ],
        )

    def test_unbalanced_raises(self):
        nodes = [TextNode("hello **bold", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_non_text_nodes_pass_through(self):
        image = TextNode("an image", TextType.IMAGE, url="https://ex.com/img.png")
        text = TextNode("plain **bold**", TextType.TEXT)
        out = split_nodes_delimiter([image, text], "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                image,
                TextNode("plain ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_only_formatted_content(self):
        nodes = [TextNode("**bold**", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(out, [TextNode("bold", TextType.BOLD)])

    def test_no_delimiter_present(self):
        nodes = [TextNode("plain text", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(out, [TextNode("plain text", TextType.TEXT)])

    def test_consecutive_delimiters_empty_section(self):
        nodes = [TextNode("before **** after", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        # Empty formatted section between the consecutive delimiters is skipped
        self.assertEqual(
            out,
            [TextNode("before ", TextType.TEXT), TextNode(" after", TextType.TEXT)],
        )

    def test_italic_and_code_delimiters(self):
        italic = [TextNode("a *b* c", TextType.TEXT)]
        code = [TextNode("x `y` z", TextType.TEXT)]
        out_i = split_nodes_delimiter(italic, "*", TextType.ITALIC)
        out_c = split_nodes_delimiter(code, "`", TextType.CODE)
        self.assertEqual(
            out_i,
            [TextNode("a ", TextType.TEXT), TextNode("b", TextType.ITALIC), TextNode(" c", TextType.TEXT)],
        )
        self.assertEqual(
            out_c,
            [TextNode("x ", TextType.TEXT), TextNode("y", TextType.CODE), TextNode(" z", TextType.TEXT)],
        )


if __name__ == "__main__":
    unittest.main()
