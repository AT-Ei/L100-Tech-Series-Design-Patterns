# Subsystem Classes
class DVDPlayer:
    """Subsystem component for DVD player"""
    def on(self):
        print("DVD Player: ON")
    
    def off(self):
        print("DVD Player: OFF")
    
    def play(self, movie):
        print(f"DVD Player: Playing '{movie}'")
    
    def stop(self):
        print("DVD Player: Stopped")
    
    def pause(self):
        print("DVD Player: Paused")

class Projector:
    """Subsystem component for projector"""
    def on(self):
        print("Projector: ON")
    
    def off(self):
        print("Projector: OFF")
    
    def wide_screen_mode(self):
        print("Projector: Wide screen mode")
    
    def tv_mode(self):
        print("Projector: TV mode")

class SoundSystem:
    """Subsystem component for sound system"""
    def on(self):
        print("Sound System: ON")
    
    def off(self):
        print("Sound System: OFF")
    
    def set_surround_sound(self):
        print("Sound System: Surround sound activated")
    
    def set_volume(self, level):
        print(f"Sound System: Volume set to {level}")

class Lights:
    """Subsystem component for lights"""
    def on(self):
        print("Lights: ON")
    
    def off(self):
        print("Lights: OFF")
    
    def dim(self, level):
        print(f"Lights: Dimmed to {level}%")

# Facade Class
class HomeTheaterFacade:
    """Facade that provides simplified interface to home theater subsystem"""
    def __init__(self):
        self.dvd = DVDPlayer()
        self.projector = Projector()
        self.sound = SoundSystem()
        self.lights = Lights()
    
    def watch_movie(self, movie):
        """Simplified method to watch a movie"""
        print("\n=== Get ready to watch a movie ===")
        self.lights.dim(20)
        self.projector.on()
        self.projector.wide_screen_mode()
        self.sound.on()
        self.sound.set_surround_sound()
        self.sound.set_volume(10)
        self.dvd.on()
        self.dvd.play(movie)
    
    def end_movie(self):
        """Simplified method to end movie watching"""
        print("\n=== Shutting down theater ===")
        self.dvd.stop()
        self.dvd.off()
        self.sound.off()
        self.projector.off()
        self.lights.on()
    
    def pause_movie(self):
        """Simplified method to pause movie"""
        print("\n=== Movie paused ===")
        self.dvd.pause()
        self.lights.dim(50)
        self.sound.set_volume(5)

# Demonstration
if __name__ == "__main__":
    # Create the facade
    home_theater = HomeTheaterFacade()
    
    # Watch a movie using simplified interface
    home_theater.watch_movie("Inception")
    
    # Pause the movie
    home_theater.pause_movie()
    
    # End the movie
    home_theater.end_movie()
    
    # Demonstrate direct subsystem access (not recommended but possible)
    print("\n=== Direct subsystem access (not using facade) ===")
    dvd = DVDPlayer()
    dvd.on()
    dvd.play("The Matrix")
    dvd.stop()
    dvd.off()