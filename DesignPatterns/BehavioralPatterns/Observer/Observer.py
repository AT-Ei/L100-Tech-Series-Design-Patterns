from abc import ABC, abstractmethod
from typing import List
import random

# Subject Interface
class Subject(ABC):
    """Abstract base class for subjects (observable objects)"""
    @abstractmethod
    def register_observer(self, observer: 'Observer') -> None:
        """Register an observer to receive updates"""
        pass
    
    @abstractmethod
    def remove_observer(self, observer: 'Observer') -> None:
        """Remove an observer from receiving updates"""
        pass
    
    @abstractmethod
    def notify_observers(self) -> None:
        """Notify all registered observers of state changes"""
        pass

# Observer Interface
class Observer(ABC):
    """Abstract base class for observers"""
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        """Update observer with new weather data"""
        pass

# Display Element Interface (for consistency)
class DisplayElement(ABC):
    """Abstract base class for display elements"""
    @abstractmethod
    def display(self) -> None:
        """Display the current state"""
        pass

# Concrete Subject
class WeatherStation(Subject):
    """Weather station that tracks weather data"""
    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0
    
    def register_observer(self, observer: Observer) -> None:
        """Add an observer to the list"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Registered new observer: {observer.__class__.__name__}")
    
    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the list"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Removed observer: {observer.__class__.__name__}")
    
    def notify_observers(self) -> None:
        """Notify all observers of weather changes"""
        print(f"\nNotifying {len(self._observers)} observers of weather change...")
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)
    
    def measurements_changed(self) -> None:
        """Called when weather measurements change"""
        self.notify_observers()
    
    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        """Update weather measurements and notify observers"""
        print(f"\nWeather update: {temperature}°C, {humidity}% humidity, {pressure} hPa")
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.measurements_changed()
    
    def get_temperature(self) -> float:
        return self._temperature
    
    def get_humidity(self) -> float:
        return self._humidity
    
    def get_pressure(self) -> float:
        return self._pressure

# Concrete Observers
class CurrentConditionsDisplay(Observer, DisplayElement):
    """Displays current weather conditions"""
    def __init__(self, weather_station: WeatherStation):
        self._temperature = 0.0
        self._humidity = 0.0
        weather_station.register_observer(self)
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        self._temperature = temperature
        self._humidity = humidity
        self.display()
    
    def display(self) -> None:
        print(f"Current conditions: {self._temperature}°C and {self._humidity}% humidity")

class StatisticsDisplay(Observer, DisplayElement):
    """Displays weather statistics"""
    def __init__(self, weather_station: WeatherStation):
        self._temperatures: List[float] = []
        self._humidities: List[float] = []
        self._pressures: List[float] = []
        weather_station.register_observer(self)
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        self._temperatures.append(temperature)
        self._humidities.append(humidity)
        self._pressures.append(pressure)
        self.display()
    
    def display(self) -> None:
        if not self._temperatures:
            print("No weather data available for statistics")
            return
        
        avg_temp = sum(self._temperatures) / len(self._temperatures)
        max_temp = max(self._temperatures)
        min_temp = min(self._temperatures)
        
        avg_humidity = sum(self._humidities) / len(self._humidities)
        
        print(f"Weather statistics:")
        print(f"  Temperature: avg={avg_temp:.1f}°C, max={max_temp}°C, min={min_temp}°C")
        print(f"  Humidity: avg={avg_humidity:.1f}%")

class ForecastDisplay(Observer, DisplayElement):
    """Displays weather forecast based on pressure changes"""
    def __init__(self, weather_station: WeatherStation):
        self._current_pressure = 0.0
        self._last_pressure = 0.0
        weather_station.register_observer(self)
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        self._last_pressure = self._current_pressure
        self._current_pressure = pressure
        self.display()
    
    def display(self) -> None:
        if self._current_pressure > self._last_pressure:
            forecast = "Improving weather on the way!"
        elif self._current_pressure == self._last_pressure:
            forecast = "More of the same"
        else:
            forecast = "Watch out for cooler, rainy weather"
        
        print(f"Forecast: {forecast}")

# Client
def main():
    # Create weather station (subject)
    weather_station = WeatherStation()
    
    # Create displays (observers) and register them
    current_display = CurrentConditionsDisplay(weather_station)
    stats_display = StatisticsDisplay(weather_station)
    forecast_display = ForecastDisplay(weather_station)
    
    # Simulate weather changes
    print("\n=== Initial Weather Update ===")
    weather_station.set_measurements(25.0, 65.0, 1013.0)
    
    print("\n=== Second Weather Update ===")
    weather_station.set_measurements(26.5, 70.0, 1015.0)
    
    print("\n=== Third Weather Update ===")
    weather_station.set_measurements(24.0, 90.0, 1008.0)
    
    # Demonstrate removing an observer
    print("\n=== Removing Statistics Display ===")
    weather_station.remove_observer(stats_display)
    
    print("\n=== Fourth Weather Update (without statistics) ===")
    weather_station.set_measurements(23.0, 85.0, 1010.0)
    
    # Demonstrate adding an observer back
    print("\n=== Re-adding Statistics Display ===")
    weather_station.register_observer(stats_display)
    
    print("\n=== Fifth Weather Update ===")
    weather_station.set_measurements(22.0, 80.0, 1012.0)
    
    # Simulate random weather changes
    print("\n=== Simulating Random Weather Changes ===")
    for i in range(3):
        temp = random.uniform(15.0, 30.0)
        humidity = random.uniform(40.0, 90.0)
        pressure = random.uniform(1000.0, 1020.0)
        weather_station.set_measurements(temp, humidity, pressure)

if __name__ == "__main__":
    main()