function EE = End_Efector(theta1,theta2,theta3) 

%Kinematic plot delta robot:

%Parámetros de diseño:
f = 125; %Lado triangulo superior (FF)
e = 130; %Lado triangulo inferior (EE)
la = 150; %Brazo superior,200
global lb 
lb = 205; %Longitud brazo inferio,350

O = [0,0,0];
hf = sqrt(0.75*(f^2)); %Altura FF
he = sqrt(0.75*(e^2));

%Matriz de rotacion en torno a eje Z:
ang = 120; ang=ang*pi/180;
Rz = [cos(ang) -sin(ang) 0;
      sin(ang)  cos(ang) 0;
      0          0       1];

O1 = [-2*hf/3,0,0];
O2 = O1*Rz;
O3 = O2*Rz;

A1 = [hf/3,0,0];
A2 = A1*Rz;
A3 = A2*Rz;

%Rotación Brazos superiores:
%theta1 = 10;
theta1 = theta1*pi/180;
%theta2 = 10; 
theta2 = theta2*pi/180;
%theta3 = 10; 
theta3 = theta3*pi/180;

B1 = [A1(1)+la*cos(theta1) ,0 ,la*sin(theta1)];
B2 = [A1(1)+la*cos(theta2) ,0 ,la*sin(theta2)];
B2 = B2*Rz;
B3 = [A1(1)+la*cos(theta3) ,0 ,la*sin(theta3)];
B3 = B3*Rz; B3 = B3*Rz;
%desplazamos B a Bp con la distancia de los lados del triangulo movil a su
%centro para poder calcular la intersección con esferas.
vhe = [-he/3 0 0]; %vector de desplazamiento al centro del triangulo del EE.
B1p = B1 + vhe;
vhe = vhe*Rz;
B2p = B2 + vhe;
vhe = vhe*Rz;
B3p = B3 + vhe;
%Así la matriz Pc, que define la posición de los tres codos desplazados queda:
global Pc
Pc = [B1p; B2p; B3p];

%Ahora desde los codos las varillas se mueven libres, por lo que se define
%una esfera en cada codod de radio lb, la intersección de las tres esferas
%dará las 2 posiciones posibles, de las cuales una será descartada por ser
%físicamente imposible de alcanzar.
%ec. esfera: (x-xo)² + (y-yo)² + (z-zo)² = r²

%FORWARD KINEMATICS SYSTEM:
%fsolve...
x0 = [0; 0; 500];
options = optimoptions(@lsqnonlin,'Display','off');
x = lsqnonlin(@esferas,x0,[-500,-500,0],[],options);

EE=x';

end
