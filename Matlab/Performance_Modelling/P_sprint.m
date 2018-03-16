function P_sprint = P_sprint(P_MAX,srateconst,t,ts)

if t>ts
    P_sprint = P_MAX*exp(srateconst*(t-ts));
else
    P_sprint = 0;
end