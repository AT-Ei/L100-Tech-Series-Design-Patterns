from abc import ABC, abstractmethod
from typing import List

# Component Interface
class FileSystemComponent(ABC):
    """Abstract base class for all file system components"""
    @abstractmethod
    def display(self, indent=0):
        """Display component with proper indentation"""
        pass
    
    @abstractmethod
    def size(self):
        """Calculate total size of the component"""
        pass

# Leaf Class
class File(FileSystemComponent):
    """Represents a file in the file system (leaf node)"""
    def __init__(self, name, size_kb):
        self.name = name
        self.size_kb = size_kb
    
    def display(self, indent=0):
        print("  " * indent + f"📄 {self.name} ({self.size_kb}KB)")
    
    def size(self):
        return self.size_kb

# Composite Class
class Directory(FileSystemComponent):
    """Represents a directory that can contain files and other directories"""
    def __init__(self, name):
        self.name = name
        self._children: List[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent):
        """Add a component to the directory"""
        self._children.append(component)
    
    def remove(self, component: FileSystemComponent):
        """Remove a component from the directory"""
        self._children.remove(component)
    
    def display(self, indent=0):
        print("  " * indent + f"📁 {self.name}/")
        for child in self._children:
            child.display(indent + 1)
    
    def size(self):
        """Calculate total size of all components in this directory"""
        total_size = 0
        for child in self._children:
            total_size += child.size()
        return total_size

# Demonstration
if __name__ == "__main__":
    # Create files (leaf nodes)
    resume = File("Resume.pdf", 250)
    photo = File("Vacation.jpg", 4200)
    readme = File("README.md", 15)
    script = File("deploy.py", 85)
    
    # Create directories (composite nodes)
    docs = Directory("Documents")
    media = Directory("Media")
    projects = Directory("Projects")
    root = Directory("Home")
    
    # Build file system structure
    docs.add(resume)
    media.add(photo)
    projects.add(readme)
    projects.add(script)
    
    root.add(docs)
    root.add(media)
    root.add(projects)
    
    # Add a subdirectory
    archive = Directory("Archive")
    archive.add(File("OldReport.docx", 750))
    docs.add(archive)
    
    # Display the entire file system
    print("=== File System Structure ===")
    root.display()
    
    # Calculate and display sizes
    print("\n=== Size Calculations ===")
    print(f"Size of 'Resume.pdf': {resume.size()}KB")
    print(f"Size of 'Media' directory: {media.size()}KB")
    print(f"Size of 'Projects' directory: {projects.size()}KB")
    print(f"Size of 'Documents' directory: {docs.size()}KB")
    print(f"Size of 'Home' directory: {root.size()}KB")
    
    # Demonstrate removal
    print("\n=== Removing 'Vacation.jpg' ===")
    media.remove(photo)
    print("Updated Media directory:")
    media.display()
    print(f"New size of 'Media' directory: {media.size()}KB")