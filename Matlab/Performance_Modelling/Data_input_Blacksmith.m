% Data File MHP Blacksmith
rho = 1.225; %Air Density, kg/m^3
CdA = 0.0243;
m = 128; % Total Mass
g = 9.80; %Gravity
mu = 0.0084; %Co-efficient of Rolling Resistance
grad = 0; %Road Gradient
intensityfactor = 1; %Percent of P_GET in inrun
P_GET = 250; %Max Aerobic Power
P_MAX = 150; %Max Anaerobic Power above P_GET
rateconst = -0.153; %Rate of increase for In-run Power
srateconst = -0.0494; %Rate of increase for Sprint Power
ts = 300;%Time when sprint starts
xs = 3500; %distance when sprint starts
P_IN = 200; %Constant 
DTEffLoss = 11.3;% Power lost in the drivetrain, due to friction in the chain