# Demoes

Demo code for basic communication concepts.


## Installation

- `numpy`
- `matplotlib`


### Installation Instructions

These instructions assume you are using a Python virtual environment to manage dependencies.

1. Clone the Repository

    Windows (PowerShell or Command Prompt)

    ```powershell
    # Clone the repo
    git clone https://github.com/martimy/comm_demos.git
    cd comm_demos
    ```

    macOS/Linux (Terminal)
    ```bash
    # Clone the repo
    git clone https://github.com/martimy/comm_demos.git
    cd comm_demos
    ```

2. Set Up a Python Virtual Environment  

    On Windows:  
    ```powershell
    # Create a virtual environment
    python -m venv signal_env

    # Activate it
    .\signal_env\Scripts\activate
    ```

    On macOS/Linux:  
    ```bash
    # Create a virtual environment
    python3 -m venv signal_env

    # Activate it
    source signal_env/bin/activate
    ```

3. Install Required Dependencies  

    Run the following command inside the activated virtual environment:  
    ```bash
    pip install -r requirements. txt
    ```

4. Download and Run the Scripts  

    Follow the instructions in one of the sections below.


5. Deactivate the Virtual Environment  

    When done, exit the environment:  
    ```bash
    deactivate
    ```

## plot_encoding.py

This code allows users to input a binary bit pattern and visualize how it would be encoded using different line encoding schemes commonly used in digital communications.

### How to Use:

1. Run the Script:  

    ```
    python3 plot_encoding.py
    ```

2. Input Bit Pattern:  
   Enter a binary string (e.g., `11010`) in the text box labeled "Bit Pattern."

3. Select Encoding Scheme:  
   Click one of the radio buttons (e.g., "Manchester") to choose the encoding method.

4. View Results:  
   The plots update automatically to show:
   - The input bits as a digital waveform.
   - The encoded signal with transitions based on the selected scheme.

## plot_sepectrum.py

This code allows users to visualize a composite signal in both the time domain and frequency domain, with interactive controls to adjust signal parameters.

### How to Use:

1. Run the Script:  

    ```
    python3 plot_spectrum.py
    ```

2. Adjust Parameters:
   - Enter frequencies in the "Freq X (Hz)" boxes.
   - Set amplitudes in the "Amp X" boxes.
   - Add a DC offset if desired.

3. Update the Plot:
   - Click the "Update Plot" button or press Enter after typing in a text box.

4. View Results:
   - The time-domain plot shows the composite signal.
   - The frequency spectrum displays peaks at the input frequencies, with magnitudes proportional to their amplitudes.
   - A green dashed line marks the DC component (if offset ≠ 0).


## plot_qam.py

This code allows users to input a binary bit pattern, select a QAM modulation order, and visualize the modulated signal along with its constellation diagram.

### How to Use:

1. Run the Script:  

    ```
    python3 plot_qam.py
    ```

2. Input Bit Pattern:  
   Enter a binary string (e.g., `0010111001`) in the "Bit Pattern" text box.

3. Select QAM Order:  
   Choose a modulation scheme in the "QAM Order" text box.

4. Update the Plot:  
   Click the "Update Plot" button or press Enter after typing.

5. View Results:
   - The bit pattern is displayed as a digital waveform.
   - The modulated signal shows the combined I/Q components.
   - The constellation diagram maps symbols to their I/Q coordinates, labeled with their binary representations.

