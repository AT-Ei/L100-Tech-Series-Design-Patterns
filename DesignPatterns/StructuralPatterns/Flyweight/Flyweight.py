from typing import Dict, Tuple

# Flyweight Class
class CharacterFormat:
    """Shared intrinsic state (formatting attributes)"""
    def __init__(self, font: str, size: int, color: str):
        self.font = font
        self.size = size
        self.color = color
    
    def __repr__(self):
        return f"Format({self.font}, {self.size}pt, {self.color})"

# Flyweight Factory
class CharacterFormatFactory:
    """Creates and manages shared CharacterFormat objects"""
    _formats: Dict[Tuple[str, int, str], CharacterFormat] = {}
    
    @classmethod
    def get_format(cls, font: str, size: int, color: str) -> CharacterFormat:
        key = (font, size, color)
        if key not in cls._formats:
            cls._formats[key] = CharacterFormat(font, size, color)
            print(f"Created new format: {cls._formats[key]}")
        else:
            print(f"Reusing existing format: {cls._formats[key]}")
        return cls._formats[key]
    
    @classmethod
    def get_total_formats(cls) -> int:
        return len(cls._formats)

# Context Class
class Character:
    """Contains extrinsic state (position) and reference to flyweight"""
    def __init__(self, char: str, x: int, y: int, format: CharacterFormat):
        self.char = char
        self.x = x
        self.y = y
        self.format = format  # Reference to shared flyweight
    
    def display(self):
        print(f"'{self.char}' at ({self.x},{self.y}) {self.format}")

# Client
class Document:
    """Manages characters and demonstrates flyweight usage"""
    def __init__(self):
        self.characters = []
    
    def add_character(self, char: str, x: int, y: int, font: str, size: int, color: str):
        """Add character with shared formatting"""
        format = CharacterFormatFactory.get_format(font, size, color)
        character = Character(char, x, y, format)
        self.characters.append(character)
    
    def display(self):
        """Display all characters in the document"""
        print("\n=== Document Content ===")
        for char in self.characters:
            char.display()
        print(f"\nTotal characters: {len(self.characters)}")
        print(f"Total unique formats: {CharacterFormatFactory.get_total_formats()}")

# Demonstration
if __name__ == "__main__":
    # Create a document
    doc = Document()
    
    # Add characters with various formatting
    # Note: Many characters share the same formatting
    doc.add_character('H', 0, 0, "Arial", 12, "black")
    doc.add_character('e', 1, 0, "Arial", 12, "black")
    doc.add_character('l', 2, 0, "Arial", 12, "black")
    doc.add_character('l', 3, 0, "Arial", 12, "black")
    doc.add_character('o', 4, 0, "Arial", 12, "black")
    
    # Different formatting for next word
    doc.add_character('W', 0, 1, "Times New Roman", 14, "blue")
    doc.add_character('o', 1, 1, "Times New Roman", 14, "blue")
    doc.add_character('r', 2, 1, "Times New Roman", 14, "blue")
    doc.add_character('l', 3, 1, "Times New Roman", 14, "blue")
    doc.add_character('d', 4, 1, "Times New Roman", 14, "blue")
    
    # Reuse first formatting
    doc.add_character('!', 5, 0, "Arial", 12, "black")
    
    # Another different format
    doc.add_character('@', 5, 1, "Courier", 10, "red")
    
    # Display the document
    doc.display()
    
    # Show memory efficiency
    print("\n=== Memory Efficiency Analysis ===")
    print("Without flyweight: 12 characters × 3 format attributes = 36 objects")
    print(f"With flyweight: {len(doc.characters)} characters + {CharacterFormatFactory.get_total_formats()} formats = {len(doc.characters) + CharacterFormatFactory.get_total_formats()} objects")
    print(f"Memory saved: {36 - (len(doc.characters) + CharacterFormatFactory.get_total_formats())} objects")