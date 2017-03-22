%generar trayectoria sencilla:

close all

t = [0:0.02:pi];
pos = 50*sin(t);
plot(t,pos,'*')

pf = zeros(size(pos));
pb = zeros(size(pos));
inc = 0;
for i = 2:length(pos)
    inc = inc + pos(i)-pos(i-1);
    if inc > 1
        pf(i) = 1;
        inc = inc - 1;
    end
    if inc < 1 & inc > -1
    end
    if inc < -1
        pb(i) = 1;
        inc = inc + 1;
    end
end

hold on
abs = 0;
for i = 1:length(pf)
    if pf(i) == 1
        abs = abs + 1;
    end
    if pb(i) == 1
        abs = abs - 1;
    end
    plot(t(i),abs,'ro');
end

%añadir ceros al final para tener bytes enteros
l = ceil(length(pf)/8)*8;
pf(l)=0;
pb(l)=0;

%cada fila es un byte:
PF = reshape(pf',8,ceil(l/8))';
PB = reshape(pb',8,ceil(l/8))';

%
nf = zeros(1, length(PF));
for i = 1:length(PF)
    byte = mat2str(PF(i,:));
    byte = byte(2:2:end);
    nf(i) = bin2dec(byte);
end

result = mat2str(nf);
for i=1:length(result)
    if result(i) == ' '
        result(i)=',';
    end
end
result

nb = zeros(1, length(PB));
for i = 1:length(PB)
    byte = mat2str(PB(i,:));
    byte = byte(2:2:end);
    nb(i) = bin2dec(byte);
end

result = mat2str(nb);
for i=1:length(result)
    if result(i) == ' '
        result(i)=',';
    end
end
result

