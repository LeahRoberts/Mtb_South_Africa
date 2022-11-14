library(ggplot2)
#install.packages('plyr')
library(plyr)

data <- read.csv("MICs.txt", sep='\t', header=TRUE)

data$mic = as.factor(data$mic)

plot_all <- ggplot(data, aes(x=mic, fill=type)) + geom_bar() + scale_y_log10()
plot_all

plot_all + facet_grid(rows = vars(type))
