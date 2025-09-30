# ============================================================
# PID Class for GNC Hapsis
#
# By: Wesley Kron
# Created: 1/30/2025
#
# ============================================================
#
class PID:
    def __init__(self, Kp, Ki, Kd, setpoint):
        """
        Initialize the PID controller with tuning parameters.

        :param Kp: Proportional constant
        :param Ki: Integral constant
        :param Kd: Derivative constant
        :param setpoint: Desired heading (setpoint)
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.heading = 0
        self.previous_error = 0
        self.integral = 0

    def compute(self, current_heading, dt):
        """
        Compute the PID control output based on current temperature.

        :param current_heading: The current measured temperature
        :param dt: Time interval between measurements (in seconds)
        :return: The control output (e.g., power level to heater/cooler)
        """
        # Calculate the error (difference between setpoint and current temperature)
        error = self.setpoint - current_heading

        # Proportional term
        P = self.Kp * error

        # Integral term
        self.integral += error * dt
        I = self.Ki * self.integral

        # Derivative term
        derivative = (error - self.previous_error) / dt if dt > 0 else 0
        D = self.Kd * derivative

        # Update previous error
        self.previous_error = error

        # Total output
        output = P + I + D
        return output
    
    def get_Avionics(self, heading):
        # implement an example avionics data and method to receive data
        # understand avionics protocol
        self.heading = heading
        return True


# pid = PID(Kp=1.0, Ki=0.1, Kd=0.01, setpoint=22.0)
