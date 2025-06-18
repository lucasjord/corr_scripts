#!/usr/bin/octave

# Ceduna
load cd.tspec;
# Wark
load wa.tspec;
# Hobart12
load hbX.tspec
load hbY.tspec
# Katherine
load keX.tspec
load keY.tspec

# formatting
x1 = cd(:,1)+6660;
C  = cd(:,[12,16]);
C(C>10) = 1.5;
#
W = wa(:,[ 4, 8]);
W(W>10) = 1.5;
#
x2 = hbX(:,1)+6644;
H  = [hbX(:,4),hbY(:,4)];
#
K  = [keX(:,4),keY(:,4)];

# plotting
figure(1)
plot(x1,W(:,1),'r');
hold on
plot(x1,W(:,2),'b');
xlim([6666,6672]); ylim([.5,4]);
title('Warkworth30');
print -dpdf warkspec.pdf

hold off
plot(x1,C(:,1),'r');
hold on
plot(x1,C(:,2),'b');
xlim([6666,6672]); ylim([.5,4]);
title('Ceduna30');
print -dpdf ceduspec.pdf

hold off
plot(x2,H);
xlim([6666,6672]); ylim([.5,4]);
title('Hobart12')
print -dpdf hobaspec.pdf

hold off
plot(x2,K);
xlim([6666,6672]); ylim([.5,4]);
title('Katherine12')
print -dpdf kathspec.pdf

