from abc import ABC, abstractmethod
from typing import Optional

# State Interface
class DocumentState(ABC):
    """Abstract base class for document states"""
    @abstractmethod
    def publish(self, document: 'Document') -> None:
        """Publish the document"""
        pass
    
    @abstractmethod
    def moderate(self, document: 'Document') -> None:
        """Send document for moderation"""
        pass
    
    @abstractmethod
    def reject(self, document: 'Document') -> None:
        """Reject the document"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Return state name"""
        pass

# Concrete States
class DraftState(DocumentState):
    """Document is in draft state"""
    def publish(self, document: 'Document') -> None:
        print("Document sent for moderation")
        document.change_state(ModerationState())
    
    def moderate(self, document: 'Document') -> None:
        print("Cannot moderate a draft document. Please publish first.")
    
    def reject(self, document: 'Document') -> None:
        print("Document rejected. Returning to draft.")
        # Already in draft, no state change needed
    
    def __str__(self) -> str:
        return "Draft"

class ModerationState(DocumentState):
    """Document is in moderation state"""
    def publish(self, document: 'Document') -> None:
        print("Document published successfully")
        document.change_state(PublishedState())
    
    def moderate(self, document: 'Document') -> None:
        print("Document is already in moderation")
    
    def reject(self, document: 'Document') -> None:
        print("Document rejected by moderator. Returning to draft.")
        document.change_state(DraftState())
    
    def __str__(self) -> str:
        return "Moderation"

class PublishedState(DocumentState):
    """Document is in published state"""
    def publish(self, document: 'Document') -> None:
        print("Document is already published")
    
    def moderate(self, document: 'Document') -> None:
        print("Published document cannot be moderated. Create a new version.")
    
    def reject(self, document: 'Document') -> None:
        print("Published document cannot be rejected. Create a new version.")
    
    def __str__(self) -> str:
        return "Published"

# Context Class
class Document:
    """The context class that maintains state"""
    def __init__(self, title: str):
        self.title = title
        self._state: DocumentState = DraftState()
        self._author: Optional[str] = None
        self._moderator: Optional[str] = None
        print(f"Created document: '{self.title}'")
    
    def change_state(self, state: DocumentState) -> None:
        """Change the document's state"""
        print(f"Document state changed from {self._state} to {state}")
        self._state = state
    
    def set_author(self, author: str) -> None:
        """Set the document author"""
        self._author = author
        print(f"Author set to: {self._author}")
    
    def set_moderator(self, moderator: str) -> None:
        """Set the document moderator"""
        self._moderator = moderator
        print(f"Moderator set to: {self._moderator}")
    
    def publish(self) -> None:
        """Publish the document (delegates to current state)"""
        print(f"\nAttempting to publish document: '{self.title}'")
        self._state.publish(self)
    
    def moderate(self) -> None:
        """Send document for moderation (delegates to current state)"""
        print(f"\nAttempting to moderate document: '{self.title}'")
        self._state.moderate(self)
    
    def reject(self) -> None:
        """Reject the document (delegates to current state)"""
        print(f"\nAttempting to reject document: '{self.title}'")
        self._state.reject(self)
    
    def __str__(self) -> str:
        return f"Document '{self.title}' by {self._author or 'Unknown'} - State: {self._state}"

# Client
def main():
    # Create a new document
    doc = Document("State Pattern Example")
    doc.set_author("Jane Doe")
    
    # Initial state is Draft
    print(f"\nCurrent state: {doc._state}")
    
    # Try to moderate a draft document (should fail)
    doc.moderate()
    
    # Publish the document (moves to moderation)
    doc.publish()
    
    # Set moderator
    doc.set_moderator("John Smith")
    
    # Try to publish again (should succeed and move to published)
    doc.publish()
    
    # Try to moderate a published document (should fail)
    doc.moderate()
    
    # Try to reject a published document (should fail)
    doc.reject()
    
    # Create a new document to demonstrate rejection
    print("\n=== Demonstrating Rejection ===")
    doc2 = Document("Rejected Document")
    doc2.set_author("Alice Johnson")
    
    # Publish to moderation
    doc2.publish()
    doc2.set_moderator("Bob Wilson")
    
    # Reject the document (moves back to draft)
    doc2.reject()
    
    # Try to publish again (should work)
    doc2.publish()
    doc2.set_moderator("Bob Wilson")
    
    # Publish again to final state
    doc2.publish()
    
    # Demonstrate state transitions
    print("\n=== State Transition Summary ===")
    print("Document lifecycle:")
    print("1. Draft -> Publish -> Moderation")
    print("2. Moderation -> Reject -> Draft")
    print("3. Draft -> Publish -> Moderation -> Publish -> Published")
    print("\nNote: Published documents cannot be moderated or rejected")

if __name__ == "__main__":
    main()