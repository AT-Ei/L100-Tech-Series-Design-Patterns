from abc import ABC, abstractmethod
from typing import Optional, List

# Handler Interface
class SupportHandler(ABC):
    """Abstract base class for all support handlers"""
    def __init__(self):
        self._next_handler: Optional['SupportHandler'] = None
    
    def set_next(self, handler: 'SupportHandler') -> 'SupportHandler':
        """Set the next handler in the chain"""
        self._next_handler = handler
        return handler  # Return handler for easy chaining
    
    @abstractmethod
    def handle(self, ticket: 'SupportTicket') -> str:
        """Handle the support ticket or pass to next handler"""
        pass
    
    def _handle_next(self, ticket: 'SupportTicket') -> str:
        """Pass ticket to next handler in chain"""
        if self._next_handler:
            return self._next_handler.handle(ticket)
        return f"No handler available for ticket: {ticket.description}"

# Concrete Handlers
class FrontDeskSupport(SupportHandler):
    """Handles basic customer inquiries"""
    def handle(self, ticket: 'SupportTicket') -> str:
        if ticket.level == "basic":
            return f"FrontDesk handled: {ticket.description}"
        return self._handle_next(ticket)

class TechnicalSupport(SupportHandler):
    """Handles technical issues"""
    def handle(self, ticket: 'SupportTicket') -> str:
        if ticket.level == "technical":
            return f"TechnicalSupport handled: {ticket.description}"
        return self._handle_next(ticket)

class ManagerSupport(SupportHandler):
    """Handles escalated issues and refunds"""
    def handle(self, ticket: 'SupportTicket') -> str:
        if ticket.level in ["escalated", "refund"]:
            return f"ManagerSupport handled: {ticket.description}"
        return self._handle_next(ticket)

class DirectorSupport(SupportHandler):
    """Handles critical issues and complaints"""
    def handle(self, ticket: 'SupportTicket') -> str:
        if ticket.level in ["critical", "complaint"]:
            return f"DirectorSupport handled: {ticket.description}"
        return self._handle_next(ticket)

# Request Class
class SupportTicket:
    """Represents a customer support ticket"""
    def __init__(self, description: str, level: str):
        self.description = description
        self.level = level
    
    def __str__(self):
        return f"Ticket[{self.level}]: {self.description}"

# Client
class CustomerSupport:
    """Creates the chain and processes tickets"""
    def __init__(self):
        # Create the chain of responsibility
        self._front_desk = FrontDeskSupport()
        self._technical = TechnicalSupport()
        self._manager = ManagerSupport()
        self._director = DirectorSupport()
        
        # Set up the chain
        self._front_desk.set_next(self._technical).set_next(self._manager).set_next(self._director)
    
    def submit_ticket(self, description: str, level: str) -> str:
        """Submit a ticket to the support chain"""
        ticket = SupportTicket(description, level)
        print(f"\nSubmitting: {ticket}")
        result = self._front_desk.handle(ticket)
        print(f"Result: {result}")
        return result

# Demonstration
if __name__ == "__main__":
    # Create customer support system
    support = CustomerSupport()
    
    # Submit various tickets to demonstrate the chain
    tickets = [
        ("How do I reset my password?", "basic"),
        ("My application crashes on startup", "technical"),
        ("I want to speak to a manager about poor service", "escalated"),
        ("I demand a full refund for my purchase", "refund"),
        ("The entire system is down and customers are affected", "critical"),
        ("I want to file a formal complaint about your company", "complaint"),
        ("This is an unknown issue type", "unknown")
    ]
    
    print("=== Customer Support Ticket Processing ===")
    for desc, level in tickets:
        support.submit_ticket(desc, level)
    
    # Demonstrate chain modification
    print("\n=== Modifying the chain ===")
    # Create a new specialized handler
    class SecuritySupport(SupportHandler):
        def handle(self, ticket: 'SupportTicket') -> str:
            if ticket.level == "security":
                return f"SecuritySupport handled: {ticket.description}"
            return self._handle_next(ticket)
    
    # Insert security support between technical and manager
    security = SecuritySupport()
    support._technical.set_next(security).set_next(support._manager)
    
    # Test the modified chain
    print("\nTesting modified chain with security issue:")
    support.submit_ticket("My account was hacked", "security")