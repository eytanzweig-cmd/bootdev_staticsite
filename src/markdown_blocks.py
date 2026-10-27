import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes


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
    is_header = True
    if markdown[0] == "#":
        for i in range(1,6):
            if markdown[i] == "#":
                continue
            elif markdown[i] == " ":
                i -= 1
                is_header = True
                break
            else:
                is_header = False
                break
        if markdown[i+1] != " ":
            is_header = False
        if is_header:
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
            if split_lines[i][0] != str(i + 1) or split_lines[i][1] != ".":
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def strip_newlines_and_prefix(block:str, prefix:str | None = None) -> list[str]:
    split_lines = block.split("\n")
    if prefix is not None and prefix != "1":
        for i in range(len(split_lines)):
            if split_lines[i].startswith(prefix):
                split_lines[i] = split_lines[i][len(prefix):len(split_lines[i])]
    if prefix == "1":
        for i in range(len(split_lines)):
            n_prefix = f"{i+1}."
            if split_lines[i].startswith(n_prefix):
                split_lines[i] = split_lines[i][len(n_prefix):len(split_lines[i])]

    return split_lines


def ordered_list_block_to_html_node(block):
    lines = strip_newlines_and_prefix(block,"1")
    leafs = []
    for line in lines:
        inline_nodes = text_to_textnodes(line)
        children = []
        for node in inline_nodes:
            children.append(text_node_to_html_node(node))
        leafs.append(ParentNode("li", children))
    this_block = ParentNode("ol", leafs)
    return this_block

def unordered_list_block_to_html_node(block):
    lines = strip_newlines_and_prefix(block,"-")
    leafs = []
    for line in lines:
        inline_nodes = text_to_textnodes(line)
        children = []
        for node in inline_nodes:
            children.append(text_node_to_html_node(node))
        leafs.append(ParentNode("li", children))
    this_block = ParentNode("ul", leafs)
    return this_block

def quote_block_to_html_node(block):
    block = " ".join(strip_newlines_and_prefix(block,">"))
    leafs = []
    inline_nodes = text_to_textnodes(block)
    for node in inline_nodes:
        leafs.append(text_node_to_html_node(node))
    this_block = ParentNode("blockquote", leafs)
    return this_block

def paragraph_block_to_html_node(block):
    block = " ".join(strip_newlines_and_prefix(block))
    leafs = []
    inline_nodes = text_to_textnodes(block)
    for node in inline_nodes:
        leafs.append(text_node_to_html_node(node))
    this_block = ParentNode("p", leafs)
    return this_block

def code_block_to_html_node(block):
    leafs=[]
    block = block.split("```")[1]
    if block.startswith("\n"):
        block = block[1:len(block)]
    node = TextNode(block,TextType.CODE)
    leafs.append(text_node_to_html_node(node))
    pre_block = ParentNode("pre",leafs)
    return pre_block

def heading_block_to_html_node(block):
    counter = 0
    for i in range(6):
        if block[0] == "#":
            counter += 1
            block = block[1:len(block)]
        elif block[0] == " ":
            block = block[1:len(block)]
            break
        else:
            raise ValueError("Improper heading node")

    leafs = []
    inline_nodes = text_to_textnodes(block)
    for node in inline_nodes:
        leafs.append(text_node_to_html_node(node))
    this_block = ParentNode("h"+str(counter), leafs)
    return this_block

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in md_blocks:
        b_type = block_to_block_type(block)
        match b_type:
            case BlockType.PARAGRAPH:
                html_blocks.append(paragraph_block_to_html_node(block))
            case BlockType.ULIST:
                html_blocks.append(unordered_list_block_to_html_node(block))
            case BlockType.OLIST:
                html_blocks.append(ordered_list_block_to_html_node(block))
            case BlockType.QUOTE:
                html_blocks.append(quote_block_to_html_node(block))
            case BlockType.HEADING:
                html_blocks.append(heading_block_to_html_node(block))
            case BlockType.CODE:
                html_blocks.append(code_block_to_html_node(block))
            case _:
                raise ValueError("Unknown Blocktype")
    output = ParentNode("div", html_blocks)
    return output
