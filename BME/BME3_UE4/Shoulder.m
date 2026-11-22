% Berechnen der Muskelkraft für die Bewegung des ausgestreckten Armes mit
% einer ausgestreckten Hantel in der Frontalebene
clear all;


% Parameter
H = 1.58; % Körpergröße in m
M = 43; % Körpergewicht in kg
g = 9.81; % Erdbeschleunigung
mA = 0.05 * M; % Masse des gesamten Arms (Antropometrietabelle)
m0 = 10; % Masse der Hantel in kg
c = (0.818-0.485)*H; % Armlänge in m
b = 0.53*c;
a = 0.4*0.186*H;
theta = deg2rad(15);
rT = 0.645*c;
Theta_zz = mA*rT^2 + m0*c^2;


% Bewegung
N = 100;
phi_min = 0;
phi_max =deg2rad(25);
T = 2;
t = linspace(0, T, N);
phi = (phi_max+phi_min)/2 - (phi_max-phi_min)/2*cos(2*pi*t/T);
dphi = (phi_max-phi_min)/2*(2*pi/T)*sin(2*pi*t/T);
ddphi = (phi_max-phi_min)/2*(2*pi/T)^2*cos(2*pi*t/T);



% Muskelkraft
Fm = (Theta_zz * ddphi + (mA*b+m0*c)*g*cos(phi))/(a*sin(theta));
Fm_stat = (mA*b+m0*c)*g*cos(phi)/(a*sin(theta));
% Plotten
figure(1)
clf;
plot(t, rad2deg(phi), t, rad2deg(dphi), t, rad2deg(ddphi));
grid on;
xlabel("t[s]");
ylabel("phi[rad], dphi[rad/s], ddphi[rad/s^2]");
legend("phi[rad]","dphi[rad/s]","ddphi[rad/s^2]");

figure(2)
clf;
plot(rad2deg(phi), Fm, rad2deg(phi), Fm_stat);
grid on;
xlabel("phi [°]");
ylabel("Fm [N]");