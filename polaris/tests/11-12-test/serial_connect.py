import serial
import serial.tools.list_ports
from datetime import datetime
import time
import os


def find_circuitpython_port():
    """
    Automatically find the CircuitPython device port.
    Returns the port name or None if not found.
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # CircuitPython devices typically show up with these identifiers
        if "CircuitPython" in port.description or "USB Serial" in port.description:
            return port.device
    return None


def log_serial_data(port=None, baudrate=115200, log_dir="serial_logs"):
    """
    Open a serial port and log data to a timestamped file.

    Args:
        port: Serial port name (e.g., 'COM3' or '/dev/ttyACM0').
              If None, will attempt to auto-detect.
        baudrate: Communication speed (default: 115200)
        log_dir: Directory to store log files
    """

    # Create log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Auto-detect port if not specified
    if port is None:
        print("Searching for CircuitPython device...")
        port = find_circuitpython_port()
        if port is None:
            print("\nAvailable ports:")
            for p in serial.tools.list_ports.comports():
                print(f"  {p.device}: {p.description}")
            raise Exception("CircuitPython device not found. Please specify port manually.")

    print(f"Connecting to {port} at {baudrate} baud...")

    # Create incremental filename
    test_number = 1
    while True:
        log_filename = os.path.join(log_dir, f"test{test_number}.csv")
        if not os.path.exists(log_filename):
            break
        test_number += 1

    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for connection to stabilize

        print(f"Connected! Logging to: {log_filename}")
        print("Press Ctrl+C to stop logging.\n")

        with open(log_filename, 'w') as log_file:
            # Write header
            log_file.write(f"Serial Log Started: {datetime.now()}\n")
            log_file.write(f"Port: {port}, Baudrate: {baudrate}\n")
            log_file.write("-" * 50 + "\n\n")
            log_file.flush()

            while True:
                if ser.in_waiting > 0:
                    # Read line from serial port
                    line = ser.readline().decode('utf-8', errors='ignore').strip()

                    if line:  # Only log non-empty lines
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        log_entry = f"[{timestamp}] {line}"

                        # Print to console
                        print(log_entry)

                        # Write to file
                        log_file.write(log_entry + "\n")
                        log_file.flush()  # Ensure data is written immediately

                time.sleep(0.01)  # Small delay to prevent CPU spinning

    except KeyboardInterrupt:
        print("\n\nLogging stopped by user.")

    except serial.SerialException as e:
        print(f"\nSerial error: {e}")
        print("Check that the device is connected and the port is correct.")

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
        print(f"Log saved to: {log_filename}")


if __name__ == "__main__":
    # Option 1: Auto-detect CircuitPython device
    # log_serial_data()

    # Option 2: Specify port manually (uncomment and modify as needed)
    # Windows: log_serial_data(port="COM3")
    # Linux: log_serial_data(port="/dev/ttyACM0")
    # Mac:
    log_serial_data(port="/dev/cu.usbmodem101")