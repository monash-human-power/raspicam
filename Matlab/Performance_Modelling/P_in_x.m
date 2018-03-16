function P_in_x = P_in_x(intensityfactor,P_GET,rateconst,P_MAX,srateconst,x,xs)
% P_in_x = intensityfactor*P_GET*(1-exp(rateconst*x));
if x<xs+1
    P_in_x = intensityfactor*P_GET*(1-exp(rateconst*0.1*x));
else
    P_in_x = intensityfactor*P_GET*(1-exp(rateconst*0.1*x))+P_MAX*exp(srateconst*0.1*(x-xs));
end
