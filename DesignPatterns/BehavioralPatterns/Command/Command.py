from abc import ABC, abstractmethod
from typing import List

# Command Interface
class Command(ABC):
    """Abstract base class for all commands"""
    @abstractmethod
    def execute(self) -> None:
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo the command"""
        pass

# Receiver Classes
class Light:
    """Receiver for light commands"""
    def __init__(self, location: str):
        self.location = location
        self._is_on = False
    
    def on(self) -> None:
        self._is_on = True
        print(f"{self.location} light is ON")
    
    def off(self) -> None:
        self._is_on = False
        print(f"{self.location} light is OFF")
    
    def is_on(self) -> bool:
        return self._is_on

class Thermostat:
    """Receiver for thermostat commands"""
    def __init__(self, location: str):
        self.location = location
        self._temperature = 20  # Default temperature
        self._previous_temperature = 20
    
    def set_temperature(self, temp: int) -> None:
        self._previous_temperature = self._temperature
        self._temperature = temp
        print(f"{self.location} thermostat set to {temp}°C")
    
    def get_temperature(self) -> int:
        return self._temperature
    
    def get_previous_temperature(self) -> int:
        return self._previous_temperature

# Concrete Commands
class LightOnCommand(Command):
    """Command to turn on a light"""
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.on()
    
    def undo(self) -> None:
        self.light.off()

class LightOffCommand(Command):
    """Command to turn off a light"""
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.off()
    
    def undo(self) -> None:
        self.light.on()

class ThermostatSetCommand(Command):
    """Command to set thermostat temperature"""
    def __init__(self, thermostat: Thermostat, temperature: int):
        self.thermostat = thermostat
        self.temperature = temperature
    
    def execute(self) -> None:
        self.thermostat.set_temperature(self.temperature)
    
    def undo(self) -> None:
        self.thermostat.set_temperature(self.thermostat.get_previous_temperature())

class NoCommand(Command):
    """Null object pattern for empty slots"""
    def execute(self) -> None:
        print("No command assigned")
    
    def undo(self) -> None:
        print("Nothing to undo")

# Invoker Class
class RemoteControl:
    """Invoker that executes commands"""
    def __init__(self):
        self._commands: List[Command] = [NoCommand()] * 7  # 7 slots
        self._undo_command: Command = NoCommand()
    
    def set_command(self, slot: int, command: Command) -> None:
        """Assign a command to a slot"""
        if 0 <= slot < len(self._commands):
            self._commands[slot] = command
    
    def button_pressed(self, slot: int) -> None:
        """Execute command assigned to a slot"""
        if 0 <= slot < len(self._commands):
            self._commands[slot].execute()
            self._undo_command = self._commands[slot]
    
    def undo_button_pressed(self) -> None:
        """Undo the last executed command"""
        print("Undoing last command...")
        self._undo_command.undo()

# Client
def main():
    # Create receivers
    living_room_light = Light("Living Room")
    kitchen_light = Light("Kitchen")
    bedroom_thermostat = Thermostat("Bedroom")
    
    # Create commands
    living_room_light_on = LightOnCommand(living_room_light)
    living_room_light_off = LightOffCommand(living_room_light)
    kitchen_light_on = LightOnCommand(kitchen_light)
    kitchen_light_off = LightOffCommand(kitchen_light)
    bedroom_thermostat_22 = ThermostatSetCommand(bedroom_thermostat, 22)
    bedroom_thermostat_18 = ThermostatSetCommand(bedroom_thermostat, 18)
    
    # Create remote control
    remote = RemoteControl()
    
    # Program the remote
    remote.set_command(0, living_room_light_on)
    remote.set_command(1, living_room_light_off)
    remote.set_command(2, kitchen_light_on)
    remote.set_command(3, kitchen_light_off)
    remote.set_command(4, bedroom_thermostat_22)
    remote.set_command(5, bedroom_thermostat_18)
    
    # Test the remote
    print("=== Testing Remote Control ===")
    remote.button_pressed(0)  # Living room light on
    remote.button_pressed(4)  # Bedroom thermostat to 22°C
    remote.button_pressed(2)  # Kitchen light on
    
    # Test undo functionality
    print("\n=== Testing Undo Functionality ===")
    remote.undo_button_pressed()  # Undo kitchen light on
    remote.undo_button_pressed()  # Undo thermostat to 22°C
    remote.undo_button_pressed()  # Undo living room light on
    
    # Test multiple undos
    print("\n=== Testing Multiple Commands and Undos ===")
    remote.button_pressed(0)  # Living room light on
    remote.button_pressed(5)  # Bedroom thermostat to 18°C
    remote.button_pressed(3)  # Kitchen light off
    
    # Undo all
    remote.undo_button_pressed()  # Undo kitchen light off
    remote.undo_button_pressed()  # Undo thermostat to 18°C
    remote.undo_button_pressed()  # Undo living room light on
    
    # Test unassigned slot
    print("\n=== Testing Unassigned Slot ===")
    remote.button_pressed(6)  # No command assigned

if __name__ == "__main__":
    main()