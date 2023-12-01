clear;
close all;
% Specified input file (degraded) and output file (restored)
input_file = 'degraded.wav';
output_file = 'output.wav';
clean_file = 'clean.wav';
detection_file = 'detection.wav';  % New file to save click detection
% Read the clean audio data
clean_audio = audioread(clean_file);
% Defined block size, duration, and sampling rate
block_size = 1000; 
duration = 10;     % Total duration provided in the audio
sample_rate = 8000; % Minimum sampling rate of 8KHz
% Read the degraded audio data
[x, sample_rate] = audioread(input_file);
% Initialize an array to store the restored audio
restored_audio = zeros(size(x));
% Define a threshold 
click_threshold = 0.45;
% Initialize variable to store the total number of clicks
total_clicks = 0;
% Initialize vector to store click detection
click_detection = zeros(size(x));
% Process the audio in blocks and remove clicks using AR model
for start_sample = 1:block_size:length(x)
    end_sample = min(start_sample + block_size - 1, length(x));
    block = x(start_sample:end_sample);
    
    % Detect clicks by comparing amplitude to the threshold
    clicks = abs(block) > click_threshold;
    
    % Update the total number of clicks
    total_clicks = total_clicks + sum(clicks);
    
    % Update click detection vector
    click_detection(start_sample:end_sample) = clicks;
    
    % Apply AR modeling to remove clicks
    block(clicks) = 0;
    
    % Estimate AR coefficients using LS
    order = 3; % Set the desired order
    reference_block = x(start_sample:min(start_sample + block_size - 1, length(x)));
    coeffs = estimateARCoefficients(reference_block, order);
    
    % Use interpolateAR to fill in missing values
    block = interpolateAR(block, clicks, coeffs);
    
    % Store the processed block in the restored audio
    restored_audio(start_sample:end_sample) = block;
end
save('detect.mat', 'click_detection');
% Calculate Mean Squared Error (MSE)
mse = immse(clean_audio, restored_audio);
% Calculate Mean Absolute Error (MAE)
mae = mean(abs(clean_audio - restored_audio));
% Display the performance metrics
fprintf('Mean Squared Error (MSE): %.6f\n', mse);
fprintf('Mean Absolute Error (MAE): %.6f\n', mae);
% Display the total number of clicks
fprintf('Total Number of Clicks: %d\n', total_clicks);
% Play "degraded.wav" for the first 5 seconds
sound(x(1:5 * sample_rate), sample_rate);
% Pause for 5 seconds
pause(5);
% Play the restored audio for the first 5 seconds
sound(restored_audio(1:5 * sample_rate), sample_rate);
% Plot the input file
subplot(4, 1, 1);
plot(x);
title('Input File');
% Plot the output file
subplot(4, 1, 2);
plot(restored_audio);
title('Output File');
% Plot the clean audio
subplot(4, 1, 3);
plot(clean_audio);
title('Clean File');
% Plot the click detection
subplot(4, 1, 4);
plot(click_detection);
title('Click Detection');
% Function to calculate the residual
function [residual] = getResidual(data, coeffs)
    % Generate the residual over the entire block
    filt_coeffs = [1, coeffs];
    residual = filter(filt_coeffs, 1, data);
end
% Function to interpolate using AR model
function [restored, A_k, A_u, y_k] = interpolateAR(block, detected_missing, coeffs)
    length_datablock = length(block);
    p = length(coeffs);
    missing_num = sum(detected_missing);
    
    % Find indices of missing values
    missing_indices = find(detected_missing);
    
    % If there are no missing values, return the original block
    if isempty(missing_indices)
        restored = block;
        A_k = [];
        A_u = [];
        y_k = [];
        return;
    end
    
    % Extract non-missing values
    y_k = block(~detected_missing);
    y_k_mean = mean(y_k);
    y_k = y_k - y_k_mean;
    
    % Construct the AR matrix
    A = zeros(length_datablock, length_datablock);
    for i = p+1:length_datablock
        A(i, i-p:i-1) = flip(coeffs);
    end
    % Identify the order of the block
    order_block = 1:length_datablock;
    
    % Remove missing values from the order
    order_block(missing_indices) = [];
    
    % Extract A_u matrix
    A_u = A(:, missing_indices);
    
    % Extract A_k matrix
    A_k = A(:, order_block);
    
    % Estimate missing values using AR model
    y_u = -inv(A_u' * A_u) * A_u' * A_k * y_k;
    y_u = y_u + y_k_mean;
    
    % Replace missing values in the original block with estimated values
    restored = block;
    restored(missing_indices) = y_u(:);
end
% Function to estimate AR coefficients using LS
function ar_coeffs = estimateARCoefficients(reference_block, order)
    H = hankel(reference_block(1:end-1), reference_block(end:-1:1));
    A = H(:, 1:order);
    b = reference_block(2:end);
    ar_coeffs = A \ b;
end
