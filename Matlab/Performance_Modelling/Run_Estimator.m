% Power Calculator and Run Estimator using a differential equation method
% Date Created 16/9/17
 close all; clear all;

%% DATA INPUTS
%put file name of input data eg. Data_input_Blacksmith
% variables will be copied to workspace
Data_input_1_5

%% POWER EQUATIONS
%Defined in separate functions for faster speed
%P_air -> Air Drag
%P_roll -> Rolling Resistance
%P_slope -> Power against gravity when riding up a slope
%P_inrun -> Power input during in-run. Aerobic Power.
%P_sprint -> Power input during final sprint. Anaerobic.

%% POWER ODE
dvdt = @(t,v) (1/(m*v))*((P_inrun(intensityfactor,P_GET,rateconst,t,ts) + P_sprint(P_MAX,srateconst,t,ts))*(1-(DTEffLoss/100)) - P_air(rho,CdA,v) - P_roll(m,g,mu,grad,v) - P_slope(m,g,grad,v)) ;

v0 = 1;
tlist = [0:ts+120];

%% SOLVING THE ODE
tspan = [min(tlist),max(tlist)];
opts = odeset('Refine',50,'RelTol',1e-6); %increases the number of points, better for plotting the power input
[t,v] = ode45(dvdt,tspan,v0,opts); % solve the ode

% Plot velocity vs time and distance

figure
subplot(3,1,1)
plot(t,v)
xlabel('time (s)')
ylabel('velocity (m/s)')

d = t.*v;
subplot(3,1,2)
plot(d,v)
xlabel('distance (m)')
ylabel('velocity (m/s)')

%plot the input power vs distance
for k = 1:length(t)
 
    Pin(k)=(P_inrun(intensityfactor,P_GET,rateconst,t(k),ts) + P_sprint(P_MAX,srateconst,t(k),ts));
end

subplot(3,1,3)
plot(d,Pin)
xlabel('distance (m)')
ylabel('Input Power (W)')

maxspeed = max(v)
maxkph = maxspeed*3.6