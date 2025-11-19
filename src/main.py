import os
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


def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path, "r", encoding="utf-8") as source_file:
		markdown_content = source_file.read()
	with open(template_path, "r", encoding="utf-8") as template_file:
		template_content = template_file.read()

	html_string = markdown_to_html_node(markdown_content).to_html()
	title = extract_title(markdown_content)
	output = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

	dest_dir = os.path.dirname(dest_path)
	if dest_dir:
		os.makedirs(dest_dir, exist_ok=True)
	with open(dest_path, "w", encoding="utf-8") as dest_file:
		dest_file.write(output)


def main():
	static_path = 'static'
	public_path = 'public'
	copy(static_path, public_path)

	from_path = 'content/index.md'
	template_path = 'template.html'
	dest_path = 'public/index.html'
	generate_page(from_path, template_path, dest_path)


if __name__ == '__main__':
	main()
