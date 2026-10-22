class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Oops not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        output = ""
        sorted_tags = sorted(self.props.items())
        for k,v in sorted_tags:
            output += f' {k}="{v}"'
        return output

    def __repr__(self) -> str:
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node does not have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"{self.tag}, {self.value}, {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent node does not have a tag")
        if self.children is None:
            raise ValueError("Parent node does not have children")

        html_output = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html_output += child.to_html()

        html_output+= f"</{self.tag}>"

        return html_output


    def __repr__(self) -> str:
        return f"{self.tag}, {self.children}, {self.props}"
