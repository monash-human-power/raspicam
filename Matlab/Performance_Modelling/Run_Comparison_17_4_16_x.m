% Power Calculator and Run Estimator using a differential equation method
% Date Created 16/9/17
close all; clear all;

%% DATA INPUTS
% Data values accurate for Record Run, 16/4/17 at FPV
Data_input_Blacksmith

%% POWER EQUATIONS
%Defined in separate functions for faster speed
%P_air -> Air Drag
%P_roll -> Rolling Resistance
%P_slope -> Power against gravity when riding up a slope
% P_Input_Easter -> Piecewise polynomial function for the power exerted at
% the easeter event, record run
%% Slope Data
SlopeData = xlsread('YYPG Track Survey Data.xlsx');
Dist = SlopeData(:,2)';
Height = SlopeData(:,3)';
[fitresult, gof] = createFitSlope(Dist, Height,1);


%% POWER INPUT FUNCTION
RunData = xlsread('Run_Data_17_4_16.xlsx');

PowerSectionA = (RunData(1:395,7))';
dSectionA = (RunData(1:395,5))';
dStart = dSectionA(1);
dSectionA = (dSectionA-dStart)*1000;
FuncA = polyfit(dSectionA,PowerSectionA,5);
% figure
% plot(tSectionA,PowerSectionA)
% hold on
% plot(tSectionA,polyval(FuncA,tSectionA))
%% POWER ODE
dvdx = @(x,v) (1/(m*v^2))*((P_input_Easter_x(FuncA,x))*(1-DTEffLoss/100) - P_air(rho,CdA,v) - P_roll(m,g,mu,gradf(x,fitresult),v) - P_slope(m,g,gradf(x,fitresult),v)) ;

v0 = 5;
xspan = [0,5500];

%% SOLVING THE ODE

opts = odeset('Refine',10,'RelTol',1e-6); %increases the number of points, better for plotting the power input
[x,v] = ode45(dvdx,xspan,v0,opts); % solve the ode

% Plot velocity vs time and distance

figure
subplot(3,1,1)
plot(x,v)
xlabel('distance (m)')
ylabel('velocity (m/s)')
hold on

vActual = (RunData(1:500,6))./3.6;
dActual = ((RunData(1:500,5)) - dStart)*1000;
plot(dActual,vActual)
hold off

% d= [0];
% for n = 2:length(t)
%     d(n) = d(n-1)+ v(n-1)*(t(n)-t(n-1));
% end
%     
%     
% subplot(3,1,2)
% plot(d,v(1:length(d)))
% xlabel('distance (m)')
% ylabel('velocity (m/s)')

%% plot the input power vs distance

for k = 1:500
     Pin(k)=P_input_Easter_x(FuncA,dActual(k));
end

subplot(3,1,3)
plot(dActual,Pin)
xlabel('distance (m)')
ylabel('Input Power (W)')
 hold on
 pActual = (RunData(1:500,7))';
 plot(dActual,pActual)