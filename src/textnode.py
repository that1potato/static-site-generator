'''
All Markdown textnodes
'''
from enum import Enum

class TextType(Enum):
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, tn1, tn2):
        return tn1.text == tn2.text and tn1.text_type == tn2.text_type and tn1.url == tn2.url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
