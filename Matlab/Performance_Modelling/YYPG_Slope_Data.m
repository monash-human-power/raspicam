clear all; close all;
SlopeData = xlsread('YYPG Track Survey Data.xlsx');
Dist = SlopeData(:,2)';
Height = SlopeData(:,3)';
[fitresult, gof] = createFitSlope(Dist, Height);
coeffvalues(fitresult)
Slope = differentiate(fitresult,Dist);
Grad = Slope*100;
hold on
yyaxis right
plot(Dist,Grad)
