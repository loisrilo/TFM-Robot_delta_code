
%TOW LINK SERIAL ROBOT:
%%
%Velocity kinematics:

syms a b O1 O2 %O1 = theta1, O2 = theta 2
x = a*cos(O1) + b*cos(O1+O2); %'symvar' could be helpfull sometimes.
y = a*sin(O1) + b*sin(O1+O2);

J = jacobian([x, y],[O1, O2])
%x_p = J * O_p

J_inv = inv(J)
%O_p = J_inv * X_p
%So the fucking thesis project of the swedish guy might be wrong...

%%
%DELTA-3 ROBOT
%%
%Model:

%codos (elbow): Pci
%la: upper arm length
%lb: forearm length
%O1: áng brazo 1 (0º)
%O2: arm 2 angle (120º)
%O3: arm 3 angle (240º)

syms R la lb O1 O2 O3

Pc1 = [ R+la*cos(O1), 0, la*sin(O1) ];
Pc2 = [ R+la*cos(O2), 0, la*sin(O3) ];
Pc3 = [ R+la*cos(O3), 0, la*sin(O3) ];

%Matriz de rotacion en torno a z, para colocar los tres brazos:
syms A1 A2 A3
RR1z = [cos(A1) -sin(A1) 0; sin(A1) cos(A1) 0; 0 0 1];
RR2z = [cos(A2) -sin(A2) 0; sin(A2) cos(A2) 0; 0 0 1];
RR3z = [cos(A3) -sin(A3) 0; sin(A3) cos(A3) 0; 0 0 1];

%Así la matriz Pc, que define la posición de los tres codos queda:
Pc = [Pc1*RR1z; Pc2*RR2z; Pc3*RR3z] 

%Ahora desde los codos las varillas se mueven libres, por lo que se define
%una esfera en cada codod de radio lb, la intersección de las tres esferas
%dará las 2 posiciones posibles, de las cuales una será descartada por ser
%físicamente imposible de alcanzar.
%ec. esfera: (x-xo)² + (y-yo)² + (z-zo)² = r²

%FORWARD KINEMATICS SYSTEM:
syms x y z
esf1 = (x-Pc(1,1))^2 + (y-Pc(1,2))^2 + (z-Pc(1,3))^2 %= lb^2;
esf2 = (x-Pc(2,1))^2 + (y-Pc(2,2))^2 + (z-Pc(2,3))^2 %= lb^2;
esf3 = (x-Pc(3,1))^2 + (y-Pc(3,2))^2 + (z-Pc(3,3))^2 %= lb^2;

%This system of 3 ecuations can be solved with a computer. This is our
%Forward kinematics system. Función útil: 'latex'

%%
%INVERSE KINEMATICS SYSTEM:
%Parámetros de diseño:
f = 200; %Lado triangulo superior (FF)
e = 100; %Lado triangulo inferior (EE)
global la
la = 100; %Brazo superior
global lb 
lb = 200; %Longitud brazo inferior

%Punto para prueba:
X = [48.7210  -31.3921  235.9008];

%
O = [0,0,0];
hf = sqrt(0.75*(f^2)); %Altura FF
he = sqrt(0.75*(e^2));

%Matriz de rotacion en torno a eje Z:
ang = 120; ang=ang*pi/180;
Rz = [cos(ang) -sin(ang) 0;
      sin(ang)  cos(ang) 0;
      0          0       1];

%calculos...
X1 = [X(1)+he/3, X(2), X(3)]; %Punto de union en el lateral del triángulo móvil.
global X1p
X1p = X1; X1p(2)=0; %Proyeccion sobre plano XZ.
global lbp
lbp = sqrt(lb^2-X(2)^2);
%Circunferencia centro en X1p y radio lbp -|

%Circunfencia centro en A1 y radio la:
global A1
A1 = [hf/3,0,0];
A2 = A1*Rz;
A3 = A2*Rz;

%opcion 1:
x0 = [1; 1];  % Make a starting guess at the solution
options = optimoptions('fsolve','Display','iter'); % Option to display output
[x,fval] = fsolve(@circunferencias,x0,options); % Call solver
%opcion 2: podemos poner restricicones!
y = lsqnonlin(@circunferencias,x0,[A1(1), 0]);

B1 = [x(1), 0, x(2)];
sol = atan(B1(3)/(B1(1)-A1(1))); %rads
sol = sol*180/pi;

%repetir para el resto de brazos...
%%