function [] = bolus()
% Modell der Gabe eines intravenösen Bolus, Kompartimentmodell

% Parameter
par.D = 1000;
par.k12 = 0.6;
par.k21 = 1.25;
par.k10 = 0.2;

% Schrittweite
tend = 24; % entspricht 24 Stunden, alle Austauschraten k12, k21, k10
           % sind Stoffmenge/Stunde

% Aufrufen der Funktion (mit unterschiedl. h)
h1 = 0.001;  % Schrittweite in Stunden
[t1, Xp1, Xc1, E1] = bolus_euler_iteration(tend, h1, par);

h2 = 0.1;  % Schrittweite in Stunden
[t2, Xp2, Xc2, E2] = bolus_euler_iteration(tend, h2, par);

% Plotten
figure(1);
plot(t1, Xc1, 'b-', t1, Xp1, 'r-', t1, E1, 'k-', 'LineWidth', 1.5); hold on;
plot(t2, Xc2, 'b--', t2, Xp2, 'r--', t2, E2, 'k--', 'LineWidth', 1.5); hold off;
xlabel('Zeit (h)');
ylabel('Stoffmenge');
legend('Zentralkompartiment', 'Peripheres Kompartiment', 'Elimination');
grid on;
end

% Berechnen der Euler Iteration
function [t, Xp, Xc, E] = bolus_euler_iteration(tend, h, par)
    % Anzahl der Schritte
    N = ceil(tend/h);
    
    % extrahieren der Parameter aus dem Parameterstruct
    D = par.D;
    k12 = par.k12;
    k21 = par.k21;
    k10 = par.k10;
    
    % Anfangsbedingungen
    Xc(1) = D;
    Xp(1) = 0;
    E(1) = 0;
    
    % Iteration nach Euler
    for i = 1:N-1
        Xc(i+1)=Xc(i)+h*(-k12*Xc(i)+k21*Xp(i)-k10*Xc(i));
        Xp(i+1)=Xp(i)+h*(-k21*Xp(i)+k12*Xc(i));
        E(i+1) =E(i) +h*k10*Xc(i);
    end
    
    % Zeitvektor
    t = 0:h:(N-1)*h;
end