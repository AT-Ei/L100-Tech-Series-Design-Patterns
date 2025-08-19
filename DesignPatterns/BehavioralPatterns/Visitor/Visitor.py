from abc import ABC, abstractmethod
from typing import List

# Element Interface
class DocumentElement(ABC):
    """Abstract base class for document elements"""
    @abstractmethod
    def accept(self, visitor: 'DocumentVisitor') -> None:
        """Accept a visitor"""
        pass

# Concrete Elements
class Paragraph(DocumentElement):
    """Represents a paragraph element"""
    def __init__(self, text: str):
        self.text = text
    
    def accept(self, visitor: 'DocumentVisitor') -> None:
        visitor.visit_paragraph(self)
    
    def __str__(self) -> str:
        return f"Paragraph: {self.text[:30]}..."

class Image(DocumentElement):
    """Represents an image element"""
    def __init__(self, src: str, alt: str = ""):
        self.src = src
        self.alt = alt
    
    def accept(self, visitor: 'DocumentVisitor') -> None:
        visitor.visit_image(self)
    
    def __str__(self) -> str:
        return f"Image: {self.src}"

class Table(DocumentElement):
    """Represents a table element"""
    def __init__(self, rows: int, cols: int, data: List[List[str]]):
        self.rows = rows
        self.cols = cols
        self.data = data
    
    def accept(self, visitor: 'DocumentVisitor') -> None:
        visitor.visit_table(self)
    
    def __str__(self) -> str:
        return f"Table: {self.rows}x{self.cols}"

# Visitor Interface
class DocumentVisitor(ABC):
    """Abstract base class for document visitors"""
    @abstractmethod
    def visit_paragraph(self, paragraph: Paragraph) -> None:
        """Visit a paragraph element"""
        pass
    
    @abstractmethod
    def visit_image(self, image: Image) -> None:
        """Visit an image element"""
        pass
    
    @abstractmethod
    def visit_table(self, table: Table) -> None:
        """Visit a table element"""
        pass

# Concrete Visitors
class HtmlExporter(DocumentVisitor):
    """Exports document to HTML format"""
    def __init__(self):
        self.output = []
    
    def visit_paragraph(self, paragraph: Paragraph) -> None:
        self.output.append(f"<p>{paragraph.text}</p>")
    
    def visit_image(self, image: Image) -> None:
        alt_attr = f' alt="{image.alt}"' if image.alt else ""
        self.output.append(f'<img src="{image.src}"{alt_attr}>')
    
    def visit_table(self, table: Table) -> None:
        html = "<table>"
        for row in table.data:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        self.output.append(html)
    
    def get_output(self) -> str:
        return "\n".join(self.output)

class MarkdownExporter(DocumentVisitor):
    """Exports document to Markdown format"""
    def __init__(self):
        self.output = []
    
    def visit_paragraph(self, paragraph: Paragraph) -> None:
        self.output.append(f"{paragraph.text}\n")
    
    def visit_image(self, image: Image) -> None:
        alt_text = image.alt if image.alt else ""
        self.output.append(f"![{alt_text}]({image.src})")
    
    def visit_table(self, table: Table) -> None:
        # Build table header
        header = "| " + " | ".join(table.data[0]) + " |"
        separator = "|" + "|".join(["---"] * table.cols) + "|"
        self.output.append(header)
        self.output.append(separator)
        
        # Build table rows
        for row in table.data[1:]:
            self.output.append("| " + " | ".join(row) + " |")
    
    def get_output(self) -> str:
        return "\n".join(self.output)

class PlainTextExporter(DocumentVisitor):
    """Exports document to plain text format"""
    def __init__(self):
        self.output = []
    
    def visit_paragraph(self, paragraph: Paragraph) -> None:
        self.output.append(paragraph.text)
    
    def visit_image(self, image: Image) -> None:
        self.output.append(f"[Image: {image.src}]")
    
    def visit_table(self, table: Table) -> None:
        for row in table.data:
            self.output.append(" | ".join(row))
    
    def get_output(self) -> str:
        return "\n".join(self.output)

# Object Structure
class Document:
    """Represents a document containing elements"""
    def __init__(self, title: str):
        self.title = title
        self.elements: List[DocumentElement] = []
    
    def add_element(self, element: DocumentElement) -> None:
        """Add an element to the document"""
        self.elements.append(element)
    
    def accept(self, visitor: DocumentVisitor) -> None:
        """Accept a visitor to process all elements"""
        for element in self.elements:
            element.accept(visitor)

# Client
def main():
    # Create a document
    doc = Document("Sample Document")
    
    # Add elements to the document
    doc.add_element(Paragraph("This is the first paragraph of the document."))
    doc.add_element(Image("logo.png", "Company Logo"))
    doc.add_element(Table(3, 2, [
        ["Name", "Age"],
        ["Alice", "30"],
        ["Bob", "25"]
    ]))
    doc.add_element(Paragraph("This is the second paragraph with more text."))
    
    # Export to HTML
    print("=== HTML Export ===")
    html_exporter = HtmlExporter()
    doc.accept(html_exporter)
    print(html_exporter.get_output())
    
    # Export to Markdown
    print("\n=== Markdown Export ===")
    md_exporter = MarkdownExporter()
    doc.accept(md_exporter)
    print(md_exporter.get_output())
    
    # Export to Plain Text
    print("\n=== Plain Text Export ===")
    text_exporter = PlainTextExporter()
    doc.accept(text_exporter)
    print(text_exporter.get_output())
    
    # Demonstrate adding a new visitor without changing element classes
    print("\n=== Adding New Visitor (Word Count) ===")
    class WordCountVisitor(DocumentVisitor):
        """Visitor that counts words in the document"""
        def __init__(self):
            self.word_count = 0
        
        def visit_paragraph(self, paragraph: Paragraph) -> None:
            self.word_count += len(paragraph.text.split())
        
        def visit_image(self, image: Image) -> None:
            # Images don't contribute to word count
            pass
        
        def visit_table(self, table: Table) -> None:
            for row in table.data:
                for cell in row:
                    self.word_count += len(cell.split())
    
    word_counter = WordCountVisitor()
    doc.accept(word_counter)
    print(f"Total word count: {word_counter.word_count}")

if __name__ == "__main__":
    main()