# Name: simulate_landscape.R
#
# Author: jlehtoma
###############################################################################

## Function create.landscape can be used to create landscapes of varying
## complexity.
## Params:
## x - matrix of coordinates, or vector of x coordinates
## y - vector of y coordinates
## z - vector of z coordinates
## model - string; describes the landscape model in
##         c("simple", "random", "GaussRF")
## patches - logical; indicates whether distinct patches are created
##           [NOT IMPLEMENTED]


batch.create.landscape <- function(n, ...) {
	landscapes <- list()
	for (i in 1:n) {
		landscapes[[paste("feat", i, sep="")]] = create.landscape(...)
	}
	return(landscapes)
}

# Generic wrapper for calling different landscape models
create.landscape <- function(x, y, z, ftype, patches=FALSE, ...) {

	ftypes <- c("simple", "random", "GaussRF")
	
	# Check the input data
	if (!is.vector(x) | !is.vector(y)) {
		msg = paste("Both x (", typeof(x), ") and y (", typeof(y),
				") need to be vectors.", sep="")
		stop(msg)
	}

	# Check the supported types
	if (!ftype %in% ftypes){
		msg <- paste("Type ", ftype, " not suitable. Use one of: ", ftypes)
		stop(msg)
	}

	switch(ftype,
			simple = create.simple.landscape(x, y, z, patches),
			random = create.random.landscape(x, y, z, patches),
			GaussRF = create.GaussRF.landscape(x, y, z, patches, ...))
}

create.simple.landscape <- function(x, y, z, patches) {
	return("Simple")
}

create.random.landscape <- function(x, y, z, patches) {
	return("Random")
}

## Create a landscape using Gaussian random field'
## Params:
## x - vector of x coordinates
## y - vector of y coordinates
## z - matrix of z values ...

create.GaussRF.landscape <- function(x, y, z=NULL, patches, seed=0,
		model="stable", mean=0, variance=10, nugget=1, scale=10, alpha=1.0,
		positive=TRUE) {

	if (!require(RandomFields)) {
		stop("Package RandomFields must be installed in order to proceed.")
	}

	# If a seed is provided, use that to always provide similar landscape
	if (seed) {
		set.seed(seed)
	}
	#browser()
	# Parameters for GaussRF, see ?GaussRF for more details
	f <- GaussRF(x=x, y=y, model=model, grid=TRUE,
			param=c(mean, variance, nugget, scale, alpha))

	# Get only positive values by adding minimun value to all elements
	if (positive) {
		f <- f + abs(min(f))
	}
	return(f)
}