library(randomForest)
library(plyr)
library(randomForestExplainer)


data=read.csv("LVbars_Business_withStars.csv",header=TRUE)
head(data)
drops=c("city","latitude","longitude","name","categories","business_id","postal_code","state","hours","MondayOPEN","TuesdayOPEN","WednesdayOPEN","ThursdayOPEN","FridayOPEN","SaturdayOPEN","SundayOPEN","MondayCOLSED","TuesdayCOLSED","WednesdayCOLSED","ThursdayCOLSED","FridayCOLSED","SaturdayCOLSED","SundayCOLSED")
dat=data[ , !(names(data) %in% drops)]

RandomForest <- randomForest(dat$stars ~ ., data=dat, ntree=40, proximity=TRUE)
# ntree：指定随机森林所包含的决策树数目，默认为500
# proximity：逻辑参数，是否计算模型的临近矩阵，主要结合MDSplot()函数使用
rf
# 绘制每一棵树的误判率
plot(rf)
# importance()函数用于计算模型变量的重要性
importance(rf)
varImpPlot(RandomForest,n.var = 15)
# treesize：计算随机森林中每棵树的节点个数
head(treesize(rf,terminal = TRUE))
count_data <- as.data.frame(plyr::count(treesize(rf, terminal = TRUE)))
head(count_data,5)


# min_depth_frame <- min_depth_distribution(rf)
# save(min_depth_frame, file = "min_depth_frame.rda")
load("min_depth_frame.rda")
head(min_depth_frame, n = 10)

# plot_min_depth_distribution(forest) # gives the same result as below but takes longer
plot_min_depth_distribution(min_depth_frame)

plot_min_depth_distribution(min_depth_frame, mean_sample = "relevant_trees", k = 15)

# importance_frame <- measure_importance(forest)
# save(importance_frame, file = "importance_frame.rda")
load("importance_frame.rda")
importance_frame

# plot_multi_way_importance(forest, size_measure = "no_of_nodes") # gives the same result as below but takes longer
plot_multi_way_importance(importance_frame, size_measure = "no_of_nodes")


#delete the variables not shown in all the trees--less important
a=importance_frame
b=a[a$no_of_trees==40,]
tobeDeleted=setdiff(a$variable,b$variable)
dat2=dat[ , !(names(dat) %in% tobeDeleted)]
rf2 <- randomForest(dat2$stars ~ ., data=dat2, ntree=40, proximity=TRUE)
rf2
# 绘制每一棵树的误判率
plot(rf2)
# importance()函数用于计算模型变量的重要性
importance(rf2)
varImpPlot(rf2)
#min_depth_frame2 <- min_depth_distribution(rf2)
#save(min_depth_frame2, file = "min_depth_frame2.rda")
load("min_depth_frame2.rda")
head(min_depth_frame2, n = 10)
plot_min_depth_distribution(min_depth_frame2)
plot_min_depth_distribution(min_depth_frame2, mean_sample = "top_trees", k = 15)
#importance_frame2 <- measure_importance(rf2)
#save(importance_frame2, file = "importance_frame2.rda")
load("importance_frame2.rda")
importance_frame2



# (vars <- important_variables(forest, k = 5, measures = c("mean_min_depth", "no_of_trees"))) # gives the same result as below but takes longer
(vars <- important_variables(importance_frame2, k = 5, measures = c("mean_min_depth", "no_of_trees")))
interactions_frame <- min_depth_interactions(rf2, vars)
save(interactions_frame, file = "interactions_frame.rda")
load("interactions_frame.rda")
head(interactions_frame[order(interactions_frame$occurrences, decreasing = TRUE), ])
plot_min_depth_interactions(interactions_frame)




