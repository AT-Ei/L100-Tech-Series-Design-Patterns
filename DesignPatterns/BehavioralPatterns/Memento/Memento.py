from typing import List
from datetime import datetime

# Memento Class
class TextEditorMemento:
    """Stores the state of the TextEditor"""
    def __init__(self, content: str, cursor_position: int):
        self._content = content
        self._cursor_position = cursor_position
        self._timestamp = datetime.now()
    
    def get_content(self) -> str:
        """Get the saved content"""
        return self._content
    
    def get_cursor_position(self) -> int:
        """Get the saved cursor position"""
        return self._cursor_position
    
    def get_timestamp(self) -> datetime:
        """Get when this state was saved"""
        return self._timestamp
    
    def __str__(self):
        return f"[{self._timestamp.strftime('%H:%M:%S')}] Content: '{self._content[:20]}...' Cursor: {self._cursor_position}"

# Originator Class
class TextEditor:
    """The originator that creates and restores mementos"""
    def __init__(self):
        self._content = ""
        self._cursor_position = 0
    
    def write(self, text: str) -> None:
        """Write text at current cursor position"""
        before = self._content[:self._cursor_position]
        after = self._content[self._cursor_position:]
        self._content = before + text + after
        self._cursor_position += len(text)
        print(f"Written: '{text}'")
        self._display_state()
    
    def move_cursor(self, position: int) -> None:
        """Move cursor to specific position"""
        if 0 <= position <= len(self._content):
            self._cursor_position = position
            print(f"Cursor moved to position {position}")
        else:
            print(f"Invalid cursor position: {position}")
    
    def delete(self, chars: int = 1) -> None:
        """Delete characters at cursor position"""
        if chars <= 0:
            return
        
        if self._cursor_position + chars > len(self._content):
            chars = len(self._content) - self._cursor_position
        
        before = self._content[:self._cursor_position]
        after = self._content[self._cursor_position + chars:]
        self._content = before + after
        print(f"Deleted {chars} character(s)")
        self._display_state()
    
    def save(self) -> TextEditorMemento:
        """Create a memento with current state"""
        return TextEditorMemento(self._content, self._cursor_position)
    
    def restore(self, memento: TextEditorMemento) -> None:
        """Restore state from memento"""
        self._content = memento.get_content()
        self._cursor_position = memento.get_cursor_position()
        print(f"Restored state from {memento.get_timestamp().strftime('%H:%M:%S')}")
        self._display_state()
    
    def _display_state(self) -> None:
        """Display current state"""
        cursor_indicator = " " * self._cursor_position + "^"
        print(f"Content: '{self._content}'")
        print(f"         {cursor_indicator}")
        print(f"Length: {len(self._content)}, Cursor: {self._cursor_position}\n")
    
    def __str__(self):
        return f"TextEditor with content: '{self._content}' (cursor at {self._cursor_position})"

# Caretaker Class
class History:
    """Manages mementos for the text editor"""
    def __init__(self, max_history: int = 5):
        self._history: List[TextEditorMemento] = []
        self._max_history = max_history
    
    def save(self, memento: TextEditorMemento) -> None:
        """Save a memento to history"""
        self._history.append(memento)
        if len(self._history) > self._max_history:
            self._history.pop(0)
        print(f"State saved to history (total: {len(self._history)})")
    
    def undo(self) -> TextEditorMemento:
        """Get the last saved memento"""
        if not self._history:
            raise ValueError("No history available")
        return self._history.pop()
    
    def list_history(self) -> None:
        """List all saved states"""
        print("\n=== History ===")
        for i, memento in enumerate(self._history, 1):
            print(f"{i}. {memento}")
        print("=============")

# Client
def main():
    # Create text editor and history
    editor = TextEditor()
    history = History(max_history=3)
    
    # Initial state
    print("=== Initial State ===")
    editor._display_state()
    
    # Save initial state
    history.save(editor.save())
    
    # Perform some operations
    print("=== Writing Text ===")
    editor.write("Hello, ")
    history.save(editor.save())
    
    editor.write("World!")
    history.save(editor.save())
    
    editor.move_cursor(7)
    editor.write("beautiful ")
    history.save(editor.save())
    
    # Show history
    history.list_history()
    
    # Undo operations
    print("\n=== Undoing Operations ===")
    try:
        editor.restore(history.undo())  # Undo last write
        editor.restore(history.undo())  # Undo previous write
        editor.restore(history.undo())  # Undo first write
    except ValueError as e:
        print(f"Error: {e}")
    
    # Try to undo beyond history
    try:
        editor.restore(history.undo())
    except ValueError as e:
        print(f"Error: {e}")
    
    # Perform more operations to test history limit
    print("\n=== Testing History Limit ===")
    editor.write("New text")
    history.save(editor.save())
    
    editor.write(" to test")
    history.save(editor.save())
    
    editor.write(" history limit")
    history.save(editor.save())
    
    # This should push out the oldest state
    editor.write(" and overflow")
    history.save(editor.save())
    
    history.list_history()
    
    # Restore to oldest state in history
    print("\n=== Restoring to Oldest State ===")
    oldest_memento = history._history[0]
    editor.restore(oldest_memento)

if __name__ == "__main__":
    main()