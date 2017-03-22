%pruebas

%%%%%%%%%%%%%%%
%ECUACIONES:%%%
%%%%%%%%%%%%%%%
%%
%resolver ecuaciones:

syms a b c x
sol = solve(a*x^2 + b*x + c == 0)
sola = solve(a*x^2 + b*x + c == 0, a)
a=2; b=3; %...
subs(sola) %solucion con subtitucion;


syms x y z
e1 = x+2*y+3*z-5;
e2 = 3*x+y-5*z+2;
e3 = -x+3*y+z-2.5;
%solve(e1,e2,e3,x,y,z)

x=solve(e1,x);
e2 = subs(e2);
e3 = subs(e3);
y=solve(e2,y);
e3 = subs(e3);
z=solve(e3,z)
y=subs(y)
x=subs(x)

%Mismo sistema, solución matricial:
%[A]*[xyz]=[B] => [xyz]=[A]^(-1)*B;
A = [ 1  2  3;
      3  1 -5;
     -1  3  1];
B = [ 5; -2; 2.5];

sol=inv(A)*B

%%
x0 = [1; 1; 100];  % Make a starting guess at the solution
options = optimoptions('fsolve','Display','iter'); % Option to display output
[x,fval] = fsolve(@esferas,x0,options) % Call solver
%%
figure
hold on
Punto(B1,'k');
Punto(B1p,'k');
Punto(B2,'k');
Punto(B2p,'k');
Punto(B3,'k');
Punto(B3p,'k');
%%
%%%%%%%%%%%%%%%%%
%Plot Work Space%
%%%%%%%%%%%%%%%%%
%figure
hold on
a = 0;
step = 5;
WE = zeros(1000,3);
tic
for i=0:step:90
    for j=0:step:90
        for k=0:step:90
            A = End_Efector(i,j,k);
            a=a+1;
            WE(a,1:3) = A;
            if A(3)>0
                Punto(A,'b');
            else
                Punto(A,'r');
                [i,j,k]
            end
            drawnow
        end        
    end

end
toc
%%
x = WE(:,1);
y = WE(:,2);
z = WE(:,3);
rx = [max(x) min(x)]
ry = [max(WE(:,2)) min(WE(:,2))]
rz = [max(WE(:,3)) min(WE(:,3))]
%%
dx = 3;
dy = 3;
res = 5;
x_edge = [floor(min(x)):dx:ceil(max(x))] + abs(floor(min(x)))+1;
y_edge = [floor(min(y)):dy:ceil(max(y))] + abs(floor(min(y)))+1;
Z = zeros(length(x_edge),length(y_edge));
tic
for i = x_edge
    for j = y_edge
        fx = find(x>(i-res) & x<(i+res));
        fy = find(y>(i-res) & y<(i+res));
        c = intersect(fx,fy);
        c
        Z(i,j) = mean(z(c));
    end
    toc
end

%%
%nope
[X, Y] = meshgrid(x_edge, y_edge);
Z = griddata(x,y,z,X,Y);
for q = 1:size(Z,1)
    for w = 1:size(Z,2)
        if isnan(Z(q,w))
            Z(q,w) = 0;
        end
    end
end
surf(X,Y,Z)

%%
figure
hold on
A=[15 30 45;
   25 60 70;
   45 45 45;
   10 15 17];

for i = 1:length(A)
    B = End_Efector(A(i,1),A(i,2),A(i,3));
    Punto(B,'r');
    drawnow
    pause(0.5)
end
Plot_Kinematics(A(end,1),A(end,2),A(end,3));
%%
figure
hold on
A=[15 30 45;
   25 60 70;
   45 45 45;
   10 15 17];

for i = 1:length(A)
    B = Plot_Kinematics(A(i,1),A(i,2),A(i,3));
    hold off
    drawnow
    pause(0.5)
end

%%
%%%%%%%%%%%%%%%%%%
%WORKING WITH WE%%
%%%%%%%%%%%%%%%%%%

%plano de trabajo/dibujo a z=z0;
z0 = 330;
WEz = WE(:,3);
index_z0 = find(WEz > (z0-10) & WEz < (z0+10));
WE_at_z0 = WE(index_z0,:);

figure
hold on
for i=1:length(WE_at_z0)
    Punto(WE_at_z0(i,:),'k');
    drawnow
end

max(WE_at_z0)
min(WE_at_z0)
    