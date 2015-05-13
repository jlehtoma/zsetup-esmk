# For functions: sigmoidal
source("preprocessing/R/utils.R")
source("preprocessing/R/function.forms.R")
source("preprocessing/R/function.plots.R")

# Create a new list with name of the tree type as key and average diameters 
# vector as value
cache.file <- "cache/refdata.Rdata"
reference.data <- read.reference.data(cache.file=cache.file)
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
  
  vol <- seq(1, 150, length=xrange)
  names(vol) <- vol
  avdia <- 1:xrange
  names(transformed) <- avdia
  index <- outer(vol, transformed, "*")
  persp(x=vol, y=avdia, z=index, theta=-45, phi=15, xlab = "Vol", 
        ylab = "Avdia", zlab = "Index", main=name, zlim=c(0, 150))
  print(range(index))
  
  print.params(name, params.spp, "avdia")
}

# Simple square root transformation

vol <- seq(1, 150, length=xrange)
names(vol) <- vol
age <- 1:120
names(age) <- age
f <- function(x, y) {r  <- sqrt(x * y)}
index <- outer(vol, age, f)
persp(x=vol, y=age, z=index, theta=-45, phi=15, xlab = "Vol", 
      ylab = "Age", zlab = "Index", zlim=c(0, 150))
