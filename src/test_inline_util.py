import unittest

from textnode import TextNode, TextType
from inline_util import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "Gallery: ![one](https://imgs.ex/1.png) and ![two](https://imgs.ex/2.jpg)"
        )
        self.assertListEqual(
            [("one", "https://imgs.ex/1.png"), ("two", "https://imgs.ex/2.jpg")],
            matches,
        )

    def test_image_with_bracketed_url_and_title(self):
        matches = extract_markdown_images(
            'Diagram ![flow](<https://imgs.ex/diagram v1.svg> "diagram v1")'
        )
        self.assertListEqual(
            [("flow", "https://imgs.ex/diagram v1.svg")],
            matches,
        )

    def test_image_with_empty_alt_text(self):
        matches = extract_markdown_images("Missing alt ![](https://imgs.ex/no-alt.png)")
        self.assertListEqual([("", "https://imgs.ex/no-alt.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "Docs at [boot](https://www.boot.dev) or [gh](https://github.com/bootdotdev)"
        )
        self.assertListEqual(
            [("boot", "https://www.boot.dev"), ("gh", "https://github.com/bootdotdev")],
            matches,
        )

    def test_link_with_bracketed_url_and_title(self):
        matches = extract_markdown_links(
            "Refer to [spec](<https://specs.ex/1.0 draft.pdf> 'draft') for details"
        )
        self.assertListEqual(
            [("spec", "https://specs.ex/1.0 draft.pdf")],
            matches,
        )

    def test_link_with_empty_text(self):
        matches = extract_markdown_links(
            "Bare [](<https://example.com/resource>) link text allowed"
        )
        self.assertListEqual([("", "https://example.com/resource")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_basic_image_split(self):
        nodes = [TextNode("Intro ![alt](https://imgs.ex/a.png) outro", TextType.TEXT)]
        out = split_nodes_image(nodes)
        self.assertEqual(
            out,
            [
                TextNode("Intro ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://imgs.ex/a.png"),
                TextNode(" outro", TextType.TEXT),
            ],
        )

    def test_multiple_images_and_non_text_nodes(self):
        nodes = [
            TextNode("![one](https://imgs.ex/1.png) + ![two](https://imgs.ex/2.png)", TextType.TEXT),
            TextNode("plain", TextType.BOLD),
        ]
        out = split_nodes_image(nodes)
        self.assertEqual(
            out,
            [
                TextNode("one", TextType.IMAGE, "https://imgs.ex/1.png"),
                TextNode(" + ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://imgs.ex/2.png"),
                TextNode("plain", TextType.BOLD),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_basic_link_split(self):
        nodes = [
            TextNode(
                "See [boot dev](https://www.boot.dev) for [more](https://example.com/more)",
                TextType.TEXT,
            )
        ]
        out = split_nodes_link(nodes)
        self.assertEqual(
            out,
            [
                TextNode("See ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" for ", TextType.TEXT),
                TextNode("more", TextType.LINK, "https://example.com/more"),
            ],
        )

    def test_no_links_returns_original_nodes(self):
        nodes = [TextNode("Just text", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(out, nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_full_markdown_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_supports_underscore_bold_and_italic(self):
        text = "Mix of __bold__ and _italic_ plus __combo__"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Mix of ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" plus ", TextType.TEXT),
                TextNode("combo", TextType.BOLD),
            ],
        )


if __name__ == "__main__":
    unittest.main()
