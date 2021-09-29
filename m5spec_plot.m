function m5spec_plot(file);
% Plot the output from m5spec commands such as
% ...
% file = Name of text file with m5spec output

spec=load(file);
dimen = size(spec);
maxes = 2:(dimen(2));
for i = 2:dimen(2)
   maxes(i) = max(spec(:,i)); 
end
minimax = min(maxes);
figure(1);
clf;
hold off;
w = round((dimen(2)-1)^0.5);
for i = 2:dimen(2)
    subplot(w,w,i-1);
    window = 4; %int64(length(smpec(:,i))/1024);
    y = spec(:,i); %smoothdata(spec(:,i), 'rlowess', window);
    plot(spec(:,1),y);
    %lab = sprintf('Channel %i',i-1);
    %axis([min(spec(:,1)) max(spec(:,1)) 0 0])
    %title(lab);
end

return
