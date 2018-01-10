% Power Calculator and Run Estimator using a differential equation method
% Date Created 16/9/17
close all; clear all;

%% DATA INPUTS
%put file name of input data eg. Data_input_Blacksmith
% variables will be copied to workspace
Data_input_Blacksmith

%% POWER EQUATIONS
%Defined in separate functions for faster speed
%P_air -> Air Drag
%P_roll -> Rolling Resistance
%P_slope -> Power against gravity when riding up a slope
%P_inrun -> Power input during in-run. Aerobic Power.
%P_sprint -> Power input during final sprint. Anaerobic.

%% Set up for loop to vary mass

mass = 90:2:130;
for i=1:length(mass)
     
    
%% POWER ODE
dvdt = @(t,v) (1/(mass(i)*v))*((P_inrun(intensityfactor,P_GET,rateconst,t,ts) + P_sprint(P_MAX,srateconst,t,ts))*(1-(DTEffLoss/100)) - P_air(rho,CdA,v) - P_roll(mass(i),g,mu,grad,v) - P_slope(mass(i),g,grad,v)) ;

v0 = 1;
tlist = [0:ts+120];

%% SOLVING THE ODE
tspan = [min(tlist),max(tlist)];
opts = odeset('Refine',50,'RelTol',1e-6); %increases the number of points, better for plotting the power input
[t,v] = ode45(dvdt,tspan,v0,opts); % solve the ode

% Plot velocity vs time and distance


    
maxspeed = max(v);
maxkph(i) = maxspeed*3.6;
end
plot(mass,maxkph)
xlabel('totalmass (kg)')
ylabel('top speed (km/h)')
grid on
kmhperkg = (maxkph(i)-maxkph(1))/(mass(i)-mass(1))