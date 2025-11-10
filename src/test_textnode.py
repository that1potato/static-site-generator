import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_0(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_1(self):
        node = TextNode('This is a text node', TextType.BOLD, url='https://www.example.com')
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_2(self):
        node = TextNode('This is a text node.', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_repr_0(self):
        node = TextNode('test', TextType.BOLD, url='https://www.example.com')
        self.assertEqual(repr(node), 'TextNode(test, bold, https://www.example.com)')
    
    def test_repr_1(self):
        node = TextNode('test', TextType.ITALIC)
        self.assertEqual(repr(node), 'TextNode(test, italic, None)')


if __name__ == "__main__":
    unittest.main()
    