class Rectangle: 
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
    
    def area(self):
            return (self.max_x - self.min_x) * (self.max_y - self.min_y)
    
    def intersects(self, other):
        return (self.min_x <= other.max_x and self.max_x >= other.min_x and
                self.min_y <= other.max_y and self.max_y >= other.min_y)
    
    def contains_point(self, x, y):
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y)
    
    def enlarge(self, other): 
        return Rectangle(
            min(self.min_x, other.min_x),
            min(self.min_y, other.min_y),
            max(self.max_x, other.max_x),
            max(self.max_y, other.max_y)
        )
    
    def __str__(self):
        return f"Rectangle({self.min_x:.6f}, {self.min_y:.6f}, {self.max_x:.6f}, {self.max_y:.6f})"
