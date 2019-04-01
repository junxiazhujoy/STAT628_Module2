regressionData<-read.table("/Users/Anesthesia/Desktop/GUIDE628/roundData/RegData.txt", header=TRUE) 

#1
library(rpart)
# 我们可以使用help(rpart)来获取rpart的使用帮助,帮助文档Usage如下
# rpart(formula, data, weights, subset, na.action = na.rpart, method,
# model = FALSE, x = FALSE, y = TRUE, parms, control, cost, ...)
fit <- rpart(regressionData$stars~.,data=regressionData,method="class",parms=list(prior=c(.2,.2,.2,.2,.2)),control=rpart.control(xval=5))
pdf(file="/Users/Anesthesia/Desktop/GUIDE628/rpart/rpart.pdf")
#plot(fit,uniform=TRUE,main="Classification Tree") #画决策树图(数据量少，上面minsplit也小)
#text(fit,use.n=TRUE,all=TRUE)
#rpart.control对树进行一些设置  
#minsplit是最小分支节点数，这里指大于等于20，那么该节点会继续分划下去，否则停止  
#minbucket：树中叶节点包含的最小样本数  
#maxdepth：决策树最大深度 
#xval:交叉验证的次数
#cp全称为complexity parameter，指某个点的复杂度，对每一步拆分,模型的拟合优度必须提高的程度
library(rpart.plot)
rpart.plot(fit,type=1,main="classification tree by rpart")
# rpart.plot(fit, branch=1, branch.type=2, type=1, extra=102,
#            shadow.col="gray", box.col="green",
#            border.col="blue", split.col="red",
#            split.cex=1.2, main="classification tree by rpart")
dev.off()


## rpart包提供了复杂度损失修剪的修剪方法，printcp会告诉分裂到每一层，cp是多少，平均相对误差是多少
## 交叉验证的估计误差（“xerror”列），以及标准误差(“xstd”列)，平均相对误差=xerror±xstd
printcp(fit)
## 通过上面的分析来确定cp的值
## 我们可以用下面的办法选择具有最小xerror的cp的办法：

fit_prune <- prune(fit, cp=fit$cptable[which.min(fit$cptable[,"xerror"]),"CP"])

pdf(file="/Users/Anesthesia/Desktop/GUIDE628/rpart/rpart_prune.pdf")
library(rpart.plot)
rpart.plot(fit_prune,type=1,main="classification tree by pruning rpart")
# rpart.plot(fit, branch=1, branch.type=2, type=1, extra=102,
#            shadow.col="gray", box.col="green",
#            border.col="blue", split.col="red",
#            split.cex=1.2, main="classification tree by rpart")
dev.off()

printcp(fit_prune)
#misclassification error = root node error * xerror * 100%

data_model_pred <- predict(fit_prune,regressionData[,-72],type="class")
source("/Users/Anesthesia/Desktop/GUIDE628/rpart/count_result.R")
count_result(data_model_pred,regressionData$stars)
