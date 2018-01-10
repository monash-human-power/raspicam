function P_slope = P_slope(m,g,grad,v)

P_slope = m*g*sin(atan(grad/100))*v; 