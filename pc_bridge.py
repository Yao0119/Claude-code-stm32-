"""Send commands to Claude Code OLED display via COM7 serial port."""
import serial
import sys
import time

COMMANDS = ["INIT", "IDLE", "CODE", "DOCS", "THINK", "SEARCH", "EXPER", "ERROR", "STATUS"]

def send_cmd(cmd):
    if cmd.upper() not in COMMANDS:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(COMMANDS)}")
        return

    try:
        ser = serial.Serial('COM7', 115200, timeout=1)
        time.sleep(0.1)
        ser.write((cmd.upper() + '\n').encode())
        time.sleep(0.1)

        if cmd.upper() == 'STATUS':
            resp = ser.readline().decode().strip()
            print(f"STM32 Status: {resp}")
        else:
            print(f"Sent: {cmd.upper()} -> STM32")

        ser.close()
    except serial.SerialException as e:
        print(f"Error: Cannot open COM7 - {e}")
        print("Is the DAPmini connected? Is COM7 in use by another program?")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pc_bridge.py <command>")
        print(f"Commands: {', '.join(COMMANDS)}")
        print("Example: python pc_bridge.py CODE")
        sys.exit(1)

    send_cmd(sys.argv[1])
