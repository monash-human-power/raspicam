function P_roll = P_roll(m,g,mu,grad,v)

P_roll = m*g*mu*v*cos(atan(grad/100));