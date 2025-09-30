clear
clc

% Max PSI
r = .25; % radium [m]
m = 22; % mass [kg]

I = .5 * m * r^2; % inertia
thrust = 1.75 * 2; % max thrust per nozzle [N]
torque = r * thrust; % Nm

omega = 2*pi; % rad/s

dt = I * omega / torque;
maxtime = 20 / 2; % seconds
disp(dt);