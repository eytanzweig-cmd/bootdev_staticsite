import unittest

from markdown_blocks import block_to_block_type, markdown_to_blocks, markdown_to_html_node, extract_title


class TestBlock(unittest.TestCase):
    def test_extrat_title(self):
        print(extract_title("# title test"))
        print(extract_title("## not the title\n#     the actual title"))

    def test_markdown_to_blocks(self):
        md = """
### Header

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

```
This is a code block```

- This is a list
- with items

1. This is an ordered list
2. This is the next item
3. And this is the third item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "### Header",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "```\nThis is a code block```",
                "- This is a list\n- with items",
                "1. This is an ordered list\n2. This is the next item\n3. And this is the third item",
            ],
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
