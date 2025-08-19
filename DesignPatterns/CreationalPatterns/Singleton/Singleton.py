import threading
from datetime import datetime
from typing import List, Optional

class SingletonMeta(type):
    """Thread-safe Singleton metaclass"""
    _instances = {}
    _lock: threading.Lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    """Thread-safe Singleton Logger class"""
    
    def __init__(self):
        """Initialize logger if not already initialized)"""
        if not hasattr(self, '_initialized'):
            self._logs: List[str] = []
            self._initialized = True
            print("Logger instance created")
    
    def log(self, message: str) -> None:
        """Add a log entry with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self._logs.append(log_entry)
        print(f"LOG: {log_entry}")
    
    def get_logs(self) -> List[str]:
        """Get all log entries"""
        return self._logs.copy()
    
    def clear_logs(self) -> None:
        """Clear all log entries"""
        self._logs.clear()
        print("All logs cleared")
    
    def get_log_count(self) -> int:
        """Get number of log entries"""
        return len(self._logs)

# Demonstration
def worker(logger: Logger, worker_id: int) -> None:
    """Worker function that uses the logger"""
    logger.log(f"Worker {worker_id} started")
    logger.log(f"Worker {worker_id} processing data")
    logger.log(f"Worker {worker_id} completed")

def main():
    # Demonstrate Singleton behavior
    print("=== Singleton Pattern Demonstration ===")
    
    # Create multiple logger instances
    logger1 = Logger()
    logger2 = Logger()
    logger3 = Logger()
    
    # Verify all references point to the same instance
    print(f"Logger 1 ID: {id(logger1)}")
    print(f"Logger 2 ID: {id(logger2)}")
    print(f"Logger 3 ID: {id(logger3)}")
    print(f"Are all instances the same? {logger1 is logger2 is logger3}")
    
    # Use the logger
    print("\n=== Logging Example ===")
    logger1.log("Application started")
    logger2.log("User logged in")
    logger3.log("Processing request")
    
    # Show logs
    print("\n=== Log Entries ===")
    logs = logger1.get_logs()
    for i, log in enumerate(logs, 1):
        print(f"{i}. {log}")
    
    # Demonstrate thread safety
    print("\n=== Thread Safety Test ===")
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(logger1, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Show final logs
    print("\n=== Final Log Count ===")
    print(f"Total log entries: {logger1.get_log_count()}")
    
    # Clear logs
    print("\n=== Clearing Logs ===")
    logger1.clear_logs()
    print(f"Log count after clear: {logger1.get_log_count()}")

if __name__ == "__main__":
    main()