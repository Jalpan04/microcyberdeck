# MicroCyberdeck

![GitHub top language](https://img.shields.io/github/languages/top/Jalpan04/microcyberdeck) ![GitHub repo size](https://img.shields.io/github/repo-size/Jalpan04/microcyberdeck) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A MicroPython-based mini-operating system and hardware interface simulation for a pocket-sized Cyberdeck. Built to run on an ESP32 or Raspberry Pi Pico inside the Wokwi hardware simulator, featuring an ILI9341 TFT display and keypad.

## Features

- **Cyberdeck Desktop UI**: A retro-futuristic dark-themed terminal UI featuring status bars, network indicators, memory monitors, and a launcher menu.
- **Modular App System**: Standardized Python application framework (`apps.py`) that handles transitions, drawing lifecycle, and state variables.
- **Pre-installed Core Apps**:
  - 🔋 **Battery Monitor (`battery_app.py`)**: Displays battery voltage, discharge rate, capacity estimation, and charging status.
  - 📡 **WiFi Manager (`wifi_app.py`)**: Simulates network scanning, signal strength (RSSI), access points list, and status.
  - 💾 **Storage Utility (`storage_app.py`)**: Monitors flash partition details, filesystem usage, and free sectors.
  - 🛠️ **System Diagnostics (`diag_app.py`)**: Visualizes real-time performance graphs, CPU speed, and free memory stats.
- **Hardware Integration**:
  - SPI TFT Display support using custom-tailored drivers for `ILI9341`.
  - Matrix keypad handling (`keypad.py`) to navigate the launcher and interact with apps.

## File Structure

```
├── main.py              # Main operating loop, inputs, and desktop rendering
├── apps.py              # Core App base class and application launcher
├── battery_app.py       # Battery status & monitoring screen
├── wifi_app.py          # WiFi scanner & connection status screen
├── storage_app.py       # Disk usage and partition info screen
├── diag_app.py          # System diagnostic & memory graphs screen
├── keypad.py            # Keypad input handling and mapping
├── ili9341.py           # SPI interface and display drivers
├── diagram.json         # Wokwi simulation schematic and wiring diagram
├── wokwi-project.txt    # Wokwi project reference
└── LICENSE              # MIT License
```

## How to Run in Wokwi Simulator

This project is configured to run out-of-the-box in the Wokwi browser-based hardware simulator.

1. Open the [Wokwi Simulator](https://wokwi.com).
2. Start a new ESP32 MicroPython project.
3. Upload all the `.py` files and `diagram.json` from this repository.
4. Run the simulation to view the desktop interface on the virtual ILI9341 display.
5. Use the keypad buttons to select and launch different apps.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
