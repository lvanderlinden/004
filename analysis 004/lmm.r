library('lme4')
library('languageR')

print('EXPERIMENT 1 CORRECTED')

# Load data file:
data <- read.csv('dm_exp004A_sacc1_endX1CorrNormToHandle.csv')

# Plot:
plot(data$saccLat1, data$endX1CorrNorm)

# MME:
mme = lmer(endX1CorrNormToHandle ~ saccLat1 + (1|file) + (1|object), data=data)
print(mme)
sum = summary(mme)
print(sum)

print('x')

pv = pvals.fnc(mme, nsim=10)
print(pv)        


# t-test:
#t = t.test(data$endX1CorrNormToHandle,mu=0) # Ho: mu=3
#print(t)
#sum = summary(t)
#print(sum)
#pv = pvals.fnc(t, nsim=10)
#print(pv)        


# 
# print('EXPERIMENT 1 UNCORRECTED')
# 
# data <- read.csv('dm_exp004A_sacc1_endX1NormToHandle.csv')
# plot(data$saccLat1, data$endX1NormToHandle)
# mme = lmer(endX1NormToHandle ~ saccLat1 + (1|file) + (1|object), data=data)
# sum = summary(mme)
# print(sum)
# #pv = pvals.fnc(mme, nsim=10)
# #print(pv)        
# 
# print('EXPERIMENT 2')
# 
# data <- read.csv('dm_exp004B_sacc1_endX1NormToHandle.csv')
# plot(data$saccLat1, data$endX1NormToHandle)
# mme = lmer(endX1NormToHandle ~ saccLat1 + (1|file) + (1|object), data=data)
# sum = summary(mme)
# print(sum)
# #pv = pvals.fnc(mme, nsim=10)
# #print(pv)
