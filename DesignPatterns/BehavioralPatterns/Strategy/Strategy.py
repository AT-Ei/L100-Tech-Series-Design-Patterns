from abc import ABC, abstractmethod
from typing import List, Dict
import math

# Strategy Interface
class RouteStrategy(ABC):
    """Abstract base class for routing strategies"""
    @abstractmethod
    def build_route(self, start: str, end: str) -> List[str]:
        """Build a route from start to end"""
        pass
    
    @abstractmethod
    def estimate_time(self, distance: float) -> float:
        """Estimate travel time based on distance"""
        pass

# Concrete Strategies
class DrivingStrategy(RouteStrategy):
    """Strategy for driving routes"""
    def build_route(self, start: str, end: str) -> List[str]:
        # Simplified route building for demonstration
        print(f"Building driving route from {start} to {end}")
        return [start, "Highway A", "Highway B", end]
    
    def estimate_time(self, distance: float) -> float:
        # Average driving speed: 60 km/h
        return distance / 60

class WalkingStrategy(RouteStrategy):
    """Strategy for walking routes"""
    def build_route(self, start: str, end: str) -> List[str]:
        # Simplified route building for demonstration
        print(f"Building walking route from {start} to {end}")
        return [start, "Park Path", "Pedestrian Bridge", end]
    
    def estimate_time(self, distance: float) -> float:
        # Average walking speed: 5 km/h
        return distance / 5

class CyclingStrategy(RouteStrategy):
    """Strategy for cycling routes"""
    def build_route(self, start: str, end: str) -> List[str]:
        # Simplified route building for demonstration
        print(f"Building cycling route from {start} to {end}")
        return [start, "Bike Lane", "Cycle Path", end]
    
    def estimate_time(self, distance: float) -> float:
        # Average cycling speed: 15 km/h
        return distance / 15

class PublicTransportStrategy(RouteStrategy):
    """Strategy for public transport routes"""
    def build_route(self, start: str, end: str) -> List[str]:
        # Simplified route building for demonstration
        print(f"Building public transport route from {start} to {end}")
        return [start, "Bus Stop 1", "Metro Station", "Bus Stop 2", end]
    
    def estimate_time(self, distance: float) -> float:
        # Average public transport speed: 30 km/h (including waiting time)
        return distance / 30

# Context Class
class Navigator:
    """Context that uses a routing strategy"""
    def __init__(self, strategy: RouteStrategy):
        self._strategy = strategy
        self._distances: Dict[str, float] = {
            ("Home", "Work"): 15.0,
            ("Home", "Gym"): 5.0,
            ("Work", "Gym"): 10.0,
            ("Home", "Airport"): 30.0,
        }
    
    def set_strategy(self, strategy: RouteStrategy) -> None:
        """Change the routing strategy"""
        print(f"Switching to {strategy.__class__.__name__}")
        self._strategy = strategy
    
    def calculate_route(self, start: str, end: str) -> None:
        """Calculate route using current strategy"""
        print(f"\nCalculating route from {start} to {end}")
        
        # Get distance
        distance = self._distances.get((start, end), 0.0)
        if distance == 0.0:
            print("No distance data available for this route")
            return
        
        # Build route using strategy
        route = self._strategy.build_route(start, end)
        
        # Estimate time using strategy
        time = self._strategy.estimate_time(distance)
        
        # Display results
        print(f"Route: {' -> '.join(route)}")
        print(f"Distance: {distance} km")
        print(f"Estimated time: {time:.1f} hours ({time*60:.0f} minutes)")
    
    def get_distance(self, start: str, end: str) -> float:
        """Helper method to get distance between two points"""
        return self._distances.get((start, end), 0.0)

# Client
def main():
    # Create navigator with default strategy
    navigator = Navigator(DrivingStrategy())
    
    # Test different routes with driving strategy
    print("=== Using Driving Strategy ===")
    navigator.calculate_route("Home", "Work")
    navigator.calculate_route("Home", "Gym")
    
    # Switch to walking strategy
    print("\n=== Switching to Walking Strategy ===")
    navigator.set_strategy(WalkingStrategy())
    navigator.calculate_route("Home", "Work")
    navigator.calculate_route("Home", "Gym")
    
    # Switch to cycling strategy
    print("\n=== Switching to Cycling Strategy ===")
    navigator.set_strategy(CyclingStrategy())
    navigator.calculate_route("Home", "Work")
    navigator.calculate_route("Work", "Gym")
    
    # Switch to public transport strategy
    print("\n=== Switching to Public Transport Strategy ===")
    navigator.set_strategy(PublicTransportStrategy())
    navigator.calculate_route("Home", "Airport")
    
    # Demonstrate runtime strategy selection
    print("\n=== Runtime Strategy Selection ===")
    strategies = {
        "driving": DrivingStrategy(),
        "walking": WalkingStrategy(),
        "cycling": CyclingStrategy(),
        "public": PublicTransportStrategy()
    }
    
    for strategy_name, strategy in strategies.items():
        print(f"\n--- Using {strategy_name.title()} Strategy ---")
        navigator.set_strategy(strategy)
        navigator.calculate_route("Home", "Work")
    
    # Compare strategies for the same route
    print("\n=== Strategy Comparison for Home to Work ===")
    start, end = "Home", "Work"
    distance = navigator.get_distance(start, end)
    
    for strategy_name, strategy in strategies.items():
        time = strategy.estimate_time(distance)
        print(f"{strategy_name.title()}: {time*60:.0f} minutes")

if __name__ == "__main__":
    main()