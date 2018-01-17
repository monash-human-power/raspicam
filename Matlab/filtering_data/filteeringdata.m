clear all
close all
clc

%Pi_1 front
Pi_1 = importdata('Pi_Test_3.txt');
%Pi_2 back
Pi_2 = importdata('Pi_Test_8_Front.csv');
%time_1
t1 = [Pi_1(:,1)];
%time_2
t2 = [Pi_2(:,1)];

% plot hz
for i = 1:(length(t1)-1)
    hz1(i) = 1/(t1(i+1)-t1(i));
end

for i = 1:(length(t2)-1)
    hz2(i) = 1/(t2(i+1)-t2(i));
end
h = mean(hz1);


%sensitivity
s = 0.488/1000;

fs = mean(hz1);
nf = fs/2;


% Convert Pi_1 accelerometer data to m/s2
a1x = Pi_1(:,2)*s ;  
a1y = Pi_1(:,3)*s ; 
a1z = Pi_1(:,4)*s ; 

% Convert Pi_2 accelerometer data to m/s2 

a2x = Pi_2(:,2)*s ;  
a2y = Pi_2(:,3)*s ; 
a2z = Pi_2(:,4)*s ; 

figure
hold on
plot(t1,a1x,t1,a1y,t1,a1z)

title('Pi_1 over time')
legend('x','y','z')
xlabel('time')
ylabel('m/s^2')

Fs = h;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(t1);             % Length of signal
t = (0:L-1)*T;
Y = fft(detrend(a1y));
Z = fft(detrend(a1z));
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
P2z = abs(Z/L);
P1z = P2z(1:L/2+1);
P1z(2:end-1) = 2*P1z(2:end-1);

f = Fs*(0:(L/2))/L;

figure 
subplot(2,1,1)
plot(f,P1)
title('HZ spec a1y')
subplot(2,1,2)
plot(f,P1z)
title('HZ spec a1z')
y = lp50(detrend(a1y));
z = lp50(detrend(a1z));
figure
subplot(2,1,1)
plot(t1,y)
title('filtered t vs a1y')
subplot(2,1,2)
plot(t1,z)
title('filtered t vs a1z')

% figure 
% 
% plot(t1,a1y)

Fs = h;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(t1);             % Length of signal
t = (0:L-1)*T;
Y = fft(y);
Z = fft(z);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
P2z = abs(Z/L);
P1z = P2z(1:L/2+1);
P1z(2:end-1) = 2*P1z(2:end-1);

f = Fs*(0:(L/2))/L;
figure
subplot(2,1,1)
plot(f,P1)
title('filtered HZ spec a1y')
subplot(2,1,2)
plot(f,P1z)
title('filtered HZ spec a1z')