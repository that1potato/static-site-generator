import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_stores_fields(self):
        node = HTMLNode(tag="p", value="hello", children=None, props=None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr_simple(self):
        node = HTMLNode(tag="div", value="content", children=None, props=None)
        self.assertEqual(repr(node), "HTMLNode(div, content, None, None)")

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="span", value="x")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_none(self):
        node = HTMLNode(tag="a", value="link", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="a", value="link", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_values(self):
        # Expect a leading space and key="value" pairs in any order
        props = {"href": "https://example.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="link", props=props)
        out = node.props_to_html()
        # Should start with a single space and contain two attributes
        self.assertTrue(out.startswith(" "), msg=f"Expected leading space, got: {out!r}")
        tokens = out.strip().split(" ") if out else []
        expected = {"href=\"https://example.com\"", "target=\"_blank\""}
        self.assertEqual(set(tokens), expected)


if __name__ == "__main__":
    unittest.main()
