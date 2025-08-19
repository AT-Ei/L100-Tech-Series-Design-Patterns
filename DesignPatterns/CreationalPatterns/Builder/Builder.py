from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum

# Enum for meal types
class MealType(Enum):
    VEGETARIAN = "Vegetarian"
    NON_VEGETARIAN = "Non-Vegetarian"

# Packing interface
class Packing(ABC):
    """Abstract base class for food packaging"""
    @abstractmethod
    def pack(self) -> str:
        """Return the packaging type"""
        pass

# Concrete packings
class Wrapper(Packing):
    """Wrapper packaging for burgers"""
    def pack(self) -> str:
        return "Wrapper"

class Bottle(Packing):
    """Bottle packaging for drinks"""
    def pack(self) -> str:
        return "Bottle"

# Item interface
class Item(ABC):
    """Abstract base class for meal items"""
    @abstractmethod
    def name(self) -> str:
        """Return the item name"""
        pass
    
    @abstractmethod
    def packing(self) -> Packing:
        """Return the item packaging"""
        pass
    
    @abstractmethod
    def price(self) -> float:
        """Return the item price"""
        pass

# Concrete items
class VegBurger(Item):
    """Vegetarian burger"""
    def name(self) -> str:
        return "Veg Burger"
    
    def packing(self) -> Packing:
        return Wrapper()
    
    def price(self) -> float:
        return 2.50

class ChickenBurger(Item):
    """Chicken burger"""
    def name(self) -> str:
        return "Chicken Burger"
    
    def packing(self) -> Packing:
        return Wrapper()
    
    def price(self) -> float:
        return 3.50

class Coke(Item):
    """Coca-Cola drink"""
    def name(self) -> str:
        return "Coke"
    
    def packing(self) -> Packing:
        return Bottle()
    
    def price(self) -> float:
        return 1.50

class Pepsi(Item):
    """Pepsi drink"""
    def name(self) -> str:
        return "Pepsi"
    
    def packing(self) -> Packing:
        return Bottle()
    
    def price(self) -> float:
        return 1.50

# Complex object being built
class Meal:
    """Represents a meal with multiple items"""
    def __init__(self):
        self.items: List[Item] = []
        self.meal_type: MealType = None
    
    def add_item(self, item: Item) -> None:
        """Add an item to the meal"""
        self.items.append(item)
    
    def set_meal_type(self, meal_type: MealType) -> None:
        """Set the meal type"""
        self.meal_type = meal_type
    
    def get_cost(self) -> float:
        """Calculate total cost of the meal"""
        return sum(item.price() for item in self.items)
    
    def show_items(self) -> None:
        """Display all items in the meal"""
        print(f"\n{self.meal_type.value} Meal")
        print("Items:")
        for item in self.items:
            print(f"  {item.name()}, {item.packing().pack()}, Price: ${item.price():.2f}")
        print(f"Total Cost: ${self.get_cost():.2f}")

# Builder interface
class MealBuilder(ABC):
    """Abstract base class for meal builders"""
    @abstractmethod
    def prepare_meal(self) -> None:
        """Prepare the meal"""
        pass
    
    @abstractmethod
    def add_burger(self) -> None:
        """Add a burger to the meal"""
        pass
    
    @abstractmethod
    def add_drink(self) -> None:
        """Add a drink to the meal"""
        pass
    
    @abstractmethod
    def add_sides(self) -> None:
        """Add sides to the meal"""
        pass
    
    @abstractmethod
    def get_meal(self) -> Meal:
        """Get the constructed meal"""
        pass

# Concrete builders
class VegMealBuilder(MealBuilder):
    """Builder for vegetarian meals"""
    def __init__(self):
        self.meal = Meal()
    
    def prepare_meal(self) -> None:
        self.meal.set_meal_type(MealType.VEGETARIAN)
        print("Preparing vegetarian meal...")
    
    def add_burger(self) -> None:
        self.meal.add_item(VegBurger())
        print("Added Veg Burger")
    
    def add_drink(self) -> None:
        self.meal.add_item(Coke())
        print("Added Coke")
    
    def add_sides(self) -> None:
        # Vegetarian meal doesn't have sides in this example
        pass
    
    def get_meal(self) -> Meal:
        return self.meal

class NonVegMealBuilder(MealBuilder):
    """Builder for non-vegetarian meals"""
    def __init__(self):
        self.meal = Meal()
    
    def prepare_meal(self) -> None:
        self.meal.set_meal_type(MealType.NON_VEGETARIAN)
        print("Preparing non-vegetarian meal...")
    
    def add_burger(self) -> None:
        self.meal.add_item(ChickenBurger())
        print("Added Chicken Burger")
    
    def add_drink(self) -> None:
        self.meal.add_item(Pepsi())
        print("Added Pepsi")
    
    def add_sides(self) -> None:
        # Non-vegetarian meal includes an extra drink as a side
        self.meal.add_item(Coke())
        print("Added Coke as side")
    
    def get_meal(self) -> Meal:
        return self.meal

# Director
class MealDirector:
    """Director that constructs meals using builders"""
    def construct(self, builder: MealBuilder) -> Meal:
        """Construct a meal using the provided builder"""
        builder.prepare_meal()
        builder.add_burger()
        builder.add_drink()
        builder.add_sides()
        return builder.get_meal()

# Client
def main():
    # Create director
    director = MealDirector()
    
    # Build vegetarian meal
    print("=== Building Vegetarian Meal ===")
    veg_builder = VegMealBuilder()
    veg_meal = director.construct(veg_builder)
    veg_meal.show_items()
    
    # Build non-vegetarian meal
    print("\n=== Building Non-Vegetarian Meal ===")
    non_veg_builder = NonVegMealBuilder()
    non_veg_meal = director.construct(non_veg_builder)
    non_veg_meal.show_items()
    
    # Demonstrate custom meal construction
    print("\n=== Building Custom Meal ===")
    custom_builder = VegMealBuilder()
    custom_builder.prepare_meal()
    custom_builder.add_burger()
    custom_builder.add_drink()
    # Skip adding sides
    custom_meal = custom_builder.get_meal()
    custom_meal.show_items()
    
    # Demonstrate builder independence
    print("\n=== Builder Independence ===")
    # Create a non-vegetarian meal without sides
    custom_non_veg_builder = NonVegMealBuilder()
    custom_non_veg_builder.prepare_meal()
    custom_non_veg_builder.add_burger()
    custom_non_veg_builder.add_drink()
    # Skip sides
    custom_non_veg_meal = custom_non_veg_builder.get_meal()
    custom_non_veg_meal.show_items()

if __name__ == "__main__":
    main()