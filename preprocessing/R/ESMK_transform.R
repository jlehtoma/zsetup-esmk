# For functions: sigmoidal
source("preprocessing/R/utils.R")
source("preprocessing/R/function.forms.R")
source("preprocessing/R/function.plots.R")

# Create a new list with name of the tree type as key and average diameters 
# vector as value
reference.data <- read.reference.data()
params <- read.table("preprocessing/data/parameters-esmk.csv", header=TRUE,
                     as.is=TRUE, sep=",")

gr.device()
parop <- par(mfcol=c(2, 2))

# Loop over the data
for (i in 1:length(reference.data)) {
	# Get the current tree type string for a name
	name <- names(reference.data)[i]
	item <- reference.data[[i]]

	# Extract relevant parameters, use only part of columns and the first row
	params.spp <- params[params$Luokka == name,][5:13][1,]
	
	# Transform the data. Will use piece wise transformation even if there
	# is only one scale value (i.e. lscale and rscale are the same)
	xrange = 50
  
	transformed <- transform.sigmoidal(item, xmod=params.spp$xmod, 
								                     mod.asym=params.spp$mod_asym,
								                     scale=c(params.spp$lscale, 
                                             params.spp$rscale),
                                     xrange=xrange)
						
	# Plotcurves. Max value is not calculated from the data, but is 
	# obtained as a parameter							
 	sigmoidal.plot(transformed, xrange=1:xrange, main=name, col="black",  
                 xlab="Lapimitta", ylab="Arvo", add=FALSE)
	print.params(name, params.spp, "avdia")
}
