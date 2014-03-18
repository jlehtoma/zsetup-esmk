# TODO: Add comment
# 
# Author: admin_jlehtoma
###############################################################################
library(raster)


setwd("C:/Data/Staging/IndexStats/img")

MH.data <- list("manty"=values(raster("MH_PUULAJI_1_index.img")), 
                "kuusi"=values(raster("MH_PUULAJI_2_index.img")),
				        "koivu"=values(raster("MH_PUULAJI_3_index.img")), 
                "mlp"=values(raster("MH_PUULAJI_4_index.img")))

MV.data <- list("manty"=values(raster("MV_PUULAJI_1_index.img")), 
                "kuusi"=values(raster("MV_PUULAJI_2_index.img")),
  			        "koivu"=values(raster("MV_PUULAJI_3_index.img")), 
                "mlp"=values(raster("MV_PUULAJI_4_index.img")))

MLVMI.data <- list("manty"=values(raster("MLVMI_PUULAJI_1_index.img")), 
                "kuusi"=values(raster("MLVMI_PUULAJI_2_index.img")),
    		        "koivu"=values(raster("MLVMI_PUULAJI_3_index.img")), 
                "mlp"=values(raster("MLVMI_PUULAJI_4_index.img")))

#MH.summary <- sapply(MH.data, function(x) {summary(x)}) 
#MV.summary <- sapply(MV.data, function(x) {summary(x)})
#MLVMI.summary <- sapply(MLVMI.data, function(x) {summary(x)})

#stats <- rbind(MH.summary, MV.summary, MLVMI.summary)
#write.csv(stats, "all_stats.csv")

png("plots/01_manty_boxplot.png", width=1000, height=800, pointsize=16)
parop <- par(mfcol=c(1, 3))
boxplot(MH.data$manty, main="MH", notch=TRUE, ylim=c(0, 515.4))
boxplot(MV.data$manty, main="MV", notch=TRUE, ylim=c(0, 515.4))
boxplot(MLVMI.data$manty, main="MLVMI", notch=TRUE, ylim=c(0, 515.4))
dev.off()

png("plots/02_kuusi_boxplot.png", width=1000, height=800, pointsize=16)
parop <- par(mfcol=c(1, 3))
boxplot(MH.data$kuusi, main="MH", notch=TRUE, ylim=c(0, 475.1))
boxplot(MV.data$kuusi, main="MV", notch=TRUE, ylim=c(0, 475.1))
boxplot(MLVMI.data$kuusi, main="MLVMI", notch=TRUE, ylim=c(0, 475.1))
dev.off()

png("plots/03_koivu_boxplot.png", width=1000, height=800, pointsize=16)
parop <- par(mfcol=c(1, 3))
boxplot(MH.data$koivu, main="MH", notch=TRUE, ylim=c(0, 326.1))
boxplot(MV.data$koivu, main="MV", notch=TRUE, ylim=c(0, 326.1))
boxplot(MLVMI.data$koivu, main="MLVMI", notch=TRUE, ylim=c(0, 326.1))
dev.off()

png("plots/04_mlp_boxplot.png", width=1000, height=800, pointsize=16)
parop <- par(mfcol=c(1, 3))
boxplot(MH.data$mlp, main="MH", notch=TRUE, ylim=c(0, 419.8))
boxplot(MV.data$mlp, main="MV", notch=TRUE, ylim=c(0, 419.8))
boxplot(MLVMI.data$mlp, main="MLVMI", notch=TRUE, ylim=c(0, 419.8))
dev.off()
