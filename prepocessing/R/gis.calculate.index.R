library(raster)

# Set the workspace
if (.Platform$OS.type == "unix") {
	setwd("/home/jlehtoma/CodeVault/gdal/R/")
} else {
	setwd("C:/Users/admin_jlehtoma/workspace/gdal/R")
}

source("function.forms.R")
source("utils.R")

calculate.index <- function(data) {
  
  name <- names(data)
  lpm <- raster(paste("input/", data[[1]], sep=""))
  vol <- raster(paste("input/", data[[2]], sep=""))
 
  lpm_max <- max(getValues(lpm))
  vol_max <- max(getValues(vol))

  product <- lpm * vol

  vals <- getValues(product, format="matrix")

  # Get rid of zeros
  is.na(vals) <- vals == 0

  vals_max <- max(vals, na.rm=TRUE)

  # vals_max * data[[3]] inflates xmod back to real value relative to given
  # max value
  # vals_max / data[[4]] keeps the scale parameter relative to max value	
  index <- raster(sigmoidal(vals, xmid=median(vals) + (vals_max * as.double(data[[3]])), scale=(vals_max / as.double(data[[4]]))))

  #plot(index)
  extent(index) <- extent(lpm)
  out_name <- paste("output/", name, "_index.tif", sep="")
  browser()
  writeRaster(index, filename=out_name)
  paste("Finished transforming", name)
}

files <- list('koivu' = c('p_s_koivu_lpm.tif', 'p_s_koivu_vol.tif', 0, 11.25),
	      'kuusi' = c('p_s_kuusi_lpm.tif', 'p_s_kuusi_vol.tif', 0.08, 8.17),
	      'manty' = c('p_s_manty_lpm.tif', 'p_s_manty_vol.tif', 0.12, 6.23),
	      'mlp' = c('p_s_mlp_lpm.tif', 'p_s_mlp_vol.tif', -0.02, 15))

#gr.device()
#parop <- par(mfcol=c(2, 2))

for (item in files) {
  calculate.index(item)
}