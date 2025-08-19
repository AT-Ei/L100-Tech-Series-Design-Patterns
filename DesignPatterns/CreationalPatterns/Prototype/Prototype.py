import copy
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import math

# Prototype Interface
class Shape(ABC):
    """Abstract base class for all shapes"""
    def __init__(self, x: float, y: float, color: str):
        self.x = x
        self.y = y
        self.color = color
    
    @abstractmethod
    def clone(self) -> 'Shape':
        """Clone the shape"""
        pass
    
    @abstractmethod
    def area(self) -> float:
        """Calculate area of the shape"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} at ({self.x}, {self.y}) with color {self.color}"

# Concrete Prototypes
class Circle(Shape):
    """Circle shape prototype"""
    def __init__(self, x: float, y: float, color: str, radius: float):
        super().__init__(x, y, color)
        self.radius = radius
    
    def clone(self) -> 'Circle':
        # Create a shallow copy
        return copy.copy(self)
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def __str__(self) -> str:
        return super().__str__() + f", radius {self.radius}"

class Rectangle(Shape):
    """Rectangle shape prototype"""
    def __init__(self, x: float, y: float, color: str, width: float, height: float):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
    
    def clone(self) -> 'Rectangle':
        # Create a shallow copy
        return copy.copy(self)
    
    def area(self) -> float:
        return self.width * self.height
    
    def __str__(self) -> str:
        return super().__str__() + f", width {self.width}, height {self.height}"

class Triangle(Shape):
    """Triangle shape prototype"""
    def __init__(self, x: float, y: float, color: str, base: float, height: float):
        super().__init__(x, y, color)
        self.base = base
        self.height = height
    
    def clone(self) -> 'Triangle':
        # Create a shallow copy
        return copy.copy(self)
    
    def area(self) -> float:
        return 0.5 * self.base * self.height
    
    def __str__(self) -> str:
        return super().__str__() + f", base {self.base}, height {self.height}"

# Prototype Registry
class ShapeRegistry:
    """Registry to store and retrieve shape prototypes"""
    def __init__(self):
        self._shapes: Dict[str, Shape] = {}
    
    def add_shape(self, name: str, shape: Shape) -> None:
        """Add a shape prototype to the registry"""
        self._shapes[name] = shape
        print(f"Added prototype: {name} -> {shape}")
    
    def get_shape(self, name: str) -> Shape:
        """Get a clone of a shape prototype"""
        if name not in self._shapes:
            raise ValueError(f"Shape prototype '{name}' not found")
        
        shape = self._shapes[name]
        cloned_shape = shape.clone()
        print(f"Cloned shape: {name} -> {cloned_shape}")
        return cloned_shape
    
    def list_shapes(self) -> None:
        """List all available shape prototypes"""
        print("\nAvailable shape prototypes:")
        for name, shape in self._shapes.items():
            print(f"  {name}: {shape}")

# Complex Prototype with Nested Objects
class ComplexShape(Shape):
    """Complex shape composed of other shapes"""
    def __init__(self, x: float, y: float, color: str, components: List[Shape]):
        super().__init__(x, y, color)
        self.components = components
    
    def clone(self) -> 'ComplexShape':
        # Create a deep copy to ensure components are also copied
        return copy.deepcopy(self)
    
    def area(self) -> float:
        return sum(component.area() for component in self.components)
    
    def __str__(self) -> str:
        components_str = ", ".join(str(comp) for comp in self.components)
        return super().__str__() + f", components: [{components_str}]"

# Client
def main():
    # Create a prototype registry
    registry = ShapeRegistry()
    
    # Create and register shape prototypes
    circle = Circle(10, 10, "red", 5)
    rectangle = Rectangle(20, 20, "blue", 10, 15)
    triangle = Triangle(30, 30, "green", 8, 12)
    
    registry.add_shape("circle", circle)
    registry.add_shape("rectangle", rectangle)
    registry.add_shape("triangle", triangle)
    
    # List available prototypes
    registry.list_shapes()
    
    # Clone shapes from the registry
    print("\n=== Cloning Shapes ===")
    
    # Clone a circle
    cloned_circle = registry.get_shape("circle")
    cloned_circle.x = 50  # Modify the clone
    cloned_circle.color = "yellow"
    print(f"Modified clone: {cloned_circle}")
    print(f"Original: {circle}")
    
    # Clone a rectangle
    cloned_rectangle = registry.get_shape("rectangle")
    cloned_rectangle.width = 20
    print(f"Modified clone: {cloned_rectangle}")
    print(f"Original: {rectangle}")
    
    # Clone a triangle
    cloned_triangle = registry.get_shape("triangle")
    cloned_triangle.base = 10
    print(f"Modified clone: {cloned_triangle}")
    print(f"Original: {triangle}")
    
    # Demonstrate complex shape cloning
    print("\n=== Complex Shape Cloning ===")
    
    # Create a complex shape
    components = [
        Circle(0, 0, "red", 3),
        Rectangle(5, 5, "blue", 4, 6),
        Triangle(10, 10, "green", 5, 8)
    ]
    complex_shape = ComplexShape(0, 0, "purple", components)
    registry.add_shape("complex", complex_shape)
    
    # Clone the complex shape
    cloned_complex = registry.get_shape("complex")
    
    # Modify a component in the clone
    cloned_complex.components[0].radius = 10
    cloned_complex.components[1].width = 20
    
    print("Original complex shape:")
    print(complex_shape)
    print("\nCloned complex shape (modified):")
    print(cloned_complex)
    
    # Verify the original is unchanged
    print("\nOriginal complex shape after clone modification:")
    print(complex_shape)
    
    # Demonstrate shallow vs deep copy
    print("\n=== Shallow vs Deep Copy ===")
    
    # Create a shape with mutable attribute
    original = Circle(0, 0, "red", 5)
    original.extra_info = {"created": "today", "version": 1}
    
    # Shallow copy
    shallow_copy = copy.copy(original)
    shallow_copy.extra_info["version"] = 2
    
    # Deep copy
    deep_copy = copy.deepcopy(original)
    deep_copy.extra_info["version"] = 3
    
    print(f"Original: {original.extra_info}")
    print(f"Shallow copy: {shallow_copy.extra_info}")
    print(f"Deep copy: {deep_copy.extra_info}")

if __name__ == "__main__":
    main()