library(raster)
library(RandomFields)

# Set the workspace
if (.Platform$OS.type == "unix") {
	setwd("/home/jlehtoma/CodeVault/gdal/R/")
} else {
	setwd("C:/Users/admin_jlehtoma/workspace/gdal/R")
}

source("landscape.R")
source("function.forms.R")
source("utils.R")

###############################################################################
##
## Function creates a RasterStack of length n consisting of Gaussian random
## fields.
##
## Params:
## x - vector of x coordinates
## y - vector of y coordinates
## n 	- number of landscapes to be created
## model - string; describes the landscape model in
##         c("simple", "random", "GaussRF") [ONLY GaussRF implemented!]

rrasters <- function(x, y, n, model="GaussRF") {

  lscapes <- list()

  for (i in 1:n) {
    # Create independent feature distribution (landscape)
    lscapes[[paste("raster", i, sep="")]] = raster(create.landscape(x=x, y=y, 
							     ftype="GaussRF", 
							     mean=0,
							     variance=10, 
							     nugget=1, 
							     scale=10,
							     alpha=1))
  }
  #browser()
  # Create a RasterStack based on the landscapes
  lstack <- stack(lscapes)

  return(lstack)
}

# Set the dimensions for the artificial landscapes
x <- y <- seq(1, 100, step=1.0)

# Create the stack (this a bit pointless...)
rasters <- rrasters(x, y, n=2)
plot(rasters)

gr.device()

# Divide the stack into individual layers
raster1 <- rasters@layers[[1]]
raster2 <- rasters@layers[[2]]

# Create a product between the two
product <- raster1 * raster2
plot(product, main="Product")

# Calculate the logistic index [FIXME scale is hard coded]
vals <- getValues(product, format="matrix")
index <- raster(sigmoidal(vals, xmid=median(vals), scale=50.0))
index2 <- raster(sigmoidal(vals, xmid=median(vals) / 2, scale=50.0))
gr.device()
plot(index, main="Index")

# Write the data
writeRaster(raster1, filename="output/source1.tif")
writeRaster(raster2, filename="output/source2.tif")
writeRaster(product, filename="output/product.tif")
writeRaster(index, filename="output/index.tif")
writeRaster(index2, filename="output/index2.tif", overwrite=TRUE)