class Shape:
    def __init__(self, shape):
        self.shape = shape

    def shape_str(self):
        """
        String representation of shape index
        """
        str_map = ["triangle", "square", "circle"]
        return str_map[self.shape-1]

    def shape_marker(self):
        """
        Create marker for matplotlib view
        """
        markers = ["^", ",", "o"]
        return markers[self.shape-1]
