dat=read.csv("att_df.csv")
dat$NoiseLevel=factor(sub(pattern="'(.*)'"   , replacement="\\1", x=dat$NoiseLevel))
model1=lm(stars~NoiseLevel*RestaurantsPriceRange2,dat)
model2=lm(stars~NoiseLevel,dat)
model3=lm(stars~RestaurantsPriceRange2,dat)
model4=lm(stars~NoiseLevel+RestaurantsPriceRange2,dat)

anova(model2)
anova(model3)

anova(model1)

anova(model2,model1) # model1 better
anova(model3,model1) # model1 better
anova(model4,model1) # model1 better


#summary(aov(model1))

#plot(dat$NoiseLevel,dat$RestaurantsPriceRange2)