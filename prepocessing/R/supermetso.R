# TODO: Add comment
# 
# Author: admin_jlehtoma
###############################################################################

library(raster)

# Set the workspace
if (.Platform$OS.type == "unix") {
	setwd("/home/jlehtoma/dev/src/gdalscripts/R/")
} else {
	setwd("C:/Users/admin_jlehtoma/workspace/gdalscripts/R")
}

# For functions: sigmoidal
source("utils.R")
source("function.forms.R")
source("function.plots.R")
  
# Change WD to where the rasters really are
setwd("/var/run/media/jlehtoma/DataPocket/Data/Projects/SuperMetso/Data")

calculate.stats <- function(data) {
	
	current.names <- data[1]
	#browser()
	print(current.names)
	current.raster <-  raster(data[2])
	current.values <- getValues(current.raster)
	
	current.max <- max(current.values, na.rm=TRUE)
	current.median <- median(current.values, na.rm=TRUE)
	current.mean <- mean(current.values, na.rm=TRUE)
	
	print(current.max)
	print(current.median)
	print(current.mean)
	#browser()
}

# Define the raster files
file.list <- list('koivu' = 'vol_koivu.img',
			   	  'kuusi' = 'vol_kuusi.img',
			   	  'manty' = 'vol_manty.img',
			   	  'mlp' = 'vol_mlp.img')
		  
names.eng <- list('koivu' = 'Birch',
			  'kuusi' = 'Spruce',
			  'manty' = 'Pine',
			  'mlp' = 'Other deciduous')
		  
gr.device()
parop <- par(mfcol=c(2, 2))

params <- read.parameters('H:/Data/SuperMetso/MSNFI_params.csv')

for (i in 1:length(file.list)) {
	#calculate.stats(item)
	tree.spp <- names(file.list[i][1])
	
	data <- file.list[[i]]
	
	current.params <- params[params$luokka == tree.spp,][1:11][1,]
	print.params(tree.spp, current.params, label="vol")
  #browser()
	current.transformed <- transform.sigmoidal(x=1:current.params$max,
											                       xmid=current.params$xmid,
											                       xmod=current.params$xmod, 
											                       mod.asym=current.params$mod_asym,
											   scale=c(current.params$lscale, current.params$rscale))	
  
  print(paste("Minimum transformed value:", min(current.transformed)))
  
	flag <- TRUE
  	cut <- NA
	for (i in 1:length(current.transformed)) {	
		if (flag && current.transformed[i] >= 0.99) {
			print(tree.spp)
			#browser()
			msg <-  paste("VolSumma@0.99 =", i/16)
			flag <- FALSE
			print(msg)
      cut  <-  i + 100
		}
	}
  
  cut.transformed  <- current.transformed[1:cut] 
 
    #browser()
    sigmoidal.plot(cut.transformed, 
				   xrange=(1:current.params$max/16)[1:cut], 
				   main=names.eng[tree.spp][[1]],
				   ylab="SUITABILITY INDEX",
           xlab=quote(VOLUME (m^3 / ha)),
				   col="black",
           cex.lab=1.2)
}