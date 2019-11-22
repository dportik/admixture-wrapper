rm(list=ls())
library(sfsmisc)

####################################
#Plots for Admixture cross-validation results

#****Change path below to correct file
results <- read.delim("/ FULL PATH TO / NAME.CV_Avg.txt", header = TRUE, sep = "\t")
results

ls(results)
# Headers = "K" "CV_Avg" "CV_Stdev" 


#Plot average cross-validation error against K value
plot(results$K, results$CV_Avg, type = "b", pch=21, col="black", bg="gray", cex = 2, xlab = "K Value", ylab = "Cross-Validation Error")

#Use errbar function to Plot average cross-validation error (with SD error bars) against K value 
errbar(results$K, results$CV_Avg, results$CV_Avg + results$CV_Stdev, results$CV_Avg - results$CV_Stdev, 
       pch=22, col="black", bg="gray", cex=2, xlab = "K Value", ylab = "Cross-Validation Error")


####################################
