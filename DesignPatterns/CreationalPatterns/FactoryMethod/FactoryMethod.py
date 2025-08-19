from abc import ABC, abstractmethod
from typing import List
import os

# Product Interface
class Document(ABC):
    """Abstract base class for all document types"""
    @abstractmethod
    def create(self) -> None:
        """Create the document content"""
        pass
    
    @abstractmethod
    def save(self, filename: str) -> None:
        """Save the document to a file"""
        pass
    
    @abstractmethod
    def get_content(self) -> str:
        """Get the document content"""
        pass

# Concrete Products
class PdfDocument(Document):
    """PDF document implementation"""
    def __init__(self):
        self.content = ""
    
    def create(self) -> None:
        self.content = "%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        print("PDF document created")
    
    def save(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(self.content)
        print(f"PDF document saved as {filename}")
    
    def get_content(self) -> str:
        return self.content

class WordDocument(Document):
    """Word document implementation"""
    def __init__(self):
        self.content = ""
    
    def create(self) -> None:
        self.content = "PK\x03\x04\n[Content_Types].xml\n...\nword/document.xml\n"
        print("Word document created")
    
    def save(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(self.content)
        print(f"Word document saved as {filename}")
    
    def get_content(self) -> str:
        return self.content

class TextDocument(Document):
    """Text document implementation"""
    def __init__(self):
        self.content = ""
    
    def create(self) -> None:
        self.content = "This is a plain text document.\n"
        print("Text document created")
    
    def save(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(self.content)
        print(f"Text document saved as {filename}")
    
    def get_content(self) -> str:
        return self.content

# Creator Class
class DocumentCreator(ABC):
    """Abstract creator class with factory method"""
    def __init__(self):
        self.documents: List[Document] = []
    
    def create_document(self, filename: str) -> Document:
        """Factory method to create a document"""
        document = self.factory_method()
        document.create()
        document.save(filename)
        self.documents.append(document)
        return document
    
    @abstractmethod
    def factory_method(self) -> Document:
        """Factory method to be implemented by subclasses"""
        pass
    
    def list_documents(self) -> None:
        """List all created documents"""
        print("\nCreated documents:")
        for i, doc in enumerate(self.documents, 1):
            print(f"{i}. {doc.__class__.__name__}")

# Concrete Creators
class PdfCreator(DocumentCreator):
    """Creator for PDF documents"""
    def factory_method(self) -> Document:
        return PdfDocument()

class WordCreator(DocumentCreator):
    """Creator for Word documents"""
    def factory_method(self) -> Document:
        return WordDocument()

class TextCreator(DocumentCreator):
    """Creator for Text documents"""
    def factory_method(self) -> Document:
        return TextDocument()

# Parameterized Factory Method
class GenericDocumentCreator(DocumentCreator):
    """Creator that can create any document type"""
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type
    
    def factory_method(self) -> Document:
        if self.doc_type == "pdf":
            return PdfDocument()
        elif self.doc_type == "word":
            return WordDocument()
        elif self.doc_type == "text":
            return TextDocument()
        else:
            raise ValueError(f"Unknown document type: {self.doc_type}")

# Client
def main():
    # Create specific document creators
    pdf_creator = PdfCreator()
    word_creator = WordCreator()
    text_creator = TextCreator()
    
    # Create documents using factory method
    print("=== Creating PDF Document ===")
    pdf_doc = pdf_creator.create_document("document.pdf")
    
    print("\n=== Creating Word Document ===")
    word_doc = word_creator.create_document("document.docx")
    
    print("\n=== Creating Text Document ===")
    text_doc = text_creator.create_document("document.txt")
    
    # List all created documents
    pdf_creator.list_documents()
    
    # Demonstrate parameterized factory method
    print("\n=== Using Parameterized Factory Method ===")
    
    # Create a generic creator for PDF
    generic_pdf_creator = GenericDocumentCreator("pdf")
    pdf_doc2 = generic_pdf_creator.create_document("document2.pdf")
    
    # Create a generic creator for Word
    generic_word_creator = GenericDocumentCreator("word")
    word_doc2 = generic_word_creator.create_document("document2.docx")
    
    # Create a generic creator for Text
    generic_text_creator = GenericDocumentCreator("text")
    text_doc2 = generic_text_creator.create_document("document2.txt")
    
    # Try to create an unknown document type
    print("\n=== Creating Unknown Document Type ===")
    try:
        unknown_creator = GenericDocumentCreator("excel")
        unknown_doc = unknown_creator.create_document("document.xlsx")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Demonstrate document content
    print("\n=== Document Contents ===")
    print("PDF content:")
    print(pdf_doc.get_content())
    print("\nWord content:")
    print(word_doc.get_content())
    print("\nText content:")
    print(text_doc.get_content())
    
    # Clean up created files
    print("\n=== Cleaning Up ===")
    files_to_remove = [
        "document.pdf", "document.docx", "document.txt",
        "document2.pdf", "document2.docx", "document2.txt"
    ]
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}")

if __name__ == "__main__":
    main()