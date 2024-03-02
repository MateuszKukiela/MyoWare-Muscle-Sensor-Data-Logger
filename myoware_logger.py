import serial
import time
import keyboard
from collections import deque
from typing import Deque
import csv
import os

ARDUINO_PORT = '/dev/cu.usbserial-110'  # Replace with your Arduino port
BAUD_RATE = 9600  # Must match the baud rate in the Arduino code
BUFFER_LEN = 100  # Adjust based on sensor data rate
MAX_PRESS = 25  # Number of presses to record
CSV_FILE_PATH = "data/sensor_data.csv"  # Path to save the CSV file


def initialize_serial(port: str, baud_rate: int) -> serial.Serial:
    """
    Initializes the serial connection to the Arduino.

    :param port: The port Arduino is connected to (e.g., '/dev/tty.usbmodemXXXX').
    :param baud_rate: The baud rate for serial communication.
    :return: The initialized serial connection.
    """
    return serial.Serial(port, baud_rate)


def save_data(data_buffer: Deque[str], press_num: int) -> None:
    """
    Saves the buffered data to a text file and appends the same data as a single row to a CSV file.

    :param data_buffer: The deque holding the sensor data.
    :param press_num: The current press count to label the saved data file.
    """
    # Save to text file
    txt_filename = f"data/sensor_data_press_{press_num}.txt"
    with open(txt_filename, "a") as txt_file:
        for line in data_buffer:
            txt_file.write(f"{line}\n")
    print(f"Data saved to text file for press {press_num}")

    # Ensure the directory exists for the CSV file
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)

    # Append to CSV file as a single row
    with open(CSV_FILE_PATH, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Convert the deque to a list and write as a single row
        csv_writer.writerow(list(data_buffer))
    print("Data appended to CSV file in a single row")


def main():
    """
    Main function to execute the MyoWare Muscle Sensor data logging.
    """
    press_count = 0
    ser = initialize_serial(ARDUINO_PORT, BAUD_RATE)
    data_buffer: Deque[str] = deque(maxlen=BUFFER_LEN)

    try:
        time.sleep(2)  # Stabilize connection
        print("Press the space key to save data...")

        key_pressed = False
        post_press_time = 0

        while press_count < MAX_PRESS:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                data_buffer.append(line)

                if keyboard.is_pressed('space') and not key_pressed:
                    press_count += 1
                    print(f"Space key pressed. Saving data for press {press_count}...")
                    save_data(data_buffer, press_count)
                    key_pressed = True
                    post_press_time = time.time()

                if key_pressed and (time.time() - post_press_time) <= 1:
                    data_buffer.append(line)
                elif key_pressed and (time.time() - post_press_time) > 1:
                    save_data(data_buffer, press_count)
                    key_pressed = False
                    if press_count < MAX_PRESS:
                        print(f"{MAX_PRESS - press_count} presses remaining...")

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        ser.close()
        print("Serial port closed")


if __name__ == "__main__":
    main()
