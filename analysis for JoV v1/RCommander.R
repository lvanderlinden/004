library('lme4')
library('languageR')

print('EXPERIMENT 1 CORRECTED')

data <- read.csv('dm_exp004A_sacc1_endX1CorrNormToHandle.csv')
plot(data$saccLat1, data$endX1CorrNorm)
mme = lmer(endX1CorrNormToHandle ~ saccLat1 + (1|file) + (1|object), data=data)
sum = summary(mme)
print(sum)
pv = pvals.fnc(mme, nsim=10)
print(pv)        

print('EXPERIMENT 1 UNCORRECTED')

data <- read.csv('dm_exp004A_sacc1_endX1NormToHandle.csv')
plot(data$saccLat1, data$endX1NormToHandle)
mme = lmer(endX1NormToHandle ~ saccLat1 + (1|file) + (1|object), data=data)
sum = summary(mme)
print(sum)
pv = pvals.fnc(mme, nsim=10)
print(pv)        

print('EXPERIMENT 2')

data <- read.csv('dm_exp004B_sacc1_endX1NormToHandle.csv')
plot(data$saccLat1, data$endX1NormToHandle)
mme = lmer(endX1NormToHandle ~ saccLat1 + (1|file) + (1|object), data=data)
sum = summary(mme)
print(sum)
pv = pvals.fnc(mme, nsim=10)
print(pv)

Even goed kijken of ik idd de goede variabelen heb gebruikt! Dit script kan je gewoon ergens saven, bv in een script dat heet `lmm.r` en dan uitvoeren met de R interpreter:

Rscript lmm.r
