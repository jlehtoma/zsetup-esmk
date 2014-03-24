library(raster)

custom.modal <- function(x, ...) {
  return(modal(x, ties="highest", ...))
}

input.file <- "data/msnfi/segments/20/segment_soil_fertility.tif"
output.file <- "data/msnfi/segments/60/segment_soil_fertility.tif"
input.raster <- raster(source.file)
(aggregate(source.raster, fact=3, fun=custom.modal, 
           filename=output.file, option=c("COMPRESS=YES")))
