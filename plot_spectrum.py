import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox

class SignalPlotter:
    def __init__(self):
        # Initialize parameters
        self.frequencies = [1, 3, 5]  # Default frequencies in Hz
        self.amplitudes = [1, 0.5, 0.3]  # Default amplitudes
        self.dc_offset = 0.0  # DC component
        self.sampling_rate = 1000  # Samples per second
        self.duration = 1.0  # Duration in seconds
        
        # Create time array
        self.t = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False)
        
        # Create figure and axes
        self.fig, (self.ax_signal, self.ax_spectrum) = plt.subplots(2, 1, figsize=(10, 8))
        plt.subplots_adjust(bottom=0.35)
        
        # Create UI elements
        self.create_ui()
        
        # Plot initial signal
        self.update_plot()
        
    def create_ui(self):
        # Add frequency input boxes
        ax_freq1 = plt.axes([0.15, 0.25, 0.2, 0.05])
        ax_freq2 = plt.axes([0.4, 0.25, 0.2, 0.05])
        ax_freq3 = plt.axes([0.65, 0.25, 0.2, 0.05])
        
        self.freq1_box = TextBox(ax_freq1, 'Freq 1 (Hz)', initial=str(self.frequencies[0]))
        self.freq2_box = TextBox(ax_freq2, 'Freq 2 (Hz)', initial=str(self.frequencies[1]))
        self.freq3_box = TextBox(ax_freq3, 'Freq 3 (Hz)', initial=str(self.frequencies[2]))
        
        # Add amplitude input boxes
        ax_amp1 = plt.axes([0.15, 0.15, 0.2, 0.05])
        ax_amp2 = plt.axes([0.4, 0.15, 0.2, 0.05])
        ax_amp3 = plt.axes([0.65, 0.15, 0.2, 0.05])
        
        self.amp1_box = TextBox(ax_amp1, 'Amp 1', initial=str(self.amplitudes[0]))
        self.amp2_box = TextBox(ax_amp2, 'Amp 2', initial=str(self.amplitudes[1]))
        self.amp3_box = TextBox(ax_amp3, 'Amp 3', initial=str(self.amplitudes[2]))
        
        # Add DC offset input box
        ax_dc = plt.axes([0.15, 0.05, 0.2, 0.05])
        self.dc_box = TextBox(ax_dc, 'DC Offset', initial=str(self.dc_offset))
        
        # Add update button
        ax_update = plt.axes([0.4, 0.05, 0.2, 0.05])
        self.update_button = Button(ax_update, 'Update Plot')
        self.update_button.on_clicked(self.on_update)
        
        # Set callback functions for text boxes
        self.freq1_box.on_submit(self.on_update)
        self.freq2_box.on_submit(self.on_update)
        self.freq3_box.on_submit(self.on_update)
        self.amp1_box.on_submit(self.on_update)
        self.amp2_box.on_submit(self.on_update)
        self.amp3_box.on_submit(self.on_update)
        self.dc_box.on_submit(self.on_update)
    
    def on_update(self, event=None):
        try:
            # Update frequencies
            self.frequencies[0] = float(self.freq1_box.text)
            self.frequencies[1] = float(self.freq2_box.text)
            self.frequencies[2] = float(self.freq3_box.text)
            
            # Update amplitudes
            self.amplitudes[0] = float(self.amp1_box.text)
            self.amplitudes[1] = float(self.amp2_box.text)
            self.amplitudes[2] = float(self.amp3_box.text)
            
            # Update DC offset
            self.dc_offset = float(self.dc_box.text)
            
            self.update_plot()
        except ValueError:
            print("Please enter valid numbers")
    
    def generate_signal(self):
        signal = np.zeros_like(self.t) + self.dc_offset / 2  # Start with DC component
        for freq, amp in zip(self.frequencies, self.amplitudes):
            if freq > 0:  # Only add if frequency is positive
                signal += amp * np.sin(2 * np.pi * freq * self.t)
        return signal
    
    def compute_spectrum(self, signal):
        n = len(signal)
        fft_result = np.fft.fft(signal)
        fft_magnitude = np.abs(fft_result) / n  * 2 # Normalize
        freqs = np.fft.fftfreq(n, 1/self.sampling_rate)
        
        # Only return the first half (positive frequencies)
        half_n = n // 2
        return freqs[:half_n], fft_magnitude[:half_n]
    
    def update_plot(self):
        # Generate signal
        signal = self.generate_signal()
        
        # Compute spectrum
        freqs, spectrum = self.compute_spectrum(signal)
        
        # Plot time domain signal
        self.ax_signal.clear()
        self.ax_signal.plot(self.t, signal)
        self.ax_signal.set_title(f'Time Domain Signal (DC offset = {self.dc_offset})')
        self.ax_signal.set_xlabel('Time (s)')
        self.ax_signal.set_ylabel('Amplitude')
        self.ax_signal.grid(True)
        
        # Plot frequency spectrum
        self.ax_spectrum.clear()
        self.ax_spectrum.stem(freqs, spectrum, markerfmt=' ', basefmt=" ")
        self.ax_spectrum.set_title('Frequency Spectrum')
        self.ax_spectrum.set_xlabel('Frequency (Hz)')
        self.ax_spectrum.set_ylabel('Magnitude')
        self.ax_spectrum.set_xlim(0, max(10, max(self.frequencies) * 1.5))
        self.ax_spectrum.grid(True)
        
        # Highlight the component frequencies
        self.ax_spectrum.axvline(x=0, color='g', linestyle='--', alpha=0.5, label='DC component')
        for freq, amp in zip(self.frequencies, self.amplitudes):
            if freq > 0:
                self.ax_spectrum.axvline(x=freq, color='r', linestyle='--', alpha=0.3)
        
        self.ax_spectrum.legend()
        plt.draw()

# Create and show the plotter
plotter = SignalPlotter()
plt.show()