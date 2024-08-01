# AVR Programmer GUI

A standalone GUI application for programming AVR microcontrollers using AVRDude. This tool allows users to select the COM port, baud rate, and microcontroller type, and upload firmware files (.hex or .elf) to the microcontroller. The application is built with Python and Tkinter and packaged into a standalone executable using PyInstaller.

## Features

- **User-Friendly GUI**: Easy-to-use graphical interface for selecting COM port, baud rate, microcontroller type, and firmware file.
- **Supported Microcontrollers**: Supports a wide range of AVR microcontrollers (e.g., ATmega328p, ATmega328pb, ATmega2560, ATmega32u4).
- **Integrated AVRDude**: Includes AVRDude executable and configuration for seamless programming.
- **Modern Look**: Uses `ttkthemes` for a modern and attractive UI design.
- **Standalone Executable**: Distributed as a single executable file, no Python installation required.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/avr-programmer-gui.git
   cd avr-programmer-gui
