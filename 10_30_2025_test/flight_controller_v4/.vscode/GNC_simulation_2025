import numpy as np
import matplotlib.pyplot as plt
from PID import PID

# ============================================================
# PID Controller for GNC Hapsis w/ simulation
#
# By: Wesley Kron
# Created: 1/30/2025
#
# ============================================================

## Initializations
tf = 20  # final time for the simulation
t = np.linspace(0, tf, 1000)  # simulation time
dt = tf / 1000  # time step

# User Setting 
turb = 10 # Set Turbulence 
setpoint = np.pi # Heading Setpoint IN RADIANS

# Cylinder data
M = 2.0  # (kg) weight of cylinder
R = 0.25  # (m) radius of the cylinder
I = 0.5 * M * R**2  # Moment of inertia for a solid cylinder (I = 1/2 * M * R^2)
print(f"Moment of Inertia I: {I} kg*m^2")

# State variable initialization
theta = [0]  # position (initial angle in radians)
omega = [0]  # velocity (initial angular velocity)
alpha = [0]  # acceleration (initial angular acceleration)
tau = [0]  # torque (initial torque)
tau_control = 0  # initial control torque

# natural spin
tau_natural = np.random.uniform(-turb,turb)  # no random torque for now

# Initialize the PID loop
pid = PID(Kp=0.8, Ki=0.3, Kd=0.5, setpoint=setpoint)  # Target setpoint is pi radians (180 degrees)

# Simulation loop
for i in range(len(t) - 1):  # Use len(t)-1 to avoid going out of range
    # Run PID loop to compute control output
    output = pid.compute(theta[i], dt)
    
    # Control Law: Apply torque based on PID output
    if abs(output) > 0:
        if output > 0:
            # Apply positive torque to slow down negative spin
            tau_control = 1.5
        else:
            # Apply negative torque to slow down positive spin
            tau_control = -1.5
    tau_natural = np.random.uniform(-1,1)  # no random torque for now
    # Update total torque (control torque + natural torque)
    tau.append(tau_control + tau_natural)

    # Integrate acceleration, velocity, and position using Euler's method
    alpha.append(tau[i] / I)  # Update alpha based on torque
    omega.append(omega[i] + alpha[i] * dt)  # Update omega based on angular acceleration
    theta.append(theta[i] + omega[i] * dt + 0.5 * alpha[i] * dt**2)  # Update position based on velocity and acceleration

    # Print some debug output (optional, for tracking behavior)
    if i % 100 == 0:  # Print every 100 iterations for debugging
        print(f"t = {t[i]:.2f}s, theta = {theta[i]:.2f}, omega = {omega[i]:.2f}, tau = {tau[i]:.3f}")

# Plotting the results (position over time)
plt.figure("Position vs Time")
plt.plot(t, theta)

# Adding lines to illustrate (+/-) 5 degree of setpoint requirement
plt.axhline((setpoint-(5*(np.pi/180))), color='k', linestyle='--') 
plt.axhline((setpoint+(5*(np.pi/180))), color='k', linestyle='--')

plt.xlabel("Time [s]")
plt.ylabel("Position (Theta) [rad]")
plt.title("PID Controlled Rotation (Position vs Time)")
plt.grid(True)
plt.show()
