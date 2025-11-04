clear;clc;close all
data = readtable("log_20000101_000837.csv");

% Notice that first data point seems invalid
data(1,:) = [];

time_series = zeros(height(data), 1);
for ii = 2:height(data)
    time_series(ii) = time_series(ii-1) + data.Time(ii);
    if data.AngularPosition(ii) > 310
        data.AngularPosition(ii) = data.AngularPosition(ii) - 360;
    end
    if data.PIDError(ii) > 360
       data.PIDError(ii) = 0; 
    end
end

setpoint =  data.AngularPosition + data.PIDError;
figure
plot(time_series, setpoint)

figure
plot(time_series, data.AngularPosition)
xlabel('time(s)')
ylabel('Angular position (deg)')
grid on

figure
plot(time_series, (data.PIDError))
xlabel('time(s)')
ylabel('PID ERROR (deg)')
grid on 
hold on
plot(time_series, 50 .* ([data.LSolenoid, data.RSolenoid] -0.5))
plot(time_series, data.P)
axis padded
legend('PID error','LSolenoid', 'RSoleniod', 'P')

% % Calculate the primary rotation angle (Z) and adjust X and Y accordingly
% primary_angle = 15;
% data.AngularVelX = data.AngularVelX .* cosd(primary_angle);
% data.AngularVelY = data.AngularVelY .* sind(primary_angle);
% data.AngularVelZ = data.AngularVelZ; % Keep Z as is for primary rotation
angVel = [data.AngularVelX, data.AngularVelY, data.AngularVelZ];

figure
plot(time_series(2:end), diff(data.AngularPosition)./1)
hold on
plot(time_series, angVel)
plot(time_series, vecnorm(angVel, 2, 2) .* sign(angVel(:,2)))
axis padded
grid on
legend('Derivatve', 'X', 'Y', 'Z')







