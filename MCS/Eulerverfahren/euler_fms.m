function [x, t] = euler_fms(par)
%------------------------------------------------------------
% Loesung der Bewegungsgleichungen für ein Feder-Masse System
% mit dem expliziten bzw. impliziten Euler.
%
% par:  parameter struct mit den Feldern m, c, d, F0, x0, v0
%       und dem feld "method" =  "explicit" oder "implicit"
%       Simulationsweite h
%
% 10. November 2026: A. Schrempf
%------------------------------------------------------------

% parameter
m = par.m;
c = par.c;
d = par.d;
F0 = par.F0;
x0 = par.x0;
v0 = par.v0;
tend = par.tend;
h = par.h;

% Methode
if isfield(par, 'method')
	method = par.method;
else
  method = 'explicit';
end

% Werte berechnen
N = round(tend/h);
t = (0:N-1)*h;

% Euler Verfahren
x = zeros(1,N);
v = zeros(1,N);
x(1) = x0;
v(1) = v0;

if strcmp(method, 'explicit')
    % explizites Verfahren
    for i = 1:N-1
        x(i+1) = x(i)+h*v(i);
        v(i+1) = v(i)+h*1/m*(F0-c*x(i)-d*v(i));
    end
else
    % implizites Verfahren
    for i = 1:N-1
        v(i+1) = (v(i)+h*1/m*(F0-x(i)))/(1+d*h/m+h^2*c/m);
        x(i+1) = x(i)+h*v(i+1);
    end
end

