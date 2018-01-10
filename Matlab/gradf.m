function gradf = gradf(x,fitresult)
slope = differentiate(fitresult,x);
gradf = slope*100;


%gradf = -0.25*cos((pi/2000)*x);
%test gradient for a track 4000m long with max gradient +-0.25.