import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, TextBox

class SignalEncoder:
    def __init__(self):
        # Initialize parameters
        self.bit_duration = 1.0  # duration of each bit in seconds
        self.sampling_rate = 1000  # samples per second
        self.default_bits = "10110010"  # Default bit pattern
        
        # Create figure
        self.fig = plt.figure(figsize=(12, 10))
        plt.subplots_adjust(bottom=0.25)
        
        # Create UI elements
        self.create_ui()
        
        # Plot initial signal
        self.update_plot()
    
    def create_ui(self):
        # Create axes for plots
        self.ax_bits = plt.subplot2grid((3, 1), (0, 0))
        self.ax_encoded = plt.subplot2grid((3, 1), (1, 0), rowspan=2)
        
        # Add bit pattern input
        ax_bits_input = plt.axes([0.2, 0.15, 0.6, 0.05])
        self.bits_box = TextBox(ax_bits_input, 'Bit Pattern:', initial=self.default_bits)
        
        # Add encoding scheme selection
        ax_encoding = plt.axes([0.2, 0.05, 0.6, 0.05])
        self.encoding_radio = RadioButtons(
            ax_encoding,
            ('NRZ-L', 'NRZ-I', 'AMI', 'Manchester', 'Differential Manchester'),
            active=0
        )
        
        # Set callback functions
        self.bits_box.on_submit(self.on_update)
        self.encoding_radio.on_clicked(self.on_update)
    
    def on_update(self, event=None):
        self.update_plot()
    
    def generate_time_axis(self, bits):
        total_time = len(bits) * self.bit_duration
        return np.linspace(0, total_time, int(total_time * self.sampling_rate), endpoint=False)
    
    def nrz_l(self, bits, t):
        signal = np.zeros_like(t)
        for i, bit in enumerate(bits):
            start = i * self.bit_duration
            end = (i + 1) * self.bit_duration
            mask = (t >= start) & (t < end)
            signal[mask] = 1 if bit == '1' else -1
        return signal
    
    def nrz_i(self, bits, t):
        signal = np.zeros_like(t)
        current_level = 1  # Start with high
        
        for i, bit in enumerate(bits):
            start = i * self.bit_duration
            end = (i + 1) * self.bit_duration
            mask = (t >= start) & (t < end)
            
            if bit == '1':
                current_level *= -1  # Toggle level
            signal[mask] = current_level
        return signal
    
    def ami(self, bits, t):
        signal = np.zeros_like(t)
        last_polarity = 1  # Start with positive
        
        for i, bit in enumerate(bits):
            start = i * self.bit_duration
            end = (i + 1) * self.bit_duration
            mask = (t >= start) & (t < end)
            
            if bit == '1':
                signal[mask] = last_polarity
                last_polarity *= -1  # Alternate polarity
            else:
                signal[mask] = 0
        return signal
    
    def manchester(self, bits, t):
        signal = np.zeros_like(t)
        half_bit = self.bit_duration / 2
        
        for i, bit in enumerate(bits):
            start = i * self.bit_duration
            mid = start + half_bit
            end = (i + 1) * self.bit_duration
            
            mask_first_half = (t >= start) & (t < mid)
            mask_second_half = (t >= mid) & (t < end)
            
            if bit == '1':
                signal[mask_first_half] = 1
                signal[mask_second_half] = -1
            else:
                signal[mask_first_half] = -1
                signal[mask_second_half] = 1
        signal = signal * -1 # to match the book
        return signal
    
    def differential_manchester(self, bits, t):
        signal = np.zeros_like(t)
        half_bit = self.bit_duration / 2
        current_level = 1  # Start with high
        
        for i, bit in enumerate(bits):
            start = i * self.bit_duration
            mid = start + half_bit
            end = (i + 1) * self.bit_duration
            
            mask_first_half = (t >= start) & (t < mid)
            mask_second_half = (t >= mid) & (t < end)
            
            if bit == '0':
                # Transition at start of bit
                current_level *= -1
                signal[mask_first_half] = current_level
                # Transition at mid bit
                current_level *= -1
                signal[mask_second_half] = current_level
            else:
                # No transition at start of bit
                signal[mask_first_half] = current_level
                # Transition at mid bit
                current_level *= -1
                signal[mask_second_half] = current_level
        return signal
    
    def update_plot(self):
        # Get user input
        bits = self.bits_box.text
        encoding = self.encoding_radio.value_selected
        
        # Validate input
        if not all(b in ('0', '1') for b in bits):
            print("Error: Bit pattern should only contain 0s and 1s")
            return
        
        # Generate time axis
        t = self.generate_time_axis(bits)
        
        # Generate encoded signal based on selected scheme
        if encoding == 'NRZ-L':
            encoded = self.nrz_l(bits, t)
        elif encoding == 'NRZ-I':
            encoded = self.nrz_i(bits, t)
        elif encoding == 'AMI':
            encoded = self.ami(bits, t)
        elif encoding == 'Manchester':
            encoded = self.manchester(bits, t)
        elif encoding == 'Differential Manchester':
            encoded = self.differential_manchester(bits, t)
        
        # Plot bit pattern
        self.ax_bits.clear()
        for i, bit in enumerate(bits):
            self.ax_bits.plot([i, i+1], [int(bit), int(bit)], 'b-', linewidth=2)
        self.ax_bits.set_xlim(0, len(bits))
        self.ax_bits.set_ylim(-0.1, 1.1)
        self.ax_bits.set_title('Input Bit Pattern')
        self.ax_bits.set_xlabel('Bit Index')
        self.ax_bits.set_yticks([0, 1])
        self.ax_bits.grid(True)
        
        # Plot encoded signal
        self.ax_encoded.clear()
        self.ax_encoded.set_xlim(0, len(bits))
        self.ax_encoded.plot(t, encoded, 'b-')
        self.ax_encoded.set_title(f'{encoding} Encoded Signal')
        self.ax_encoded.set_xlabel('Time (s)')
        self.ax_encoded.set_ylabel('Amplitude')
        self.ax_encoded.set_yticks([-1, 0, 1])
        self.ax_encoded.grid(True)
        
        # Add bit separators
        for i in range(len(bits) + 1):
            self.ax_encoded.axvline(x=i * self.bit_duration, color='r', linestyle='--', alpha=0.3)
        
        plt.draw()

# Create and show the encoder
encoder = SignalEncoder()
plt.show()