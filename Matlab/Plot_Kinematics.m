function EE = Plot_Kinematics(theta1,theta2,theta3) 

%Kinematic plot delta robot:

%Parámetros de diseño:
f = 125; %Lado triangulo superior (FF)
e = 130; %Lado triangulo inferior (EE)
la = 150; %Brazo superior
global lb 
lb = 205; %Longitud brazo inferior

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
% x0 = [1; 1; 100];  % Make a starting guess at the solution
% options = optimoptions('fsolve','Display','off'); % Option to display output
% [x,fval] = fsolve(@esferas,x0,options); % Call solver

x0 = [0; 0; 500];
options = optimoptions(@lsqnonlin,'Display','off');
x = lsqnonlin(@esferas,x0,[-500,-500,0],[],options);
%sol:


EE=x';

%uniones a los laterales del EE para cada brazo:
vhe = [-he/3 0 0];
C1 = EE - vhe;
vhe = vhe*Rz;
C2 = EE -vhe;
vhe = vhe*Rz;
C3 = EE -vhe;
%...puntos union!

%Plotear posición robot delta:
%figure
Punto(O,'k');
hold on
Linea(O1,O2,'k');
Linea(O2,O3,'k');
Linea(O3,O1,'k');
Punto(A1,'b');
Punto(A2,'r');
Punto(A3,'g');
Punto(B1,'b');
Linea(A1,B1,'b');
Punto(B2,'r');
Linea(A2,B2,'r');
Punto(B3,'g');
Linea(A3,B3,'g');
Punto(EE,'k');
Linea(B1,C1,'b');
Linea(B2,C2,'r');
Linea(B3,C3,'g');
Punto(C1,'b');
Punto(C2,'r');
Punto(C3,'g');
Linea(C1,EE,'k');
Linea(C2,EE,'k');
Linea(C3,EE,'k');
view(60,45)

end
