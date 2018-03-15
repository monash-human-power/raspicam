function P_inrun = P_inrun(intensityfactor,P_GET,rateconst,t,ts)
P_inrun = intensityfactor*P_GET*(1-exp(rateconst*t));
% if t<ts+1
%     P_inrun = intensityfactor*P_GET*(1-exp(rateconst*t));
% else
%     P_inrun = 0;
% end
