class HTMLNode:
    '''
    Nodes in an HTML document tree
    '''
    def __init__(self, tag=None, value=None, children=None, props=None):
        '''
        tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        value - A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        children - A list of HTMLNode objects representing the children of this node
        props - A dictionary of key-value pairs representing the attributes of the HTML tag.
        For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        '''
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ''
        
        output = ''
        for k, v in self.props.items():
            output += f' {k}=\"{v}\"'
        return output
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        '''
        leaf node cannot have children
        '''
        super().__init__(tag=tag, value=value, children=None, props=props)

    @property
    def children(self):
        return None

    @children.setter
    def children(self, value):
        # Allow None/empty but forbid any non-empty assignment
        if value not in (None, [], ()):  # treat empty sequences as None-equivalent
            raise AttributeError("LeafNode cannot have children")

    def to_html(self):
        if self.value is None:
            raise ValueError('LeafNode must have a value')
        if self.tag is None:
            return self.value   # return value as raw text if no tag
        
        return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    @property
    def props(self):
        return None

    @props.setter
    def props(self, value):
        # Allow None/empty but forbid any non-empty assignment
        if value not in (None, [], ()):  # treat empty sequences as None-equivalent
            raise AttributeError("ParentNode cannot have props")
    
    def to_html(self):
        if self.tag is None:
            raise ValueError('ParentNode must have a tag')
        if self.children is None or len(self.children) == 0:
            raise ValueError('ParentNode must have a child node')
        # Recursively render all children and wrap with this node's tag
        children_html = ''
        for c in self.children:
            children_html += c.to_html()
        return f'<{self.tag}{super().props_to_html()}>{children_html}</{self.tag}>'
