% Matlab Skript - schwingender US
clear all;

% Laden der Messdaten
load("TrackedMarkers.mat")

% Plotten der Daten
figure(1);
plot(timePlot.t, timePlot.phi, LineWidth=2);
grid on;
xlabel(" t(s)")

% Messdaten für Simulink vorbereiten
% erster Peak bei 1.76 sec, Periodendauer 1.12 sec
t0 = 1.76 - 1.12;
data.time = timePlot.t - t0;
data.signals.values = timePlot.phi;


% Definieren der Parameter
m = 4;           % Masse US
Thetazz = 0.495; % Massenträgheit
ls = 0.4;        % Abstand Massenschwerpunkt
g = 9.81;
mu = 0.45;       % Reibungskoeffizient

% Anfangsbedingungen
phi0 = interp1(timePlot.t, timePlot.phi, t0);
omega0 = 0;

% Eigenwerte berechnen
A = [0 1; -m*g*ls/Thetazz -mu/Thetazz];
lambda = eig(A)
% Periodendauer anhand der Eigenwerte
T = 2*pi/imag(lambda(1))  

% Simulink ausführen
out = sim("leg.slx");

% Ergebnisse plotten
figure(2);
plot(out.results.time, out.results.signals.values, ...
     LineWidth = 2);
grid on;
xlabel(" t (s)")
ylabel(" phi (rad)")
legend("Simulation", "Messung")