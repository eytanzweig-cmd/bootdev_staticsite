import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def markdown_to_blocks(markdown:str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
       block = block.strip()
       if block != "":
           cleaned_blocks.append(block)
    return cleaned_blocks

def block_to_block_type(markdown:str) -> BlockType:
    if re.match(r"^#{1,6}", markdown):
        return BlockType.HEADING
    return BlockType.PARAGRAPH
