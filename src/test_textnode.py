import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.IMG, "http://test.bmp")
        node2 = TextNode("This is a text node", TextType.IMG, "http://test.bmp")

        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)

        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "xyz")

        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

        node = TextNode("This is an image node", TextType.IMG, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")

    def test_splitter(self):
        node = TextNode("This node has _italic_ text", TextType.PLAIN)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("This node has ", TextType.PLAIN, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" text", TextType.PLAIN, None),
            ],
        )

        node = TextNode("This node has italic text", TextType.PLAIN)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [node])

        node = TextNode("This node has **bold** text", TextType.PLAIN)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 3)

        node = TextNode("This **node** has **bold** text", TextType.PLAIN)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 5)

        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.PLAIN
        )
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 4)

        node = TextNode("**bold** and _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)

        node = TextNode("This is text with a `unclosed code block word", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
            "This is text without an image"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
            "This is text with a link: [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
            "This is text without an image"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
            "This is text with a link: [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ", TextType.PLAIN),
                TextNode("image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
