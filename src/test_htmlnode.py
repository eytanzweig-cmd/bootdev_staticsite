import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("hi", "test", [HTMLNode("boo")], {"a": "b", "<p>": "hello"})
        node2 = HTMLNode("hi", None, None, {"<p>": "hello", "a": "b"})

        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Hello, world!", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Hello, world!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"happy":"sad"})
        self.assertEqual(
            parent_node.to_html(),
            '<div happy="sad"><span><b>grandchild</b></span></div>',
        )

if __name__ == "__main__":
    unittest.main()
