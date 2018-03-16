function P_input = P_input_Easter(polyFunc,x)

if x<4200
    P_input = polyval(polyFunc,x);
elseif x > 4900
    P_input = 50;
else
    P_input = 0.0598*x + 29.7;
    
end