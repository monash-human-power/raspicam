function CdA = CdAf(v,type)

if type == 1
    CdA = 0.0243;
    %Add variable CdA with speed form December testing
    % CdA = -0.001v + 0.0243
elseif type == 2
        CdA = 0.3;
        %Add unfaired CdA from testing
end
    