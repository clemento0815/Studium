% Autor: Clemens Loher
% Date: 03.11.2026
% ----------------------------------------------------------------------
% MATLAB Version: 25.2.0.2998904 (R2025b)
% MATLAB License Number: 40641888
% Operating System: Microsoft Windows 11 Home Version 10.0 (Build 26300)
% Java Version: Java is not enabled
% ----------------------------------------------------------------------
% MATLAB                                                Version 25.2        (R2025b)
% Simulink                                              Version 25.2        (R2025b)
% Signal Processing Toolbox                             Version 25.2        (R2025b)
% 
% Betriebsystemname	Microsoft Windows 11 Home
% Version	10.0.26300 Build 26300
% Weitere Betriebsystembeschreibung 	Nicht verfügbar
% Betriebsystemhersteller	Microsoft Corporation
% Systemname	CLAPTOP
% Systemhersteller	Acer
% Systemmodell	Swift SF14-11
% Systemtyp	ARM64-based PC
% System-SKU	0000000000000000
% Prozessor	Snapdragon(R) X Plus - X1P64100 - Qualcomm(R) Oryon(TM) CPU, 3417 MHz, 10 Kern(e), 10 logische(r) Prozessor(en)
% BIOS-Version/-Datum	Insyde Corp. V1.24, 12.05.2025
% SMBIOS-Version	3.6
% Version des eingebetteten Controllers	1.21
% BIOS-Modus	UEFI
% BaseBoard-Hersteller	SX1
% BaseBoard-Produkt	Bluetang_SX1
% BaseBoard-Version	V1.24
% Plattformrolle	Mobil
% Sicherer Startzustand	Ein
% PCR7-Konfiguration	Erweiterung zum Anzeigen erforderlich
% Windows-Verzeichnis	C:\Windows
% Systemverzeichnis	C:\Windows\system32
% Startgerät	\Device\HarddiskVolume1
% Gebietsschema	Deutschland
% Hardwareabstraktionsebene	Version = "10.0.26100.1"
% Benutzername	Claptop\cleme
% Zeitzone	Mitteleuropäische Zeit
% Installierter physischer Speicher (RAM)	16,0 GB
% Gesamter physischer Speicher	15,6 GB
% Verfügbarer physischer Speicher	2,34 GB
% Gesamter virtueller Speicher	55,0 GB
% Verfügbarer virtueller Speicher	31,8 GB
% Größe der Auslagerungsdatei	39,4 GB
% Auslagerungsdatei	C:\pagefile.sys
% Kernel-DMA-Schutz	Ein
% Virtualisierungsbasierte Sicherheit	Wird ausgeführt...
% Virtualisierungsbasierte Sicherheit – erforderliche Sicherheitseigenschaften	Allgemeine Virtualisierungsunterstützung
% Virtualisierungsbasierte Sicherheit – verfügbare Sicherheitseigenschaften	Allgemeine Virtualisierungsunterstützung, Sicherer Start, DMA-Schutz, UEFI-Code Readonly, Modusbasierte Ausführungssteuerung
% Virtualisierungsbasierte Sicherheit – konfigurierte Dienste	Durch Hypervisor erzwungene Codeintegrität, Sicherer Start
% Virtualisierungsbasierte Sicherheit – ausgeführte Dienste	Durch Hypervisor erzwungene Codeintegrität, Sicherer Start
% App Control for Business-Richtlinie	Erzwungen
% App Control for Business-Benutzermodusrichtlinie	Aus
% Sicherheitsfeatures aktiviert	Absenderadressensignierung (Kernelmodus)
% Unterstützung für automatische Geräteverschlüsselung	Erweiterung zum Anzeigen erforderlich
% Es wurde ein Hypervisor erkannt. Features, die für Hyper-V erforderlich sind, werden nicht angezeigt.	


% Programmieren der Temperaturkennlinie von PTC und NTC Thermistoren

clc
clear
close all

% Parameter
fs       = 2e6;               % Sendefrequenz in Hz
cBlut    = 1483;              % Schallgeschwindigkeit im Blut in m/s
alpha    = 40;                % Einschallwinkel in Grad
alpharad = deg2rad(alpha);    % Umrechnung in rad
deltaf   = -800:1:800;        % Frequenzdifferenz fs - fe in Hz

% lutflussgeschwindigkeit berechnen
% v > 0: Blut fließt auf den Schallkopf zu
vBlut_exakt     = deltaf * cBlut ./ (cos(alpharad) * (2*fs - deltaf));  % exakte Formel
vBlut_naeherung = deltaf * cBlut  / (cos(alpharad) * 2*fs);             % Näherungsformel

% Grafische Darstellung
figure(1)
plot(deltaf, vBlut_exakt, 'o')
hold on
plot(deltaf, vBlut_naeherung, '.')
hold off
grid on
xlabel('\Deltaf [Hz]')
ylabel('Blutflussgeschwindigkeit [m/s]')
legend('Exakte Formel', 'Näherung', 'Location', 'best')
title('Blutflussgeschwindigkeit in Abhängigkeit von der Frequenzdifferenz')

% Abweichung zwischen exaktem Wert und Näherung
abweichung     = vBlut_naeherung - vBlut_exakt;          % absolut in m/s
abweichung_rel = abweichung ./ vBlut_exakt * 100;        % relativ in % (bei deltaf = 0: NaN)

% Abweichung grafisch darstellen
figure(2)
plot(deltaf, abweichung, LineWidth=2)
grid on
xlabel('\Deltaf [Hz]')
ylabel('Abweichung v_{exakt} - v_{Näherung} [m/s]')
title('Abweichung zwischen exakter Formel und Näherung')

% Werte bei deltaf = 413.1977 Hz mittels interp1
df_gesucht      = 413.1977;                                    % gegebene Frequenzdifferenz in Hz
v_exakt_gesucht = interp1(deltaf, vBlut_exakt, df_gesucht);     % exakter Wert
v_naeh_gesucht  = interp1(deltaf, vBlut_naeherung, df_gesucht); % Näherungswert
abw_gesucht     = interp1(deltaf, abweichung, df_gesucht);      % Abweichung

fprintf('Bei Deltaf = %.4f Hz:\n', df_gesucht);
fprintf('  exakte Geschwindigkeit:  %.6f m/s\n', v_exakt_gesucht);
fprintf('  Näherung:                %.6f m/s\n', v_naeh_gesucht);
fprintf('  Abweichung:              %.2e m/s\n', abw_gesucht);

% interpolierte Abweichung in Figure 2 eintragen
figure(2)
hold on
plot(df_gesucht, abw_gesucht, 'r*', 'MarkerSize', 12)
hold off
legend('Abweichung', 'Abweichung interpoliert', 'Location', 'best')

% interpolierte Geschwindigkeiten in Figure 3
figure(3)
plot(deltaf, vBlut_exakt, 'o')
hold on
plot(deltaf, vBlut_naeherung, '.')
plot(df_gesucht, v_exakt_gesucht, 'r*', 'MarkerSize', 12)
plot(df_gesucht, v_naeh_gesucht,  'kx', 'MarkerSize', 12)
hold off
grid on
xlabel('\Deltaf [Hz]')
ylabel('Blutflussgeschwindigkeit [m/s]')
legend('Exakte Formel', 'Näherung', 'v_{exakt} interpoliert', 'v_{Näherung} interpoliert', 'Location', 'best')
title('Interpolierte Werte bei \Deltaf = 413.1977 Hz')
