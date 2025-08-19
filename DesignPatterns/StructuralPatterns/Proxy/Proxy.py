from abc import ABC, abstractmethod
import time

# Subject Interface
class Image(ABC):
    """Abstract base class for all image types"""
    @abstractmethod
    def display(self):
        """Display the image"""
        pass

# Real Subject
class RealImage(Image):
    """The actual image that loads from disk"""
    def __init__(self, filename):
        self.filename = filename
        self._load_image_from_disk()
    
    def _load_image_from_disk(self):
        """Simulate loading a large image from disk"""
        print(f"Loading {self.filename} from disk...")
        time.sleep(2)  # Simulate slow loading
        print(f"{self.filename} loaded!")
    
    def display(self):
        print(f"Displaying {self.filename}")

# Proxy
class ProxyImage(Image):
    """Proxy that controls access to RealImage"""
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None  # Reference to RealImage
    
    def display(self):
        """Load image only when needed"""
        if self._real_image is None:
            print(f"First request for {self.filename}. Creating real image...")
            self._real_image = RealImage(self.filename)
        self._real_image.display()

# Demonstration
if __name__ == "__main__":
    # Create proxy images (real images not loaded yet)
    print("=== Creating image proxies ===")
    image1 = ProxyImage("photo1.jpg")
    image2 = ProxyImage("photo2.jpg")
    
    # Images are not loaded yet - no loading time
    print("\n=== Image proxies created (no images loaded) ===")
    
    # Display first image (will trigger loading)
    print("\n=== Displaying first image ===")
    start_time = time.time()
    image1.display()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    # Display first image again (uses cached version)
    print("\n=== Displaying first image again ===")
    start_time = time.time()
    image1.display()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    # Display second image (will trigger loading)
    print("\n=== Displaying second image ===")
    start_time = time.time()
    image2.display()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    # Display second image again (uses cached version)
    print("\n=== Displaying second image again ===")
    start_time = time.time()
    image2.display()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")