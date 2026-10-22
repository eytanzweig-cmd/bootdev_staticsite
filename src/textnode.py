import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMG = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            if text_node.url is None:
                url = ""
            else:
                url = text_node.url
            return LeafNode("a", text_node.text, {"href": url})
        case TextType.IMG:
            if text_node.url is None:
                url = ""
            else:
                url = text_node.url
            return LeafNode("img", "", {"src": url, "alt": text_node.text})
        case _:
            raise ValueError("Unknown text type!")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid Markdown - delimiter unmatched!")
        for i in range(len(split_text)):
            if i % 2 == 1:
                tt = text_type
            else:
                tt = TextType.PLAIN
            if split_text[i] != "":
                new_nodes.append(TextNode(split_text[i], tt))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        extracted_images = extract_markdown_images(old_node.text)
        text_to_split = old_node.text
        for alttext,imgurl in extracted_images:
            split_text = text_to_split.split(f"![{alttext}]({imgurl})",1)
            new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
            new_nodes.append(TextNode(alttext, TextType.IMG, imgurl))
            text_to_split = split_text[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        extracted_links = extract_markdown_links(old_node.text)
        text_to_split = old_node.text
        for alttext,linkurl in extracted_links:
            split_text = text_to_split.split(f"[{alttext}]({linkurl})",1)
            new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
            new_nodes.append(TextNode(alttext, TextType.LINK, linkurl))
            text_to_split = split_text[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text:str) -> list[TextNode]:
    base_node = TextNode(text,TextType.PLAIN)
    node_list = [base_node]
    node_list = split_nodes_delimiter(node_list,"_",TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list,"**",TextType.BOLD)
    node_list = split_nodes_delimiter(node_list,"`",TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list
