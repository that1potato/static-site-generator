import os
import sys
import shutil

from block_util import markdown_to_html_node
from inline_util import extract_title


def copy(source, destination):
	'''
	copies all the contents from a source directory to a destination directory (in our case, static to public)
	'''
	if not os.path.isdir(source):
		print('source is not a directory')
		return

	# delete all files in detination
	if os.path.exists(destination):
		for filename in os.listdir(destination):
			file_path = os.path.join(destination, filename)
			if os.path.isdir(file_path):
				shutil.rmtree(file_path)
			else:
				os.remove(file_path)
			print(f"Path '{file_path}' deleted.")
	# copy all files and subdirectories, nested files...
	for root, _, files in os.walk(source):
		# figure out where to put the copied items under destination
		relative_path = os.path.relpath(root, source)
		destination_root = (
			os.path.join(destination, relative_path)
			if relative_path != '.'
			else destination
		)
		os.makedirs(destination_root, exist_ok=True)

		for file_name in files:
			source_path = os.path.join(root, file_name)
			destination_path = os.path.join(destination_root, file_name)
			shutil.copy2(source_path, destination_path)
			# logging the path of each file copied for debugging
			print(f"Copied '{source_path}' to '{destination_path}'")
	return


def normalize_base_url(base_url):
	if not base_url:
		return '/'
	if not base_url.endswith('/'):
		base_url += '/'
	return base_url


def generate_page(base_url, from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path, "r", encoding="utf-8") as source_file:
		markdown_content = source_file.read()
	with open(template_path, "r", encoding="utf-8") as template_file:
		template_content = template_file.read()

	html_string = markdown_to_html_node(markdown_content).to_html()
	title = extract_title(markdown_content)
	output = (
		template_content
		.replace("{{ Title }}", title)
		.replace("{{ Content }}", html_string)
		.replace('href="/', f'href="{base_url}')
		.replace('src="/', f'src="{base_url}')
	)

	dest_dir = os.path.dirname(dest_path)
	if dest_dir:
		os.makedirs(dest_dir, exist_ok=True)
	with open(dest_path, "w", encoding="utf-8") as dest_file:
		dest_file.write(output)


def generate_pages_recursive(base_url, content_dir, template_path, dest_dir):
	if not os.path.isdir(content_dir):
		print(f"Content directory '{content_dir}' does not exist.")
		return
	for root, _, files in os.walk(content_dir):
		relative_root = os.path.relpath(root, content_dir)
		for file_name in files:
			if not file_name.lower().endswith(".md"):
				continue
			source_path = os.path.join(root, file_name)
			destination_root = dest_dir if relative_root == "." else os.path.join(dest_dir, relative_root)
			destination_name = os.path.splitext(file_name)[0] + ".html"
			destination_path = os.path.join(destination_root, destination_name)
			generate_page(base_url, source_path, template_path, destination_path)


def main():
	if len(sys.argv) > 1:
		base_path = os.path.abspath(sys.argv[1])
		base_url = normalize_base_url(sys.argv[2] if len(sys.argv) > 2 else '/')
	else:
		# default to the project root (parent directory of this file's folder)
		base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
		base_url = normalize_base_url('/')
	static_path = os.path.join(base_path, 'static')
	docs_path = os.path.join(base_path, 'docs')
	content_path = os.path.join(base_path, 'content')
	template_path = os.path.join(base_path, 'template.html')
	copy(static_path, docs_path)
	generate_pages_recursive(base_url, content_path, template_path, docs_path)


if __name__ == '__main__':
	main()
