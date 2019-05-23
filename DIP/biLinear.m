function [fp] = biLinear(x, y, x1, x2, y1, y2, f11, f12, f21, f22)
    %%双线性插值
    %   params:
    %       [x y] 要估计的点、
    %       x1, y1, x2, y2, f11, f12, f21, f22     
        fp = 1.0/(x2-x1)/(y2-y1)*[x2-x x-x1]*[f11 f12;f21 f22]*[y2-y;y-y1];
    end