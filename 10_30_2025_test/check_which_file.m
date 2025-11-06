clear;clc;close all
files = dir;
file_names = cell(length(files), 1);

file_ctr = 1;
for file = files'
    file_names{file_ctr} = file.name; 
    file_ctr = file_ctr + 1; 
    
    try
        if length(file.name) > 4
            if file.name(1:3) == ['log']
                file_end = file.name(end-6:end);
                
                warning off
                file_data = readtable(file.name);
                warning on
                
                %Throwaway first datapoint
                file_data(1,:) = [];
                
                % get things to plot
                time_series = zeros(height(file_data), 1);
                for ii = 2:height(file_data)
                    time_series(ii) = time_series(ii-1) + file_data.Time(ii);
                    if file_data.AngularPosition(ii) > 310
                        file_data.AngularPosition(ii) = file_data.AngularPosition(ii) - 360;
                    end
                    if file_data.PIDError(ii) > 360
                       file_data.PIDError(ii) = 0; 
                    end
                end
    
                % Plot it
                figure
                plot(time_series, file_data.AngularVelY)
                hold on
                grid on
                plot(time_series, 1 .* ([file_data.LSolenoid, file_data.RSolenoid] -0.5))
                axis padded
                legend('AngVel','LSolenoid', 'RSoleniod')
                xlabel('Time (s?)')
                ylabel('Angvel and soleniod state')
                title(sprintf('Data ending in %s', file.name(end-6:end)))
            end
        else
            continue
        end
    catch
        continue
    end
end

