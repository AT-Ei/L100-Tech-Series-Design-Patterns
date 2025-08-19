# Implementation Interface
class Device:
    """The Implementation interface defines operations for all device types"""
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass
    
    def set_channel(self, channel):
        pass
    
    def get_status(self):
        pass

# Concrete Implementations
class TV(Device):
    """Concrete implementation for TV devices"""
    def __init__(self):
        self._on = False
        self._channel = 1
        self._max_channels = 100
    
    def turn_on(self):
        self._on = True
        print("TV is now ON")
    
    def turn_off(self):
        self._on = False
        print("TV is now OFF")
    
    def set_channel(self, channel):
        if self._on:
            self._channel = max(1, min(channel, self._max_channels))
            print(f"TV channel set to {self._channel}")
        else:
            print("Cannot set channel - TV is OFF")
    
    def get_status(self):
        status = "ON" if self._on else "OFF"
        return f"TV Status: {status}, Channel: {self._channel}"

class Radio(Device):
    """Concrete implementation for Radio devices"""
    def __init__(self):
        self._on = False
        self._frequency = 87.5  # MHz
        self._max_frequency = 108.0
    
    def turn_on(self):
        self._on = True
        print("Radio is now ON")
    
    def turn_off(self):
        self._on = False
        print("Radio is now OFF")
    
    def set_channel(self, frequency):
        if self._on:
            self._frequency = max(87.5, min(frequency, self._max_frequency))
            print(f"Radio frequency set to {self._frequency:.1f} MHz")
        else:
            print("Cannot set frequency - Radio is OFF")
    
    def get_status(self):
        status = "ON" if self._on else "OFF"
        return f"Radio Status: {status}, Frequency: {self._frequency:.1f} MHz"

# Abstraction
class RemoteControl:
    """Abstraction representing a remote control"""
    def __init__(self, device):
        self._device = device
    
    def toggle_power(self):
        if self._device.get_status().split()[1] == "ON":
            self._device.turn_off()
        else:
            self._device.turn_on()
    
    def channel_up(self):
        current_status = self._device.get_status()
        if isinstance(self._device, TV):
            current_channel = int(current_status.split("Channel: ")[1])
            self._device.set_channel(current_channel + 1)
        elif isinstance(self._device, Radio):
            current_freq = float(current_status.split("Frequency: ")[1].split()[0])
            self._device.set_channel(current_freq + 0.5)
    
    def channel_down(self):
        current_status = self._device.get_status()
        if isinstance(self._device, TV):
            current_channel = int(current_status.split("Channel: ")[1])
            self._device.set_channel(current_channel - 1)
        elif isinstance(self._device, Radio):
            current_freq = float(current_status.split("Frequency: ")[1].split()[0])
            self._device.set_channel(current_freq - 0.5)
    
    def show_status(self):
        print(self._device.get_status())

# Refined Abstraction
class AdvancedRemoteControl(RemoteControl):
    """Extended remote with additional features"""
    def mute(self):
        print("Mute function activated")
        # Implementation would depend on specific device capabilities

# Demonstration
if __name__ == "__main__":
    # Create devices (implementations)
    tv = TV()
    radio = Radio()
    
    # Create remotes (abstractions) linked to devices
    tv_remote = RemoteControl(tv)
    radio_remote = AdvancedRemoteControl(radio)
    
    # Operate TV using basic remote
    print("=== Operating TV ===")
    tv_remote.toggle_power()
    tv_remote.channel_up()
    tv_remote.channel_up()
    tv_remote.show_status()
    tv_remote.toggle_power()
    
    # Operate Radio using advanced remote
    print("\n=== Operating Radio ===")
    radio_remote.toggle_power()
    radio_remote.channel_up()
    radio_remote.channel_up()
    radio_remote.show_status()
    radio_remote.mute()  # Advanced feature
    radio_remote.toggle_power()