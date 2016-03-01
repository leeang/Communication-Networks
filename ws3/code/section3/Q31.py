import math


######### Case 1 #########

srate=6         # service rate
arate=5         # arrrival rate

meandelay = 1/(srate-arate)
meansize = arate * meandelay

print 'Case 1'
print 'Mean theoretical delay: {:4f}'.format(meandelay)
print 'Mean theoretical size : {:4f}'.format(meansize)


######### Case 2 #########

srate=3         # service rate
arate=5         # arrrival rate

arate_new = arate * 0.5     # new arrrival rate

meandelay = 1/(srate-arate_new)
meansize = arate * meandelay

print ''
print 'Case 2'
print 'Mean theoretical delay: {:4f}'.format(meandelay)
print 'Mean theoretical size : {:4f}'.format(meansize)


######### Case 3 #########

srate=3         # service rate
arate=5         # arrrival rate
m=2             # number of servers

rho = float(arate) / (m * srate)

tmp = 0.0
for k in range(m):
    tmp += (m*rho)**k / math.factorial(k)

tmp += (m*rho)**m / math.factorial(m) / (1 - rho)
p0 = 1.0 / tmp

Nq = (m*rho)**m * rho / math.factorial(m) / (1-rho)**2 * p0
W = Nq / arate
meandelay = 1.0 / srate + W
meansize = arate * meandelay

print ''
print 'Case 3'
print 'Mean theoretical delay: {:4f}'.format(meandelay)
print 'Mean theoretical size : {:4f}'.format(meansize)
