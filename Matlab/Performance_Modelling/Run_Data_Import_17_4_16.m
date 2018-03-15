close all;
RunData = xlsread('Run_Data_17_4_16.xlsx');

PowerSectionA = (RunData(1:395,7))';
tSectionA = [1:length(PowerSectionA)];
FuncA = polyfit(tSectionA,PowerSectionA,6);

figure
plot(tSectionA,PowerSectionA)
hold on
plot(tSectionA,polyval(FuncA,tSectionA))

dSectionA = (RunData(1:395,5))';
dStart = dSectionA(1)
dSectionA = dSectionA-dStart;
FuncA2 = polyfit(dSectionA,PowerSectionA,6);

figure
plot(dSectionA,PowerSectionA)
hold on
plot(dSectionA,polyval(FuncA2,dSectionA))