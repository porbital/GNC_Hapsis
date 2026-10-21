
import digitalio
import busio


# ============================================================
# IMU-Teensy Integration code for GNC Icarus w/ simulation
#
# By: Steven Sutton
# Created: 10/14/2024
#
# ============================================================

#addresses
IMU = 0x29
UNIT_SEL = 0x3b
OPR_MODE = 0x3d
PWR_MODE = 0x3e
GYR_Config_0 = 0x0a
GYR_Config_1 = 0x0b
GYR_DATA_X_LSB = 0x14
#all gyroscopic data goes to address 0x19 X,Y,Z at 2 bytes per
QUA_DATA_W_LSB = 0x20
#all quaternion data goes to address 0x27 W,X,Y,Z 2 bytes per

#IMU Configuration
with SMBus(1) as bus:
    #operating mode to GYROONLY
    bus.write_byte_data(IMU, OPR_MODE, 0b00000011)
    #unit selection (m/s^2, DPS, Degrees, Celsius)
    bus.write_byte_data(IMU, UNIT_SEL, 0b00000110)
    

def main():
    with SMBus(1) as bus:
        control_law()

            
def gyro_x():
    with SMBus(1) as bus:
        x_dps = bus.read_byte_data(IMU, GYR_DATA_X_LSB + 4)
    return x_dps

def control_law():
    #put control law here

if __name__ == "__main__":
    main()
