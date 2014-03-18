# TODO: Add comment
# 
# Author: jlehtoma
###############################################################################


# Set the workspace
if (.Platform$OS.type == "unix") {
	setwd("/home/jlehtoma/dev/src/gdalscripts/R/")
} else {
	setwd("C:/Users/jlehtoma/Documents/workspace/GDALscripts/R")
}

# For functions: sigmoidal
source("utils.R")
source("function.forms.R")

gr.device()
parop <- par(mfcol=c(1, 2))

old.koivu.transformed <- transform.sigmoidal(avdia.koivu, scale=4.0)
new.koivu.transformed <- transform.sigmoidal(avdia.koivu, xmod=5.0, mod.asym=0.9, scale=c(4.0 / 1.35, 4.0))
sigmoidal.plot(old.koivu.transformed, xrange=1:max(avdia.koivu), main="Koivu", col="blue")
sigmoidal.plot(new.koivu.transformed, xrange=1:max(avdia.koivu), main="Koivu", col="red", add=TRUE)