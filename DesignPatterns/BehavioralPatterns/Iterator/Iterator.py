from abc import ABC, abstractmethod
from typing import List, Any, Iterator as PyIterator

# Iterator Interface
class Iterator(ABC):
    """Abstract base class for all iterators"""
    @abstractmethod
    def has_next(self) -> bool:
        """Check if there are more elements"""
        pass
    
    @abstractmethod
    def next(self) -> Any:
        """Get the next element"""
        pass

# Aggregate Interface
class Aggregate(ABC):
    """Abstract base class for all aggregates"""
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Create an iterator for the aggregate"""
        pass

# Concrete Aggregate
class Playlist(Aggregate):
    """Represents a music playlist"""
    def __init__(self):
        self._songs: List['Song'] = []
    
    def add_song(self, song: 'Song') -> None:
        """Add a song to the playlist"""
        self._songs.append(song)
    
    def get_songs(self) -> List['Song']:
        """Get all songs (for demonstration only)"""
        return self._songs.copy()
    
    def create_iterator(self) -> Iterator:
        """Create a sequential iterator"""
        return SequentialIterator(self)
    
    def create_reverse_iterator(self) -> Iterator:
        """Create a reverse iterator"""
        return ReverseIterator(self)
    
    def create_shuffle_iterator(self) -> Iterator:
        """Create a shuffle iterator"""
        return ShuffleIterator(self)

# Concrete Iterators
class SequentialIterator(Iterator):
    """Iterates through songs in order"""
    def __init__(self, playlist: Playlist):
        self._playlist = playlist
        self._position = 0
    
    def has_next(self) -> bool:
        return self._position < len(self._playlist.get_songs())
    
    def next(self) -> 'Song':
        if not self.has_next():
            raise StopIteration("No more songs")
        song = self._playlist.get_songs()[self._position]
        self._position += 1
        return song

class ReverseIterator(Iterator):
    """Iterates through songs in reverse order"""
    def __init__(self, playlist: Playlist):
        self._playlist = playlist
        self._position = len(playlist.get_songs()) - 1
    
    def has_next(self) -> bool:
        return self._position >= 0
    
    def next(self) -> 'Song':
        if not self.has_next():
            raise StopIteration("No more songs")
        song = self._playlist.get_songs()[self._position]
        self._position -= 1
        return song

class ShuffleIterator(Iterator):
    """Iterates through songs in random order"""
    def __init__(self, playlist: Playlist):
        self._playlist = playlist
        self._songs = playlist.get_songs().copy()
        self._position = 0
        self._shuffle()
    
    def _shuffle(self) -> None:
        """Shuffle the songs using Fisher-Yates algorithm"""
        import random
        for i in range(len(self._songs) - 1, 0, -1):
            j = random.randint(0, i)
            self._songs[i], self._songs[j] = self._songs[j], self._songs[i]
    
    def has_next(self) -> bool:
        return self._position < len(self._songs)
    
    def next(self) -> 'Song':
        if not self.has_next():
            raise StopIteration("No more songs")
        song = self._songs[self._position]
        self._position += 1
        return song

# Item Class
class Song:
    """Represents a song in the playlist"""
    def __init__(self, title: str, artist: str, duration: str):
        self.title = title
        self.artist = artist
        self.duration = duration
    
    def __str__(self):
        return f"{self.title} by {self.artist} ({self.duration})"

# Client
def main():
    # Create a playlist
    playlist = Playlist()
    
    # Add songs to the playlist
    playlist.add_song(Song("Bohemian Rhapsody", "Queen", "5:55"))
    playlist.add_song(Song("Stairway to Heaven", "Led Zeppelin", "8:02"))
    playlist.add_song(Song("Hotel California", "Eagles", "6:30"))
    playlist.add_song(Song("Sweet Child O'Mine", "Guns N' Roses", "5:56"))
    playlist.add_song(Song("Smells Like Teen Spirit", "Nirvana", "5:01"))
    
    # Demonstrate sequential iteration
    print("=== Sequential Iteration ===")
    sequential_iter = playlist.create_iterator()
    while sequential_iter.has_next():
        song = sequential_iter.next()
        print(song)
    
    # Demonstrate reverse iteration
    print("\n=== Reverse Iteration ===")
    reverse_iter = playlist.create_reverse_iterator()
    while reverse_iter.has_next():
        song = reverse_iter.next()
        print(song)
    
    # Demonstrate shuffle iteration
    print("\n=== Shuffle Iteration ===")
    shuffle_iter = playlist.create_shuffle_iterator()
    while shuffle_iter.has_next():
        song = shuffle_iter.next()
        print(song)
    
    # Demonstrate Python's built-in iterator support
    print("\n=== Using Python's Built-in Iterator ===")
    for song in playlist:
        print(song)
    
    # Demonstrate list comprehension
    print("\n=== List Comprehension ===")
    song_titles = [song.title for song in playlist]
    print("Song titles:", song_titles)

# Make Playlist compatible with Python's iteration protocol
def __iter__(self):
    return self.create_iterator()

Playlist.__iter__ = __iter__

if __name__ == "__main__":
    main()