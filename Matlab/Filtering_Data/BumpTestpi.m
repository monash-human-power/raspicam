clc;
clear all;
close all;

% For Titles
fig_title = 'Data 6-12-17 @ Carpark';
str = 'Test 1';

% Import data
% UEI_Data = importdata('UEI_Test_3.csv');
Pi_Data = importdata('.csv');

% Analog calibration values
% ZeroGx = 1.5881;
% ZeroGy = 1.6681;
% ZeroGz = 1.5691;
% Sensx = 0.4003;
% Sensy = 0.4129;
% Sensz = 0.4031;

% Convert UEI accelerometer data to Gs
% accelxUEI = ((UEI_Data.data(:,8)) - ZeroGx) / Sensx ;  
% accelyUEI = ((UEI_Data.data(:,9)) - ZeroGy) / Sensy ; 
% accelzUEI = ((UEI_Data.data(:,10)) - ZeroGz) / Sensz ; 

% Get sensitivity for pi from "Sensor Characteristics" section of Datasheet
Sensitivity = 3.90625; % Sensitivity = 32,000mg / 65,535 counts

% NOTE THAT THIS SENSITIVITY HAD TO BE GUESSED AFTER TESTING

% Obtain time index
timePi = Pi_Data(:,1);
% timeUEI = 0:0.00025:(length(accelxUEI)-1)*0.00025;

% Calculate sampling frequency
fsPi = mean(1./diff(timePi));
fsUEI = 1/.00025;

% Convert Pi front accelerometer data to G
accelxPi = Pi_Data(:,2) * Sensitivity;
accelyPi = Pi_Data(:,3) * Sensitivity;
accelzPi = Pi_Data(:,4) * Sensitivity;

figure('Name',fig_title)
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1])

% Graph UEI Data
% subplot(2,1,1)
% hold on;
% plot(timeUEI,accelxUEI)
% 
% xindexmax = find(max(accelxUEI) == accelxUEI);
% xmax = accelxUEI(xindexmax);
% tmax = timeUEI(xindexmax);
% strmax = ['xmax = ',num2str(round(xmax,2)),' G\rightarrow'];
% text(tmax,xmax,strmax,'HorizontalAlignment','right');
% 
% plot(timeUEI,accelyUEI)
% 
% yindexmax = find(max(accelyUEI) == accelyUEI);
% ymax = accelyUEI(yindexmax);
% tmax = timeUEI(yindexmax);
% strmax = ['ymax = ',num2str(round(ymax,2)),' G\rightarrow'];
% text(tmax,ymax,strmax,'HorizontalAlignment','right');
% 
% plot(timeUEI,accelzUEI)
% 
% zindexmax = find(max(accelzUEI) == accelzUEI);
% zmax = accelzUEI(zindexmax(1));
% tmax = timeUEI(zindexmax(1));
% strmax = ['zmax = ',num2str(round(zmax,2)),' G\rightarrow'];
% text(tmax,zmax,strmax,'HorizontalAlignment','right');
% 
% title(['UEI Logger - ',str,' @ ',num2str(round(fsUEI,2)),' Hz'])
% legend('x','y','z')
% xlabel('Time (sec)')
% ylabel('Acceleration (Gs)')
% hold off;

% Graph Pi Data
hold on;
subplot(2,1,2)
plot(timePi,accelxPi)

xindexmax = find(max(accelxPi) == accelxPi);
xmax = accelxPi(xindexmax(1));
tmax = timePi(xindexmax(1));
strmax = ['xmax = ',num2str(round(xmax,2)),' G\rightarrow'];
text(tmax,xmax,strmax,'HorizontalAlignment','right');
hold off;

hold on;
plot(timePi,accelyPi)

yindexmax = find(max(accelyPi) == accelyPi);
ymax = accelyPi(yindexmax(1));
tmax = timePi(yindexmax(1));
strmax = ['ymax = ',num2str(round(ymax,2)),' G\rightarrow'];
text(tmax,ymax,strmax,'HorizontalAlignment','right');
hold off;

hold on;
plot(timePi,accelzPi)

zindexmax = find(max(accelzPi) == accelzPi);
zmax = accelzPi(zindexmax(1));
tmax = timePi(zindexmax(1));
strmax = ['zmax = ',num2str(round(zmax,2)),' G\rightarrow'];
text(tmax,zmax,strmax,'HorizontalAlignment','right');

title(['Pi - ',str,' @ ',num2str(round(fsPi,2)),' Hz'])
legend('x','y','z')
xlabel('Time (sec)')
ylabel('Acceleration (Gs)')
hold off;



% plot hz
for i = 1:(length(timePi)-1)
    hz1(i) = 1/(timePi(i+1)-timePi(i));
end

h = mean(hz1)



Fs = h;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(timePi);             % Length of signal

Y = fft(detrend(accelyPi));
Z = fft(detrend(accelzPi));
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
P2z = abs(Z/L);
P1z = P2z(1:L/2+1);
P1z(2:end-1) = 2*P1z(2:end-1);

f = Fs*(0:(L/2))/L;

% figure 
% subplot(2,1,1)
% plot(f,P1)
% title('HZ spec a1y')
% subplot(2,1,2)
% plot(f,P1z)
% title('HZ spec a1z')
y = lp50(detrend(accelyPi));
z = lp50(detrend(accelzPi));

figure
subplot(2,1,1)
plot(timePi,y)
title('filtered t vs a1y')
subplot(2,1,2)
plot(timePi,z)
title('filtered t vs a1z')


Fsf = h;            % Sampling frequency                    
Tf = 1/Fsf;             % Sampling period       
Lf = length(timePi);             % Length of signal

Yf = fft(y);
Zf = fft(z);
P2f = abs(Yf/Lf);
P1f = P2f(1:Lf/2+1);
P1f(2:end-1) = 2*P1f(2:end-1);
P2zf = abs(Zf/Lf);
P1zf = P2zf(1:Lf/2+1);
P1zf(2:end-1) = 2*P1zf(2:end-1);

ff = Fsf*(0:(Lf/2))/Lf;
figure
subplot(4,1,1)
plot(f,P1)
title('HZ spec a1y')
subplot(4,1,2)
plot(f,P1z)
title('HZ spec a1z')

subplot(4,1,3)
plot(ff,P1f)
title('filtered HZ spec a1y')
subplot(4,1,4)
plot(ff,P1zf)
title('filtered HZ spec a1z')
