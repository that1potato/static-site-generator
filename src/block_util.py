'''
Block-level markdown is the separation of different sections of an entire document. This assumes blocks are separated by a single blank line.
'''
def markdown_to_blocks(markdown):
	'''
	takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings.
	'''
	blocks = markdown.split('\n\n') 	# split by double new line
	for b in blocks:
		b = b.strip()	# remove leading or trailing whitespace
	return blocks
