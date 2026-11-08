% Autor: Clemens Loher
% Date: 03.11.2026

% Programmieren der Temperaturkennlinie von PTC und NTC Thermistoren
clc
clear all

%% Teil 1

% Parameter
R0PTC00 = 500;
alpha = 3.90802e-3;
beta = -5.802e-7;
Temperatur1 = [0:0.01:100]; % Temperaturbereich von 0 °C - 100 °C
Temperatur2 = [0:0.01:1200]; % Temperaturbereich von 0 °C - 1200 °C

% Formeln
Widerstand1 = R0PTC00 .* (1 + alpha .* Temperatur1 + beta .* Temperatur1.^2);
Widerstand2 = R0PTC00 .* (1 + alpha .* Temperatur2 + beta .* Temperatur2.^2);
Widerstandohnebeta = R0PTC00 .* (1 + alpha .* Temperatur2);

% Temperaturkennlinie des PTC
figure(1)
plot(Temperatur1, Widerstand1, 'r')
grid on
xlabel("Temperatur[°C]")
ylabel("Widerstand [Ohm]")
title("Temperaturkennlinie des PTC-Thermistors")
legend("PTC")

figure(2)
plot(Temperatur2, Widerstand2, 'r')
grid on
xlabel("Temperatur[°C]")
ylabel("Widerstand [Ohm]")
title("Temperaturkennlinie des PTC-Thermistors")
legend("PTC")

figure(3)
plot(Temperatur2, Widerstand2, 'g')
grid on
hold on
plot(Temperatur2, Widerstandohnebeta, 'r--')
xlabel("Temperatur[°C]")
ylabel("Widerstand [Ohm]")
hold off
legend('Widerstand mit beta','Widerstand ohne beta')
title("Temperaturkennlinie des PTC-Thermistors")

%% Teil 2

% Parameter
T0 = 20;
R0NTC20 = 20000; %  Widerstand R0 von 20000 Ohm bei 20 °C
B = 3000; % Materialparameter
Temperatur3 = [0:10:100]; % Die Temperatur nur in 10er Schritten um die Interpolation zu machen

% Formel
RT_exakt = R0NTC20 .* exp(B .* (1./(Temperatur1 + 273.15) - 1./(T0 + 273.15))); % exakte Kurve
RT_gemessen =  R0NTC20 .* exp(B .* (1./(Temperatur3 + 273.15) - 1./(T0 + 273.15))); % Messwerte

% Temperaturkennlinie des NTC darstellen
figure(4)
plot(Temperatur1, RT_exakt/1000, 'g')
grid on
xlabel("Temperatur [°C]")
ylabel("Widerstand [kOhm]")
title("Temperaturkennlinie des NTC-Thermistors")
legend("NTC")

% Interpolierte Ergebnisse
figure(5)
plot(Temperatur1, RT_exakt/1000, 'g')
grid on
hold on
plot(Temperatur3, RT_gemessen/1000, 'rX--')
hold off
xlabel("Temperatur [°C]")
ylabel("Widerstand [kOhm]")
title("Temperaturkennlinie des NTC-Thermistors")
legend("NTC-Kurve","NTC-Kurve gemessen")



% Interpolation bei 5°C
RTinterpoliert5 = interp1(Temperatur3,RT_gemessen/1000,5); 
fprintf("Widerstand bei 5°C: %.1f kOhm\n", RTinterpoliert5)
fprintf("exakter Widerstand bei 5°C: %.1f kOhm\n", RT_exakt(501)/1000) % bei 501 -> 5 (Index = Wert/Schrittweite +1)

% Interpolation bei 15°C
RTinterpoliert15 = interp1(Temperatur3,RT_gemessen/1000,15); 
fprintf("Widerstand bei 15°C: %.1f kOhm\n", RTinterpoliert15)
fprintf("exakter Widerstand bei 15°C: %.1f kOhm\n", RT_exakt(1501)/1000) % bei 1501 -> 15 (Index = Wert/Schrittweite +1)

% Interpolation bei 65°C
RTinterpoliert65 = interp1(Temperatur3,RT_gemessen/1000,65); 
fprintf("Widerstand bei 65°C: %.1f kOhm\n", RTinterpoliert65)
fprintf("exakter Widerstand bei 15°C: %.1f kOhm\n", RT_exakt(6501)/1000) % bei 6501 -> 65 (Index = Wert/Schrittweite +1)

