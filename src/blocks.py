import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            cleaned_blocks.append(block)
    return cleaned_blocks


def block_to_block_type(markdown: str) -> BlockType:
    if re.match(r"^#{1,6}", markdown):
        return BlockType.HEADING
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    split_lines = markdown.split("\n")
    first_symbol = markdown[0]
    if first_symbol == ">" or first_symbol == "-":
        for line in split_lines:
           if line[0] != first_symbol:
              return BlockType.PARAGRAPH
        if first_symbol == ">":
            return BlockType.QUOTE
        return BlockType.ULIST
    if first_symbol == "1":
        for i in range(len(split_lines)):
            if split_lines[i][0] != str(i+1) or split_lines[i][1] != ".":
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH
