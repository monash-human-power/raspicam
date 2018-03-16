close all; clear all;

dvdt = @(t,v) (200-20*v)*(1/(20*v));
v0 = 1;
[t,v] = ode45(dvdt,[0,100],v0);
d = t.*v;
% sum(d(1:2))
% for k = 1:length(d)
%     dtotal(k) = sum(d(1:k));
% end
plot(t,v)
figure
plot(d,v)
%%
%To plot v as a funtion of t, use divide by the factor mv.
%To plot v as a funtion of d, use divide by the factor mv^2, 
%since dv/dt = v * dv/dx

dvdx2 = @(x,v) (200-20*v)*(1/(20*v*v));
[x2,v2] = ode45(dvdx2,[0,100],v0);
figure
plot(x2,v2)