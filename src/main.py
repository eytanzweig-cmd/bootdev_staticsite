import os
import shutil

from markdown_blocks import markdown_to_blocks, markdown_to_html_node
from textnode import TextNode, TextType

def transfer_dir(from_dir:str, to_dir:str):
    if not (os.path.exists(from_dir) and os.path.exists(to_dir)):
        return
    contents = os.listdir(from_dir)
    for file in contents:
        from_file = os.path.join(from_dir,file)
        if os.path.isfile(from_file):
            print(from_file)
            shutil.copy(from_file,to_dir)
        else:
            new_dir = os.path.join(to_dir,file)
            os.mkdir(new_dir)
            transfer_dir(from_file,new_dir)


def transfer_files(from_dir:str, to_dir:str):
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    os.mkdir(to_dir)
    transfer_dir(from_dir, to_dir)



def main():
    transfer_files("static","public")
    a = markdown_to_html_node(
        "### Header\n\n1.this is a simple test, \n2.with a [url](google.com)"
    )
    b = markdown_to_html_node(
        "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
    )


if __name__ == "__main__":
    main()
