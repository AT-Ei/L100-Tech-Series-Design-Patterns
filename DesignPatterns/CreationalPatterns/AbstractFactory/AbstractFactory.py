from abc import ABC, abstractmethod
from typing import Protocol

# Abstract Products
class Button(ABC):
    """Abstract base class for buttons"""
    @abstractmethod
    def paint(self) -> None:
        """Render the button"""
        pass
    
    @abstractmethod
    def click(self) -> None:
        """Handle button click"""
        pass

class Checkbox(ABC):
    """Abstract base class for checkboxes"""
    @abstractmethod
    def paint(self) -> None:
        """Render the checkbox"""
        pass
    
    @abstractmethod
    def toggle(self) -> None:
        """Toggle checkbox state"""
        pass

# Concrete Products for Windows
class WindowsButton(Button):
    """Windows-style button implementation"""
    def paint(self) -> None:
        print("Rendering Windows button with square corners")
    
    def click(self) -> None:
        print("Windows button clicked - Standard Windows sound")

class WindowsCheckbox(Checkbox):
    """Windows-style checkbox implementation"""
    def __init__(self):
        self._checked = False
    
    def paint(self) -> None:
        state = "checked" if self._checked else "unchecked"
        print(f"Rendering Windows checkbox - {state}")
    
    def toggle(self) -> None:
        self._checked = not self._checked
        state = "checked" if self._checked else "unchecked"
        print(f"Windows checkbox toggled - now {state}")

# Concrete Products for macOS
class MacOSButton(Button):
    """macOS-style button implementation"""
    def paint(self) -> None:
        print("Rendering macOS button with rounded corners")
    
    def click(self) -> None:
        print("macOS button clicked - Subtle macOS sound")

class MacOSCheckbox(Checkbox):
    """macOS-style checkbox implementation"""
    def __init__(self):
        self._checked = False
    
    def paint(self) -> None:
        state = "checked" if self._checked else "unchecked"
        print(f"Rendering macOS checkbox - {state}")
    
    def toggle(self) -> None:
        self._checked = not self._checked
        state = "checked" if self._checked else "unchecked"
        print(f"macOS checkbox toggled - now {state}")

# Abstract Factory
class GUIFactory(ABC):
    """Abstract factory for creating GUI components"""
    @abstractmethod
    def create_button(self) -> Button:
        """Create a button"""
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a checkbox"""
        pass

# Concrete Factories
class WindowsFactory(GUIFactory):
    """Factory for Windows GUI components"""
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacOSFactory(GUIFactory):
    """Factory for macOS GUI components"""
    def create_button(self) -> Button:
        return MacOSButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()

# Client
class Application:
    """Client that uses GUI components"""
    def __init__(self, factory: GUIFactory):
        self._factory = factory
        self._button = None
        self._checkbox = None
    
    def create_ui(self) -> None:
        """Create UI components using the factory"""
        self._button = self._factory.create_button()
        self._checkbox = self._factory.create_checkbox()
    
    def paint_ui(self) -> None:
        """Render the UI components"""
        print("\nPainting UI:")
        self._button.paint()
        self._checkbox.paint()
    
    def interact(self) -> None:
        """Simulate user interaction"""
        print("\nUser interaction:")
        self._button.click()
        self._checkbox.toggle()
        self._checkbox.toggle()

# Factory Provider
class GUIFactoryProvider:
    """Provides the appropriate factory based on OS"""
    @staticmethod
    def get_factory(os_name: str) -> GUIFactory:
        """Get factory for the specified OS"""
        if os_name.lower() == "windows":
            return WindowsFactory()
        elif os_name.lower() == "macos":
            return MacOSFactory()
        else:
            raise ValueError(f"Unsupported OS: {os_name}")

# Demonstration
def main():
    # Configure the application for Windows
    print("=== Windows Application ===")
    windows_factory = GUIFactoryProvider.get_factory("windows")
    windows_app = Application(windows_factory)
    windows_app.create_ui()
    windows_app.paint_ui()
    windows_app.interact()
    
    # Configure the application for macOS
    print("\n=== macOS Application ===")
    macos_factory = GUIFactoryProvider.get_factory("macos")
    macos_app = Application(macos_factory)
    macos_app.create_ui()
    macos_app.paint_ui()
    macos_app.interact()
    
    # Demonstrate runtime factory switching
    print("\n=== Runtime Factory Switching ===")
    # Start with Windows
    app = Application(windows_factory)
    app.create_ui()
    print("Initial UI (Windows):")
    app.paint_ui()
    
    # Switch to macOS
    app._factory = macos_factory
    app.create_ui()
    print("Switched UI (macOS):")
    app.paint_ui()
    
    # Try to get factory for unsupported OS
    print("\n=== Unsupported OS ===")
    try:
        linux_factory = GUIFactoryProvider.get_factory("linux")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()