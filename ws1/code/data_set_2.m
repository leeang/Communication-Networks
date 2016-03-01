clear;
close all;
load('time2.mat');

gap = diff(Time);

% Question 3.2
fprintf('minimum: %f\n', min(gap));
fprintf('maximum: %f\n', max(gap));
fprintf('average: %f\n', mean(gap));
fprintf('standard deviation: %f\n\n', std(gap));

% Question 3.3
gap_clean = gap(gap<prctile(gap, 95));
fprintf('minimum (clean): %f\n', min(gap_clean));
fprintf('maximum (clean): %f\n', max(gap_clean));
fprintf('average (clean): %f\n', mean(gap_clean));
fprintf('standard deviation (clean): %f\n', std(gap_clean));

% Question 3.4
plot(gap_clean);
title('Time series of the cleaned packet IATs');
xlabel('n-th packet');
ylabel('inter-arrival time (s)');

figure;
histogram(gap_clean);
title('Histogram of the cleaned packet IATs and trend line');
xlabel('Inter-arrival time (s)');
ylabel('Quantity of packets');

% Question 3.5
muhat = expfit(gap_clean, 1e-12)

% Question 3.6
x = 0:1e-6:max(gap_clean);
hold on;
plot(x, exppdf(x, muhat), 'linewidth', 2);
legend('histogram', 'trend line');

figure;
h = histfit(gap_clean);
h(1).FaceColor = [0 0.5 0];
title('Histogram of the cleaned packet IATs and trend line');
xlabel('Inter-arrival time (s)');
ylabel('Quantity of packets');
legend('histogram', 'normal distribution');
