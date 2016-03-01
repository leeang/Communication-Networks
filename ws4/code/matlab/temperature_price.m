clear;
close all;

load data.mat;
% temperature and price

hour = 0:47;
hour = floor(hour/2);

minute = zeros(1, 48);
minute(2:2:48) = 30;

sdate = datenum(2015, 10, 5, hour, minute, 0);

temperature_average = mean(temperature);
price_average = mean(price);

set_point1 = ones(1, 48) * 20;
for index=1:48
    if price(index) > price_average
        set_point1(index) = set_point1(index) - 0.3 * (price(index) - price_average);
    else
        set_point1(index) = set_point1(index) - 0.1 * (price(index) - price_average);
    end
end

set_point2 = ones(1, 48) * 20;
for index=1:48
    if index<=13
        set_point2(index) = set_point2(index) - (10 - 1.66 * abs(index - 7));
    end
end

set_point = ones(1, 48) * 20;
for index=1:48
    if price(index) > price_average
        set_point(index) = set_point(index) - 0.3 * (price(index) - price_average);
    end
    if price(index) < price_average
        set_point(index) = set_point(index) - 0.1 * (price(index) - price_average);
    end
    if index<=13
        set_point(index) = set_point(index) - (10 - 1.66 * abs(index - 7));
    end
end

plot(sdate, temperature, sdate, price, 'linewidth', 1.5);
hold on;
plot([sdate(1) sdate(48)], [temperature_average temperature_average], '-.');
plot([sdate(1) sdate(48)], [price_average price_average], '-.');
datetick('x', 'HH:MM');
legend('temperature', 'price', 'average temperature', 'average price', 'location', 'northwest');
title('Temperature and price simulation');
xlabel('time');
ylim([0 55]);
grid on;

figure;
plot(sdate, price, sdate, set_point1, 'linewidth', 1.5);
hold on;
plot([sdate(1) sdate(48)], [price_average price_average], '-.');
datetick('x', 'HH:MM');
title('Factor 1: set point varies with price');
xlabel('time');
legend('price', 'set point', 'average price', 'location', 'northwest');
ylim([0 55]);
grid on;

figure;
plot(sdate, price, sdate, set_point2, 'linewidth', 1.5);
hold on;
plot([sdate(1) sdate(48)], [price_average price_average], '-.');
datetick('x', 'HH:MM');
title('Factor 2: set point varies with time');
xlabel('time');
legend('price', 'set point', 'average price', 'location', 'northwest');
ylim([0 55]);
grid on;

figure;
plot(sdate, price, sdate, set_point, 'linewidth', 1.5);
hold on;
plot([sdate(1) sdate(48)], [price_average price_average], ':');
plot(sdate, temperature, '-.');
datetick('x', 'HH:MM');
title('Set point varies with price and time');
xlabel('time');
legend('price', 'set point', 'average price', 'outside temperature', 'location', 'northwest');
ylim([0 55]);
grid on;
