% Konvergenzanalyse für die numerische Lösung der Bewegungsgleichungen
% eines Feder Masse Systems

clear all;

% Parameter definieren
par.m = 1;
par.c = 1;
par.d = 0.5;
par.F0 = 10;
par.x0 = 0;
par.v0 = 0;
par.tend = 35;
par.method = 'explicit';
par.h = 0.01;

% Berechnen der Grenzschrittweite
A = [0 1;-par.c/par.m -par.d/par.m];
lambda = eig(A);
a = real(lambda);
b = imag(lambda);
h_stab = -2*a./(a.^2+b.^2);
h_grenz = min(h_stab);


% Schrittweiten definiern
h_values = logspace(log10(h_grenz),log10(h_grenz/1E10),100);

% gemeinsamte Zeitbasis
t_eval = 0:0.01:par.tend;

xsim = [];
tsim = [];
t_comp = [];

for h = h_values
    % Starten der Stoppuhr
    tic;
    % Schrittweite in par struct schreiben
    par.h = h;
    % Funktion aufrufen
    [x, t] = euler_fms(par);
    % merken der Rechenzeit
    t_comp(end+1) = toc;
    % Ergebnisse in Matrix schreiben
    xsim(end+1,:) = interp1(t, x, t_eval, "linear","extrap");
    
end

% Berechnung der Abweichung zwiscehn den Lösungen
xsim_betrag = sqrt(sum(xsim.^2, 2));
delta = sqrt(sum(diff(xsim).^2, 2));
delta_rel = delta./xsim_betrag(1:end-1)*100;



% Plotten
figure(1); clf;
% plot(t_eval,xsim, LineWidth=2);
% grid on;
% xlabel('t(s)')
% ylabel('x(m)')
yyaxis left;
loglog(h_values(2:end),delta_rel, LineWidth=2)
grid on
xlabel('Schrittweite h(s)')
ylabel('relative Abweichung in %')
yyaxis right
loglog(h_values(2:end), t_comp(2:end));
ylabel('Rechenzeit (s)')
legend('Relative Abweichung', 'Rechenzeit', 'Location', 'best')
title('Konvergenzanalyse')
