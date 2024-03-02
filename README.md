# MyoWare Muscle Sensor Data Logger

This Python project interfaces with a MyoWare® 2.0 Muscle Sensor through an Arduino to capture muscle movement data. It's designed to log data one second before and after pressing the space key, allowing for 25 such captures with a human-readable countdown during data collection.

## Prerequisites

Before starting, ensure you have the following:

- **Hardware**: MyoWare® 2.0 Muscle Sensor, Arduino board (e.g., Uno, Mega), connecting wires.
- **Software**: Arduino IDE, Python 3.x.

## Setup Guide

### 1. Arduino Configuration

- Connect the MyoWare Muscle Sensor to the Arduino, ensuring the signal pin is connected to the `A0` analog input.
- Upload the provided Arduino sketch to read sensor data and transmit it over the serial connection.

### 2. Environment Setup

#### Install Pipenv

If not already installed, use pip to install `pipenv`:

```bash
pip install pipenv
```

#### Initialize Pipenv and Install Dependencies

Navigate to your project directory and set up `pipenv` with the required Python version and dependencies:

```bash
pipenv install
```

### 3. Running the Data Logger

Activate the `pipenv` shell to work within the virtual environment:

```bash
pipenv shell
```

Then, run the Python script to start logging data:

```bash
python myoware_logger.py
```

#### Key Presses

- Press the **space key** to trigger data capture. The script logs data from one second before and after each keypress.
- The script provides a countdown during the one-second post-press data collection and displays the number of remaining presses.
- Data for each press is saved in a uniquely named file within the project directory.

#### Termination

- The script concludes after 25 key presses or can be manually terminated using `Ctrl+C`.

## Customization

- Modify the `buffer_length` in the script to match your sensor's data rate, ensuring it holds approximately one second of data.
- Adjust the serial port in the script to match your Arduino's connection port.

## Troubleshooting

- Ensure you have the correct permissions to access the serial port on your system.
- The script requires the terminal window to be in focus for detecting key presses due to the nature of the `keyboard` library.

## Contributing

Your contributions are welcome! Please fork the repository, make your changes, and submit a pull request with a description of your updates.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.
