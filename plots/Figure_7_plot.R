library(ggplot2)

data <- read.csv("MIC_change_results.txt", sep='\t', header=FALSE)

data$V5 <- factor(data$V5, levels=c("IS6110:779007", "IS6110:779075-79", 
                                    "A36V", "L40S", "L40fs", "C46G", 
                                    "C46fs:GSRAA", "C46fs:VIPSG", 
                                    "D47fs:LPSGS", "P48L", "P48fs:RAAVL", 
                                    "P48fs:trunc", "T58P", "G66fs:DQHQC", 
                                    "G66fs:SAPMP", "I67fs", "T69P", "N70D", 
                                    "A71fs", "L74M", "I80M", "L83P", "F93S", 
                                    "R96L", "P97fs", "A99P", "R109L", "R109P", 
                                    "Q115fs", "Q115trunc", "A124fs", "M139I", 
                                    "R140fs", "L142R", "Y145trunc", "R156fs:DTASE", 
                                    "Y157trunc"))

# MIC change all

ggplot(data, aes(x = V5, y = V3, colour = V5)) + 
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(colour= 1, size = 0.5) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("MIC change")

# MIC change n>3
data2 <- read.csv("MIC_change_results_common_vars.txt", sep='\t', header=FALSE)

ggplot(data2, aes(x = V5, y = V3, colour = V5)) + 
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(colour= 1, size = 0.5) +
  theme(axis.text.x = element_text(angle = 90)) + ylab("MIC change")
