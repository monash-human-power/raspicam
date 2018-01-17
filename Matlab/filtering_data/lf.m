function y = lf(x)
%LF Filters input x and returns output y.

% MATLAB Code
% Generated by MATLAB(R) 9.1 and the DSP System Toolbox 9.3.
% Generated on: 17-Jan-2018 14:17:13

%#codegen

% To generate C/C++ code from this function use the codegen command. Type
% 'help codegen' for more information.

persistent Hd;

if isempty(Hd)
    
    % The following code was used to design the filter coefficients:
    % % Equiripple Lowpass filter designed using the FIRPM function.
    %
    % % All frequency values are in Hz.
    % Fs = 800;  % Sampling Frequency
    %
    % Fpass = 100;             % Passband Frequency
    % Fstop = 110;             % Stopband Frequency
    % Dpass = 0.057501127785;  % Passband Ripple
    % Dstop = 0.0001;          % Stopband Attenuation
    % dens  = 20;              % Density Factor
    %
    % % Calculate the order from the parameters using FIRPMORD.
    % [N, Fo, Ao, W] = firpmord([Fpass, Fstop]/(Fs/2), [1 0], [Dpass, Dstop]);
    %
    % % Calculate the coefficients using the FIRPM function.
    % b  = firpm(N, Fo, Ao, W, {dens});
    
    Hd = dsp.FIRFilter( ...
        'Numerator', [0.000118546096118012 9.73415362206435e-05 ...
        -0.00014308069237356 -0.000827572869316628 -0.0020746534397138 ...
        -0.00379262610437111 -0.00561203279748747 -0.00694531399574736 ...
        -0.00718901471293391 -0.00600447607718037 -0.00354590226962067 ...
        -0.000499083125980333 0.00213384761331118 0.00344291808231036 ...
        0.00303292660239322 0.00124275398513012 -0.000977908897097431 ...
        -0.00250701453405647 -0.00260179486403906 -0.00127888736834013 ...
        0.000692187060838808 0.0022000958837014 0.00240088398891749 ...
        0.00119363120844814 -0.000712473587887195 -0.00219442578149395 ...
        -0.00236383128655956 -0.00109786816359934 0.000866114949278105 ...
        0.00234734408740164 0.00242176804386362 0.000995050604816487 ...
        -0.00110610175307284 -0.0026033568197996 -0.00253656936988673 ...
        -0.000874716411128261 0.00141868105560888 0.0029358134502504 ...
        0.00268172940587768 0.000720548531989719 -0.0018056209527821 ...
        -0.00333361612643448 -0.0028395453374945 -0.000516622251743878 ...
        0.0022736939143412 0.00379120511524268 0.00299475743784466 ...
        0.000245272171790608 -0.00283444980798718 -0.00430843476879641 ...
        -0.00313597867049521 0.000109378773540967 0.00349849935741158 ...
        0.00488330375509 0.00324815195106978 -0.00056807293905168 ...
        -0.00428048162317998 -0.00551439201578075 -0.0033116967847326 ...
        0.00116043590973541 0.00520493318398377 0.0062067146993803 ...
        0.00330677852140933 -0.00192306158545853 -0.00630646892468779 ...
        -0.00697277409924813 -0.00321379665971217 0.00289985937873377 ...
        0.00762928720853573 0.00782856073813672 0.00300443721452818 ...
        -0.00415436680663624 -0.0092378207881009 -0.00879543319067078 ...
        -0.0026290785058843 0.00579644011558754 0.0112484343774476 ...
        0.00992163113923843 0.00201464515115954 -0.00801036393024801 ...
        -0.0138688667034161 -0.0113045676308551 -0.00104160015253095 ...
        0.011129855738716 0.0174938475058017 0.0131399746910704 ...
        -0.000525413189493488 -0.0158486914443819 -0.0229772698838822 ...
        -0.0158611945495838 0.00327205452368457 0.0239542483454466 ...
        0.0326592752175151 0.0207688675997412 -0.00898979157623539 ...
        -0.0416066828638898 -0.0556772643196084 -0.03378253664182 ...
        0.0276811158834639 0.114452750709713 0.19876469220529 0.250576020584283 ...
        0.250576020584283 0.19876469220529 0.114452750709713 0.0276811158834639 ...
        -0.03378253664182 -0.0556772643196084 -0.0416066828638898 ...
        -0.00898979157623539 0.0207688675997412 0.0326592752175151 ...
        0.0239542483454466 0.00327205452368457 -0.0158611945495838 ...
        -0.0229772698838822 -0.0158486914443819 -0.000525413189493488 ...
        0.0131399746910704 0.0174938475058017 0.011129855738716 ...
        -0.00104160015253095 -0.0113045676308551 -0.0138688667034161 ...
        -0.00801036393024801 0.00201464515115954 0.00992163113923843 ...
        0.0112484343774476 0.00579644011558754 -0.0026290785058843 ...
        -0.00879543319067078 -0.0092378207881009 -0.00415436680663624 ...
        0.00300443721452818 0.00782856073813672 0.00762928720853573 ...
        0.00289985937873377 -0.00321379665971217 -0.00697277409924813 ...
        -0.00630646892468779 -0.00192306158545853 0.00330677852140933 ...
        0.0062067146993803 0.00520493318398377 0.00116043590973541 ...
        -0.0033116967847326 -0.00551439201578075 -0.00428048162317998 ...
        -0.00056807293905168 0.00324815195106978 0.00488330375509 ...
        0.00349849935741158 0.000109378773540967 -0.00313597867049521 ...
        -0.00430843476879641 -0.00283444980798718 0.000245272171790608 ...
        0.00299475743784466 0.00379120511524268 0.0022736939143412 ...
        -0.000516622251743878 -0.0028395453374945 -0.00333361612643448 ...
        -0.0018056209527821 0.000720548531989719 0.00268172940587768 ...
        0.0029358134502504 0.00141868105560888 -0.000874716411128261 ...
        -0.00253656936988673 -0.0026033568197996 -0.00110610175307284 ...
        0.000995050604816487 0.00242176804386362 0.00234734408740164 ...
        0.000866114949278105 -0.00109786816359934 -0.00236383128655956 ...
        -0.00219442578149395 -0.000712473587887195 0.00119363120844814 ...
        0.00240088398891749 0.0022000958837014 0.000692187060838808 ...
        -0.00127888736834013 -0.00260179486403906 -0.00250701453405647 ...
        -0.000977908897097431 0.00124275398513012 0.00303292660239322 ...
        0.00344291808231036 0.00213384761331118 -0.000499083125980333 ...
        -0.00354590226962067 -0.00600447607718037 -0.00718901471293391 ...
        -0.00694531399574736 -0.00561203279748747 -0.00379262610437111 ...
        -0.0020746534397138 -0.000827572869316628 -0.00014308069237356 ...
        9.73415362206435e-05 0.000118546096118012]);
end

y = step(Hd,double(x));


% [EOF]
