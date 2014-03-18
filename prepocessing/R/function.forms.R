# TODO: Add comment
#
# Author: jlehtoma
###############################################################################

## A function to calculate heterogeneity indices based on different function
## forms.
## Parameters:
## data - list containing all the features used in the calculation
## form - string; indicates the specific function form used;
## 		  c("sqrt.multiply", "log.additive", "exp.additive", "additive" "window")
## weight - vector giving weights [0, 1]; default 1 -> all have equal weight

hgen <- function (data, form, weight=1, ...) {

  # Check the data
  if (!is.list(data)) {
    stop("Input data must be a list.")
  }
  if (length(data) <= 2) {
    stop("Operation need 2 or more matrices.")
  }
  for (i in 1:length(data)) {plto
    if (!is.matrix(data[[i]])) {
      stop("Provided list contains non-matrix elements.")
    }
    if (i == 1) {
      dims <- dim(data[[i]])
    } else if (dim(data[[i]])[1] != dims[1] | dim(data[[i]])[2] != dims[2]) {
      stop("Matrix dimensions do not match.")
    }
  }

  # Check the weight vector
  if (length(weight) > 1 & length(weight) != length(data)) {
    print("Provided weight vector different length than data, using 1 for all.")
    weight <- 1
  }

  # Apply weights, if 1 no need to apply
  if (length(weight) > 1) {
    for (i in 1:length(data)) {
		data[[i]] <- data[[i]] * weight[i]
	}
  }

  switch(form,
		  additive = .additive(data, ...),
		  exp.additive = .exp.additive(data, ...),
		  focal = .focal(data, ...),
		  log.additive = .log.additive(data, ...),
		  sqrt.multiply = .sqrt.multiply(data))
}

## hg.additive takes a list of matrices and returns their sum.
## Parameters.
## data - list holding more than 2 matrices

.additive <-function (data) {
	res <- 0
	for (mat in data) {
		res <- res + mat
	}
	return(res)
}

.exp.additive <- function(data) {
	res <- 0
	for (mat in data) {
		res <- res + mat
	}
	return(exp(res))
}

.focal <- function(data, layer, ...) {
	library(raster)
	temp <- raster(data[[layer]])

	# Typical parameters for focal
	# ngb - neighborhood
	# fun - statistics function
	# na.rm - remove nas

	values <- getValues(focal(temp, ...))
	#browser()
	return(matrix(values, nrow(data[[layer]]), ncol(data[[layer]])))
}

## hg.log.additive takes a list of matrices and returns a logarithm of their sum.
## Parameters.
## data - list holding more than 2 matrices
## base - integer; base of the logarithm (exp(base)); default is 1 (exp(1))

.log.additive <- function(data, base=1) {
	res <- 0
	for (mat in data) {
		res <- res + mat
	}
	return(log(res, base=exp(base)))
}

## hg.sqrt.multiply takes in a list of matrices and returns the square root of
## their product.
## Parameters:
## data - list holding more than 2 matrices

.sqrt.multiply <- function (data) {
  res <- 1
  for (mat in data) {
    res <- res * mat
  }
  return(sqrt(res))
}

## Sigmoidal transforms a vector by a custom sigmoidal (logistic) function.
## Parameters:
## x - a numeric vector of values at which to evaluate the model.
## asym - a numeric parameter representing the asymptote.
## xmid - a numeric parameter representing the x value at the inflection point 
##	      of the curve.
## xmod - a numeric modifier parameter for xmid
## scale - a numeric scale parameter on the input axis. 

sigmoidal <- function(x, asym=1.0, mod.asym=1.0, xmid, xmod=0, scale=1.0) {
  	# HACK! mod.asym is not used for anything, kept here to consume the 
	  # parameter (i.e. similar interface to asym.sigmoidal)
	  # CHANGE: parameter xmid MUST be explicitly provided -> previously used
    # if (is.na(xmid)) {
  	#   xmid <- median(x)
	  # }
    # check does not work as the x provided is 1:max(data), not data itself

  xmid <- xmid + xmod
  
	return(asym / (1 + exp((xmid-x)/scale)))
}

inverse.sigmoidal <- function(x, asym, xmid, scale) {
	
	return(xmid - scale *log(asym / x -1))
}

## Variant of the standard sigmoidal function that enables asymmetric scaling 
## parameters for each side of the function (as defined by the median).

asym.sigmoidal <- function(x, asym=1.0, mod.asym=1.0, xmid=NA, xmod= 0, 
                           lscale=1.0, rscale=1.0) {
	if (is.na(xmid)) {
		xmid <- median(x)
	}
  xmid <- xmid + xmod
  #browser()
	return(ifelse(x <= xmid,	 ((asym * mod.asym) / (1 + exp((xmid-x)/lscale))),
					(asym / (1 + exp((xmid-x)/rscale)))))
	
}

transform.sigmoidal <- function(x, xmid=NA, asym=1.0, xmod=0, mod.asym=1.0, 
                                scale=2.0, n=NA, xrange=NA, ...) {
	
	if (is.na(xmid)) {
		xmid <- median(x)
	}
  
  if (is.na(xrange)) {
    xrange = max(x)
  }
  
	#browser()
	if (length(scale) == 1) {
		transformed = sigmoidal(x=1:xrange, 
								            asym=asym, 
								            mod.asym=mod.asym, 
								            xmid=xmid,
                            xmod=xmod,
  								          scale=scale)
						
	} else if (length(scale) == 2) {
		      #browser()
          transformed = asym.sigmoidal(x=1:xrange, 
									                     asym=asym, 
                    									 mod.asym=mod.asym,
                    									 xmid=xmid,
                                       xmod=xmod,
                    									 lscale=scale[1], 
                    									 rscale=scale[2])
	}
	return(transformed)
}

