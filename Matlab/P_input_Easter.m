function P_input = P_input_Easter(polyFunc,t)

if t<405
    P_input = polyval(polyFunc,t);
elseif t > 460
    P_input = 50;
else
    P_input = 0.598*t + 29.7;
    
end