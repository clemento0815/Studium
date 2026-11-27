model RLC_graphical
  Modelica.Electrical.Analog.Sources.StepVoltage U(V = 10, startTime = 5E-3)  annotation(
    Placement(transformation(origin = {-140, 210}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Electrical.Analog.Basic.Resistor R1(R = 1)  annotation(
    Placement(transformation(origin = {-110, 240}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Capacitor C1(C = 1E-3)  annotation(
    Placement(transformation(origin = {-70, 240}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Inductor L1(L = 1E-4)  annotation(
    Placement(transformation(origin = {-40, 210}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Electrical.Analog.Basic.Ground Gnd annotation(
    Placement(transformation(origin = {-40, 170}, extent = {{-10, -10}, {10, 10}})));
equation
  connect(U.p, R1.p) annotation(
    Line(points = {{-140, 220}, {-140, 240}, {-120, 240}}, color = {0, 0, 255}));
  connect(U.n, Gnd.p) annotation(
    Line(points = {{-140, 200}, {-140, 180}, {-40, 180}}, color = {0, 0, 255}));
  connect(Gnd.p, L1.n) annotation(
    Line(points = {{-40, 180}, {-40, 200}}, color = {0, 0, 255}));
  connect(R1.n, C1.p) annotation(
    Line(points = {{-100, 240}, {-80, 240}}, color = {0, 0, 255}));
  connect(C1.n, L1.p) annotation(
    Line(points = {{-60, 240}, {-40, 240}, {-40, 220}}, color = {0, 0, 255}));

annotation(
    Diagram(coordinateSystem(extent = {{-300, -300}, {300, 300}})),
    Icon(coordinateSystem(extent = {{-300, -300}, {300, 300}})),
    version = "",
    uses(Modelica(version = "4.1.0")));
end RLC_graphical;
