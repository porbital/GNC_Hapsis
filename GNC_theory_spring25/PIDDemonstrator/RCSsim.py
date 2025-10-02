import numpy as np
import matplotlib.pyplot as plt

# I1 body
I1 = 0.082

# I2 flywheel
M = 2 # kg
I2 = M * (0.078359 ** 2)

# body A matrix
A = np.array(
    [
        [0,0,1,0],
        [0,0,0,1],
        [0,0,0,0],
        [0,0,0,0]
    ]
)

# body B matrix
B = np.array(
    [
        0,
        0,
        -1/I1,
        1/I2
    ]
)

# initial state
x = np.array([
    0, # body theta
    0, # flywheel theta
    2*np.pi*3.5, # body theta dot
    0 # flywheel theta dot
], dtype=np.float64)

# torque input
u = 0

# PID for kP,  kI, kD
kP = 10
kI = 0
kD = 1.6248

setpoint = 2

body_pos = []
flywheel_pos = []
body_vel = []
flywheel_vel = []
u_int_plot = []

u_int = 0

dt = 0.001
for i in range(10000):
    # append to array
    body_pos.append(x[0])
    flywheel_pos.append(x[1])
    body_vel.append(x[2] * 9.549297)
    flywheel_vel.append(x[3] * 9.549297)
    u_int_plot.append(u_int)

    # update state
    x_dot = A @ x + B * u
    x += x_dot * dt

    #e = x[0]
    
    e = (x[0] - setpoint) % (2 * np.pi)
    if e > np.pi:
        e -= 2*np.pi
    elif e < -np.pi:
        e += 2*np.pi

    u_int += e * dt
    u_int = np.clip(u_int, -3, 3)

    uo = kP * e + kI * u_int + kD * x[2]
    u = np.clip(uo, -1, 1)

print(f"Max flywheel speed: {max(flywheel_vel) * 9.549297}")
print(f"Final flywheel speed: {x[3] * 9.549297}")
print(f"Final body speed: {x[2] * 9.549297}")

plt.plot(body_pos)
plt.title("Body Position")
plt.show()

plt.plot(flywheel_pos)
plt.title("Flywheel Position")
plt.show()

plt.plot(body_vel)
plt.title("Body Velocity")
plt.show()

plt.plot(flywheel_vel)
plt.title("Flywheel Velocity")
plt.show()

plt.plot(u_int_plot)
plt.title("Integral of Error")
plt.show()
