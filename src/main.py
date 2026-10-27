import os
import shutil

from markdown_blocks import extract_title, markdown_to_html_node


def transfer_dir(from_dir: str, to_dir: str):
    if not (os.path.exists(from_dir) and os.path.exists(to_dir)):
        return
    contents = os.listdir(from_dir)
    for file in contents:
        from_file = os.path.join(from_dir, file)
        if os.path.isfile(from_file):
            print(from_file)
            shutil.copy(from_file, to_dir)
        else:
            new_dir = os.path.join(to_dir, file)
            os.mkdir(new_dir)
            transfer_dir(from_file, new_dir)


def transfer_files(from_dir: str, to_dir: str):
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    os.mkdir(to_dir)
    transfer_dir(from_dir, to_dir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        markdown_contents = f.read()
    with open(template_path, encoding="utf-8") as f:
        page_content = f.read()
    html_contents = markdown_to_html_node(markdown_contents).to_html()
    page_title = extract_title(markdown_contents)
    page_content = page_content.replace("{{ Title }}",page_title)
    page_content = page_content.replace("{{ Content }}",html_contents)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for file in contents:
        from_file = os.path.join(dir_path_content, file)
        if os.path.isfile(from_file):
            filename = file.split(".")
            if filename[1]=="md":
                dest_filename = dest_dir_path+"/"+filename[0]+".html"
                generate_page(from_file,template_path,dest_filename)
        else:
            to_dest = os.path.join(dest_dir_path, file)
            if not os.path.exists(to_dest):
                os.mkdir(to_dest)

            generate_pages_recursive(from_file,template_path,to_dest)


def main():
    transfer_files("static","public")
    generate_pages_recursive("content","template.html","public")

if __name__ == "__main__":
    main()
