import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_no_tag_returns_raw_value(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_with_props_contains_all_attributes(self):
        props = {"href": "https://example.com", "target": "_blank"}
        node = LeafNode("a", "link", props=props)
        html = node.to_html()
        self.assertTrue(html.startswith("<a"))
        self.assertTrue(html.endswith(">link</a>"))
        self.assertIn(' href="https://example.com"', html)
        self.assertIn(' target="_blank"', html)

    def test_leaf_to_html_empty_props_has_no_extra_space(self):
        node = LeafNode("span", "x", props={})
        self.assertEqual(node.to_html(), "<span>x</span>")

    def test_leaf_to_html_value_none_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_children_assignment_rules(self):
        node = LeafNode("p", "x")
        # Always exposes children as None
        self.assertIsNone(node.children)
        # Allow assigning None or empty sequences
        node.children = None
        self.assertIsNone(node.children)
        node.children = []
        self.assertIsNone(node.children)
        # Forbid assigning non-empty children
        with self.assertRaises(AttributeError):
            node.children = [LeafNode("span", "y")]


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
