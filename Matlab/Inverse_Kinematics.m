function [theta1,theta2,theta3] = Inverse_Kinematics(EE)

%INVERSE KINEMATICS SYSTEM:
%Parámetros de diseño:
f = 125; %Lado triangulo superior (FF)
e = 130; %Lado triangulo inferior (EE)
global la
la = 150; %Brazo superior
global lb 
lb = 205; %Longitud brazo inferior

%Parámetros auxiliares
O = [0,0,0];
hf = sqrt(0.75*(f^2)); %Altura FF
he = sqrt(0.75*(e^2));
%Matriz de rotacion en torno a eje Z:
ang = 120; ang=ang*pi/180;
Rz = [cos(ang) -sin(ang) 0;
      sin(ang)  cos(ang) 0;
      0          0       1];
%Puntos triangulo superior
A1 = [hf/3,0,0];
A2 = A1*Rz;
A3 = A2*Rz;

%Theta1:
EE1 = [EE(1)+he/3, EE(2), EE(3)]; %Punto de union en el lateral del triángulo móvil.
%Circunferencia centro en X1p y radio lbp:
X1p = EE1; X1p(2)=0; %Proyeccion sobre plano XZ.
lbp = sqrt(lb^2-EE(2)^2);%Proyeccion radio.
%+Circunfencia centro en A1 y radio la:
%interseccion cirunferencias:
x0 = [1; 1];
options = optimoptions(@lsqnonlin,'Display','off');
x = lsqnonlin(@(x) circunferencias(x,lbp,X1p,A1),x0,[A1(1), 0],[],options);
%sol:
B1 = [x(1), 0, x(2)];
theta1 = atan(B1(3)/(B1(1)-A1(1)))*180/pi; %grados

%theta2:
%Todos los puntos que ya existiesen se rotan 240 grados (sentido positivo)
EE120 = EE*Rz;
EE240 = EE120*Rz;
EE2 = [EE240(1)+he/3, EE240(2), EE240(3)];
%Circunferencia centro X2p y radio lbp
X2p = EE2; X2p(2) = 0;
lbp = sqrt(lb^2-EE240(2)^2);
%+Circunferencia centro en A2 y radio la:
%interseccion:
x0 = [1; 1];
A240=A2*Rz*Rz;
x = lsqnonlin(@(x) circunferencias(x,lbp,X2p,A240),x0,[A240(1), 0],[],options);
%sol:
B2 = [x(1), 0, x(2)];
theta2 = atan(B2(3)/(B2(1)-A240(1)))*180/pi; %grados

%theta3:
%Todos los puntos que ya existiesen se rotan 120 grados!
EE3 = [EE120(1)+he/3, EE120(2), EE120(3)];
%Circunferencia centro en X3p y radio lbp
X3p = EE3; X3p(2) = 0; %Proyeccion sobre plano XZ.
lbp = sqrt(lb^2-EE120(2)^2);
%+Circunfencia centro en A3 y radio la:
%interseccion:
x0 = [1; 1];
A120=A3*Rz;
x = lsqnonlin(@(x) circunferencias(x,lbp,X3p,A120),x0,[A120(1), 0],[],options);
%sol:
B3 = [x(1), 0, x(2)];
theta3 = atan(B3(3)/(B3(1)-A120(1)))*180/pi; %grados

end