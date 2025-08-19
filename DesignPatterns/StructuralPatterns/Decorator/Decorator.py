from abc import ABC, abstractmethod

# Component Interface
class Beverage(ABC):
    """Abstract base class for all beverages"""
    @abstractmethod
    def get_description(self) -> str:
        """Return beverage description"""
        pass
    
    @abstractmethod
    def cost(self) -> float:
        """Calculate cost of the beverage"""
        pass

# Concrete Component
class SimpleCoffee(Beverage):
    """Basic coffee implementation"""
    def get_description(self) -> str:
        return "Simple Coffee"
    
    def cost(self) -> float:
        return 2.50

# Base Decorator
class BeverageDecorator(Beverage):
    """Base decorator class that implements Beverage interface"""
    def __init__(self, beverage: Beverage):
        self._beverage = beverage
    
    def get_description(self) -> str:
        return self._beverage.get_description()
    
    def cost(self) -> float:
        return self._beverage.cost()

# Concrete Decorators
class MilkDecorator(BeverageDecorator):
    """Adds milk to the coffee"""
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Milk"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.50

class SugarDecorator(BeverageDecorator):
    """Adds sugar to the coffee"""
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Sugar"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.20

class WhippedCreamDecorator(BeverageDecorator):
    """Adds whipped cream to the coffee"""
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Whipped Cream"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.70

class CaramelDecorator(BeverageDecorator):
    """Adds caramel to the coffee"""
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Caramel"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.60

# Demonstration
if __name__ == "__main__":
    # Order a simple coffee
    coffee = SimpleCoffee()
    print(f"Order: {coffee.get_description()}")
    print(f"Cost: ${coffee.cost():.2f}\n")
    
    # Add milk to the coffee
    coffee_with_milk = MilkDecorator(coffee)
    print(f"Order: {coffee_with_milk.get_description()}")
    print(f"Cost: ${coffee_with_milk.cost():.2f}\n")
    
    # Add sugar to the coffee with milk
    coffee_with_milk_sugar = SugarDecorator(coffee_with_milk)
    print(f"Order: {coffee_with_milk_sugar.get_description()}")
    print(f"Cost: ${coffee_with_milk_sugar.cost():.2f}\n")
    
    # Add whipped cream to the previous order
    coffee_with_milk_sugar_cream = WhippedCreamDecorator(coffee_with_milk_sugar)
    print(f"Order: {coffee_with_milk_sugar_cream.get_description()}")
    print(f"Cost: ${coffee_with_milk_sugar_cream.cost():.2f}\n")
    
    # Create a complex order with all condiments
    complex_order = CaramelDecorator(
        WhippedCreamDecorator(
            SugarDecorator(
                MilkDecorator(SimpleCoffee())
            )
        )
    )
    print(f"Complex Order: {complex_order.get_description()}")
    print(f"Cost: ${complex_order.cost():.2f}\n")
    
    # Demonstrate that decorators can be added in any order
    another_order = SugarDecorator(
        CaramelDecorator(
            MilkDecorator(SimpleCoffee())
        )
    )
    print(f"Another Order: {another_order.get_description()}")
    print(f"Cost: ${another_order.cost():.2f}")