'''
Block-level markdown is the separation of different sections of an entire document. This assumes blocks are separated by a single blank line.
'''


def markdown_to_blocks(markdown):
    '''
    takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings.
    Separation is strictly by exactly two newlines ("\n\n").
    '''
    if markdown is None:
        return []
    text = markdown.strip()
    if not text:
        return []
    parts = text.split("\n\n")
    blocks = [p.strip() for p in parts if p.strip()]
    return blocks
