function F = esferas(x)
   
   global lb
   global Pc
   
   F=[(x(1)-Pc(1,1))^2 + (x(2)-Pc(1,2))^2 + (x(3)-Pc(1,3))^2 - lb^2;
      (x(1)-Pc(2,1))^2 + (x(2)-Pc(2,2))^2 + (x(3)-Pc(2,3))^2 - lb^2;
      (x(1)-Pc(3,1))^2 + (x(2)-Pc(3,2))^2 + (x(3)-Pc(3,3))^2 - lb^2];

    if x(3)<0
        %solo nos valen soluciones de z positivo
        z=10000;
    end
  
%    F=[(x(1)-15)^2 + (x(2)-0)^2 + (x(3)-1.73)^2 - lb^2;
%       (x(1)-(-6))^2 + (x(2)-(-10))^2 + (x(3)-7.66)^2 - lb^2;
%       (x(1)-(-7))^2 + (x(2)-(13))^2 + (x(3)-3.42)^2 - lb^2];
end