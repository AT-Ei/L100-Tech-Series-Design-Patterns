from abc import ABC, abstractmethod
from typing import List, Dict

# Mediator Interface
class ChatRoomMediator(ABC):
    """Abstract base class for chat room mediators"""
    @abstractmethod
    def send_message(self, message: str, user: 'User', recipient: 'User' = None) -> None:
        """Send a message to another user or broadcast to all"""
        pass
    
    @abstractmethod
    def register_user(self, user: 'User') -> None:
        """Register a user with the chat room"""
        pass

# Colleague Interface
class User(ABC):
    """Abstract base class for chat users"""
    def __init__(self, name: str, mediator: ChatRoomMediator):
        self.name = name
        self.mediator = mediator
    
    @abstractmethod
    def send(self, message: str, recipient: 'User' = None) -> None:
        """Send a message through the mediator"""
        pass
    
    @abstractmethod
    def receive(self, message: str, sender: 'User') -> None:
        """Receive a message from another user"""
        pass

# Concrete Mediator
class ChatRoom(ChatRoomMediator):
    """Concrete mediator that manages user communications"""
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    def register_user(self, user: 'User') -> None:
        """Register a user with the chat room"""
        if user.name not in self._users:
            self._users[user.name] = user
            print(f"{user.name} has joined the chat room")
    
    def send_message(self, message: str, user: 'User', recipient: 'User' = None) -> None:
        """Send a message to a specific user or broadcast to all"""
        if recipient:
            # Private message
            if recipient.name in self._users:
                recipient.receive(message, user)
            else:
                print(f"Error: User {recipient.name} not found in chat room")
        else:
            # Broadcast message to all users except sender
            for u in self._users.values():
                if u != user:
                    u.receive(message, user)

# Concrete Colleague
class ChatUser(User):
    """Concrete user that participates in the chat"""
    def send(self, message: str, recipient: 'User' = None) -> None:
        """Send a message through the mediator"""
        print(f"{self.name} sends: '{message}'")
        self.mediator.send_message(message, self, recipient)
    
    def receive(self, message: str, sender: 'User') -> None:
        """Receive a message from another user"""
        print(f"{self.name} receives from {sender.name}: '{message}'")

# Client
def main():
    # Create the chat room (mediator)
    chat_room = ChatRoom()
    
    # Create users and register them with the chat room
    alice = ChatUser("Alice", chat_room)
    bob = ChatUser("Bob", chat_room)
    charlie = ChatUser("Charlie", chat_room)
    diana = ChatUser("Diana", chat_room)
    
    chat_room.register_user(alice)
    chat_room.register_user(bob)
    chat_room.register_user(charlie)
    chat_room.register_user(diana)
    
    print("\n=== Chat Room Communication ===")
    
    # Alice sends a broadcast message
    alice.send("Hello everyone!")
    
    # Bob sends a private message to Alice
    bob.send("Hi Alice! How are you?", alice)
    
    # Charlie sends a broadcast message
    charlie.send("Good morning all!")
    
    # Diana sends a private message to Bob
    diana.send("Bob, can you help me with something?", bob)
    
    # Bob sends a broadcast message
    bob.send("Sure Diana, what do you need?")
    
    # Demonstrate error handling
    print("\n=== Error Handling ===")
    # Try to send a message to an unregistered user
    eve = ChatUser("Eve", chat_room)
    alice.send("Hello Eve!", eve)  # Eve is not registered
    
    # Try to send a message from an unregistered user
    frank = ChatUser("Frank", chat_room)
    frank.send("I'm not registered!")  # Frank is not registered

if __name__ == "__main__":
    main()