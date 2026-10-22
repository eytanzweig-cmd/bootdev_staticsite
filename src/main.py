from textnode import TextNode, TextType


def main():
    a = TextNode("test text", TextType.BOLD, "http://text.html")
    print(a)


if __name__ == "__main__":
    main()
