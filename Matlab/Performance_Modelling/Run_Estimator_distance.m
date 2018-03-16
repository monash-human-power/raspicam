% Power Calculator and Run Estimator using a differential equation method
% Date Created 16/9/17
 close all; clear all;

%% DATA INPUTS
%put file name of input data eg. Data_input_Blacksmith
% variables will be copied to workspace
Data_input_1_5

%% Slope Data
SlopeData = xlsread('YYPG Track Survey Data.xlsx');
Dist = SlopeData(:,2)';
Height = SlopeData(:,3)';
[fitresult, gof] = createFitSlope(Dist, Height,1); %1 to draw height graph, 0 to ignore
% Slope = differentiate(fitresult,Dist);
% Grad = Slope*100;
% hold on
% yyaxis right
% plot(Dist,Grad)


%% POWER EQUATIONS
%Defined in separate functions for faster speed
%P_air -> Air Drag
%P_roll -> Rolling Resistance
%P_slope -> Power against gravity when riding up a slope, uses variable
%gradient function
%P_inrun -> Power input during in-run. Aerobic Power.
%P_sprint -> Power input during final sprint. Anaerobic.

%% POWER ODE
dvdx = @(x,v) (1/(m*v^2))*((P_in_x(intensityfactor,P_GET,rateconst,P_MAX,srateconst,x,xs))*(1-(DTEffLoss/100)) - P_air(rho,CdA,v) - P_roll(m,g,mu,gradf(x,fitresult),v) - P_slope(m,g,gradf(x,fitresult),v)) ;

v0 = 1;
xlist = [0:4000];

%% SOLVING THE ODE
xspan = [min(xlist),max(xlist)];
opts = odeset('Refine',50,'RelTol',1e-6); %increases the number of points, better for plotting the power input

[x,v] = ode45(dvdx,xspan,v0,opts); % solve the ode

% Plot velocity vs time and distance

figure
subplot(3,1,1)
plot(x,v)
xlabel('distance (m)')
ylabel('velocity (m/s)')

% d = v./t;
subplot(3,1,2)
plot(x,gradf(x,fitresult))
xlabel('distance (m)')
ylabel('gradient (m/s)')

%plot the input power vs distance
for k = 1:length(x)
 
    Pin(k)=P_in_x(intensityfactor,P_GET,rateconst,P_MAX,srateconst,x(k),xs);
end

subplot(3,1,3)
plot(x,Pin)
xlabel('distance (m)')
ylabel('Input Power (W)')

maxspeed = max(v)
maxkph = maxspeed*3.6