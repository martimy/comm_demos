import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox

class QAM_Modulator:
    def __init__(self):
        # Initialize parameters
        self.carrier_freq = 10  # Hz
        self.symbol_rate = 2  # symbols per second
        self.sampling_rate = 1000  # samples per second
        self.duration = 2  # seconds
        self.default_bits = "0010111001"  # Default bit pattern
        
        # Create time array
        self.t = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False)
        
        # Create figure
        self.fig = plt.figure(figsize=(14, 10))
        
        # Create UI elements
        self.create_ui()
        
        # Plot initial signal
        self.update_plot()
    
    def create_ui(self):
        # Create axes for plots
        self.ax_bits = plt.subplot2grid((4, 2), (0, 0), colspan=2)
        # self.ax_i = plt.subplot2grid((4, 2), (1, 0))
        # self.ax_q = plt.subplot2grid((4, 2), (1, 1))
        self.ax_modulated = plt.subplot2grid((4, 2), (1, 0), colspan=2)
        self.ax_constellation = plt.subplot2grid((4, 1), (2, 0), rowspan=2)
        # self.ax_spectrum = plt.subplot2grid((4, 2), (3, 0), colspan=2)
        
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.2, hspace=0.5)
        
        # Add bit pattern input
        ax_bits_input = plt.axes([0.2, 0.1, 0.6, 0.05])
        self.bits_box = TextBox(ax_bits_input, 'Bit Pattern:', initial=self.default_bits)
        
        # Add modulation order selection
        ax_mod_order = plt.axes([0.2, 0.05, 0.3, 0.05])
        self.mod_order_box = TextBox(ax_mod_order, 'QAM Order (4, 16, 64):', initial="4")
        
        # Add update button
        ax_update = plt.axes([0.6, 0.05, 0.2, 0.05])
        self.update_button = Button(ax_update, 'Update Plot')
        self.update_button.on_clicked(self.on_update)
        
        # Set callback functions
        self.bits_box.on_submit(self.on_update)
        self.mod_order_box.on_submit(self.on_update)
    
    def on_update(self, event=None):
        try:
            self.update_plot()
        except ValueError as e:
            print(f"Error: {e}")
    
    def binary_to_symbols(self, bits, order):
        # Convert bit string to symbols based on QAM order
        if order == 4:
            symbol_bits = 2
            constellation = {
                '00': (-1, -1),
                '01': (-1, 1),
                '10': (1, -1),
                '11': (1, 1)
            }
        elif order == 16:
            symbol_bits = 4
            constellation = {
                '0000': (-3, -3),
                '0001': (-3, -1),
                '0010': (-3, 3),
                '0011': (-3, 1),
                '0100': (-1, -3),
                '0101': (-1, -1),
                '0110': (-1, 3),
                '0111': (-1, 1),
                '1000': (3, -3),
                '1001': (3, -1),
                '1010': (3, 3),
                '1011': (3, 1),
                '1100': (1, -3),
                '1101': (1, -1),
                '1110': (1, 3),
                '1111': (1, 1)
            }
        elif order == 64:
            symbol_bits = 6
            # Simplified 64-QAM constellation
            constellation = {}
            values = [-7, -5, -3, -1, 1, 3, 5, 7]
            for i in range(64):
                bits = format(i, '06b')
                x = values[i % 8]
                y = values[i // 8]
                constellation[bits] = (x, y)
        else:
            raise ValueError("Supported QAM orders: 4, 16, 64")
        
        # Pad bits with zeros if needed
        padding = (symbol_bits - (len(bits) % symbol_bits)) % symbol_bits
        padded_bits = bits + '0' * padding
        
        # Split into symbols
        symbols = []
        for i in range(0, len(padded_bits), symbol_bits):
            symbol_bits_str = padded_bits[i:i+symbol_bits]
            symbols.append(constellation[symbol_bits_str])
        
        return symbols, constellation
    
    def modulate_qam(self, symbols, order):
        # Create I and Q signals
        samples_per_symbol = int(self.sampling_rate / self.symbol_rate)
        total_symbols = len(symbols)
        
        # Create baseband signals
        i_signal = np.zeros_like(self.t)
        q_signal = np.zeros_like(self.t)
        
        for i, (i_val, q_val) in enumerate(symbols):
            start = i * samples_per_symbol
            end = (i + 1) * samples_per_symbol
            if end > len(self.t):
                end = len(self.t)
            i_signal[start:end] = i_val
            q_signal[start:end] = q_val
        
        # Modulate with carrier
        carrier_i = np.cos(2 * np.pi * self.carrier_freq * self.t)
        carrier_q = np.sin(2 * np.pi * self.carrier_freq * self.t)
        
        modulated = i_signal * carrier_i + q_signal * carrier_q
        
        return i_signal, q_signal, modulated
    
    def plot_constellation(self, constellation, ax):
        ax.clear()
        for bits, (i, q) in constellation.items():
            ax.plot(i, q, 'bo')
            ax.text(i, q, bits, fontsize=8)
        ax.axhline(0, color='k', linestyle='--', alpha=0.3)
        ax.axvline(0, color='k', linestyle='--', alpha=0.3)
        ax.grid(True)
        ax.set_title('Constellation Diagram')
        ax.set_xlabel('In-phase (I)')
        ax.set_ylabel('Quadrature (Q)')
    
    def compute_spectrum(self, signal):
        n = len(signal)
        fft_result = np.fft.fft(signal)
        fft_magnitude = np.abs(fft_result) / n
        freqs = np.fft.fftfreq(n, 1/self.sampling_rate)
        
        # Only return positive frequencies
        half_n = n // 2
        return freqs[:half_n], fft_magnitude[:half_n]
    
    def update_plot(self):
        # Get user input
        bits = self.bits_box.text
        order = int(self.mod_order_box.text)
        
        if order not in [4, 16, 64]:
            raise ValueError("QAM order must be 4, 16, or 64")
        
        # Convert bits to symbols
        symbols, constellation = self.binary_to_symbols(bits, order)
        
        # Modulate
        i_signal, q_signal, modulated = self.modulate_qam(symbols, order)
        
        # Compute spectrum
        freqs, spectrum = self.compute_spectrum(modulated)
        
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

        # Plot modulated signal
        self.ax_modulated.clear()
        self.ax_modulated.plot(self.t, modulated)
        self.ax_modulated.set_title(f'{order}-QAM Modulated Signal')
        self.ax_modulated.set_xlabel('Time (s)')
        self.ax_modulated.set_ylabel('Amplitude')
        self.ax_modulated.grid(True)
        
        # Plot I and Q signals
        # self.ax_i.clear()
        # self.ax_i.plot(self.t, i_signal)
        # self.ax_i.set_title('In-phase (I) Signal')
        # self.ax_i.set_xlabel('Time (s)')
        # self.ax_i.set_ylabel('Amplitude')
        # self.ax_i.grid(True)
        
        # self.ax_q.clear()
        # self.ax_q.plot(self.t, q_signal)
        # self.ax_q.set_title('Quadrature (Q) Signal')
        # self.ax_q.set_xlabel('Time (s)')
        # self.ax_q.set_ylabel('Amplitude')
        # self.ax_q.grid(True)
        
        # Plot constellation diagram
        self.plot_constellation(constellation, self.ax_constellation)
                
        # Plot spectrum
        # self.ax_spectrum.clear()
        # self.ax_spectrum.plot(freqs, spectrum)
        # self.ax_spectrum.set_title('Frequency Spectrum')
        # self.ax_spectrum.set_xlabel('Frequency (Hz)')
        # self.ax_spectrum.set_ylabel('Magnitude')
        # self.ax_spectrum.set_xlim(0, 2 * self.carrier_freq)
        # self.ax_spectrum.grid(True)
        
        plt.draw()

# Create and show the modulator
qam = QAM_Modulator()
plt.show()