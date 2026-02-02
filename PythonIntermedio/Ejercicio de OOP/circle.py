class Circle: 
    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return 3.14 * (self.radius**2)
        
circle = Circle(5)
print(circle.get_area())