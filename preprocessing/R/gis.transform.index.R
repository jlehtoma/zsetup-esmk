library(raster)

# Set the workspace
if (.Platform$OS.type == "unix") {
	setwd("/home/jlehtoma/CodeVault/gdal/R/")
} else {
	setwd("C:/Users/admin_jlehtoma/workspace/gdal/R")
}

source("function.forms.R")
source("utils.R")

lookup <- function(value, dataA, dataB) {
	if (length(dataA) != length(dataB)) {
		stop("Datas must be of the same lengths")
	}
	for (i in 1:length(dataA)){
		if (dataA[i] == value) {
			return(dataB[i])
		}
	}
	return(NA)
}

transform.index <- function(data) {
  
  old <- raster(data[[1]])

  old.vals <- getValues(old, format="matrix")

  new.vals <- raster(lookup)

  #plot(index)
  extent(index) <- extent(lpm)
  out_name <- paste("output/", name, "_index.tif", sep="")
  browser()
  writeRaster(index, filename=out_name)
  paste("Finished transforming", name)
}

files <- list.files(TARGET)

for (item in files) {
  transform.index(item)
}