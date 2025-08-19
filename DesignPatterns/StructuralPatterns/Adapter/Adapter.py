# Target Interface: Expected by the client (US device)
class USASocket:
    """Interface expected by US devices (110V)"""
    def voltage(self):
        """Return voltage in volts"""
        pass

# Adaptee: Existing class with incompatible interface
class EuropeanSocket:
    """European socket providing 230V"""
    def voltage(self):
        """European standard voltage"""
        return 230

# Adapter: Makes EuropeanSocket compatible with USASocket interface
class SocketAdapter(USASocket):
    """Adapter to convert European 230V to US 110V"""
    def __init__(self, european_socket):
        self.european_socket = european_socket
    
    def voltage(self):
        """Convert 230V to 110V"""
        source_voltage = self.european_socket.voltage()
        # Step down voltage (simplified for demo)
        converted_voltage = 110
        print(f"Adapter: Converting {source_voltage}V to {converted_voltage}V")
        return converted_voltage

# Client: US device expecting 110V
class USDevice:
    """Device designed for US sockets"""
    def __init__(self, socket):
        self.socket = socket
    
    def power_on(self):
        """Use socket to power device"""
        voltage = self.socket.voltage()
        if voltage == 110:
            print("Device powered on successfully!")
        else:
            print(f"Error: {voltage}V is incompatible!")

# Demonstration
if __name__ == "__main__":
    # Create European socket (Adaptee)
    european_socket = EuropeanSocket()
    
    # Create adapter to make EuropeanSocket compatible
    adapter = SocketAdapter(european_socket)
    
    # Create US device using the adapter
    us_device = USDevice(adapter)
    
    # Power on the device (works with adapter)
    us_device.power_on()