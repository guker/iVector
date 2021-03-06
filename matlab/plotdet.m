function plothandle = plotdet(llrs, labels, color)
%plots det curves for given system
maxaxis = 20*5;
thresholds = -70:0.1:70;

numtrue = ones(1, size(llrs, 1));%array with i-th element equal number of classes with that label

%set up labels as a logical matrix to make life easier
labelMat = true(size(llrs));
for i = 1:size(labelMat, 1)
    labelMat(i, :) = (labels == i);
    numtrue(i) = sum(labelMat(i, :));
end
faweight = 100./((size(labelMat, 2)-numtrue)*size(labelMat, 1));
frweight = 100./(numtrue*size(labelMat, 1));

y = ones(size(thresholds));
x = ones(size(thresholds));

for i = 1:size(thresholds, 2),
    dec = llrs > thresholds(i);
    y(i) = sum(frweight*(~dec & labelMat));
    x(i) = sum(faweight*(dec & ~labelMat));

    %fa = sum(dec(:) & ~labelMat(:));
    %fr = sum(~dec(:) & labelMat(:));
    %y(i) = fr*100.0/tot;
    %x(i) = fa*100.0/tot;
end

[none, i] = min(abs(thresholds));
[none, eeri] = min(abs(y-x));
disp(['EER: ' num2str(y(eeri))])

if nargin == 2,
    plothandle = plot(x, y, 'b', x(i), y(i), 'bx', 'MarkerSize', 15);
else
    plothandle = plot(x, y, color, x(i), y(i), [color 'x'], 'MarkerSize', 15);
end


%holdstatus = ishold;
%hold on
%plot(x, x, 'c')
%if ~holdstatus,
%    hold off
%end

axis([0 maxaxis 0 maxaxis])
xlabel('False alarm probability (in %)')
ylabel('Miss probability (in %)')
grid on