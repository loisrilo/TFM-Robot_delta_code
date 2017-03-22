function F = circunferencias(x,lbp,Xp,A)
   
   global la
   
   %Circunferencia centro en Xp y radio lbp
   %Circunfencia centro en A y radio la
   %Plano XZ
   
   F=[(x(1)-Xp(1))^2 + (x(2)-Xp(3))^2  - lbp^2;
      (x(1)-A(1))^2 + (x(2))^2  - la^2];

end