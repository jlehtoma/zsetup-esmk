# For functions: sigmoidal
source("preprocessing/R/utils.R")
source("preprocessing/R/function.forms.R")
source("preprocessing/R/function.plots.R")

# Create a new list with name of the tree type as key and average diameters 
# vector as value
data <- read.reference.data()
params <- read.parameters()

gr.device()
parop <- par(mfcol=c(2, 2))

# Loop over the data
for (i in 1:length(data)) {
	# Get the current tree type string for a name
	name <- names(data)[i]
	item <- data[[i]]
	#browser()
	# Extract relevant parameters, use only part of columns and the first row
	p.old <- params$old[params$old$Luokka == name,][5:13][1,]
	p.new <- params$new[params$new$Luokka == name,][5:13][1,]
	
	#browser()
	
	# Transform the data. Will use piece wise transformation even if there
	# is only one scale value (i.e. lscale and rscale are the same
	#transformed.old <- transform.sigmoidal(item, xmod=p.old$xmod, 
	#							                         mod.asym=p.old$mod_asym,
	#							                         scale=c(p.old$lscale, p.old$rscale))
	xrange = 70
  
	transformed.new <- transform.sigmoidal(item, xmod=p.new$xmod, 
								                         mod.asym=p.new$mod_asym,
								                         scale=c(p.new$lscale, p.new$rscale),
                                         xrange=xrange)
						
	# Plot both curves. Max value is not calculated from the data, but is 
	# obtained as a parameter
	#sigmoidal.plot(transformed.old, xrange=1:p.old$max, main=name, 
	#														col="blue")								
 	sigmoidal.plot(transformed.new, xrange=1:xrange, main=name, 
															col="black",  
															xlab="Lapimitta",
															ylab="Arvo",
															add=FALSE)
	print.params(name, p.new, "avdia")
}
