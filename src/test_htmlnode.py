import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("hi", "test", [HTMLNode("boo")], {"a":"b","<p>":"hello"})
        node2 = HTMLNode("hi", None, None,{"<p>":"hello","a":"b"})

        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Hello, world!", {"href":"www.google.com"})
        print(node)
        self.assertEqual(node.to_html(), '<a href="www.google.com">Hello, world!</a>')

if __name__ == "__main__":
    unittest.main()
