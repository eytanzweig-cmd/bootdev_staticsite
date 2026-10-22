import unittest

from blocks import block_to_block_type, markdown_to_blocks


class TestBlock(unittest.TestCase):
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
                    "1. This is an ordered list\n2. This is the next item\n3. And this is the third item"
                ],
            )

            for block in blocks:
                print(block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()
