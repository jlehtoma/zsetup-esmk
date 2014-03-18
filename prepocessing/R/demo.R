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

# Create some data
data <- runif(10, 5, 15)

## DEMO: scale

tr.data <- sigmoidal(x=1:max(data), asym=1.0, xmid=median(data), mod.asym=1.0, 
                     scale=1.0)
plot(tr.data, type="l", ylab="Benefit value", xlab="Data value", ylim=c(0.0, 1.1))
tr.data2 <- sigmoidal(x=1:max(data), asym=1.0, xmid=median(data), mod.asym=1.0, 
                      scale=0.5)
lines(tr.data2, col="blue")
tr.data3 <- sigmoidal(x=1:max(data), asym=1.0, xmid=median(data), 
                      mod.asym=1.0, scale=2.0)
lines(tr.data3, col="red")
abline(a=1.0, b=0, lty=2)
abline(v=median(data), lty=2)

## DEMO: xmod
tr.data <- sigmoidal(x=1:max(data), asym=1.0, xmid=median(data), mod.asym=1.0, 
                     scale=1.0)
plot(tr.data, type="l", ylab="Benefit value", xlab="Data value", ylim=c(0.0, 1.1))
tr.data2 <- sigmoidal(x=1:max(data), asym=1.0, xmid=median(data), xmod=2,
                      mod.asym=1.0, scale=1.0)
lines(tr.data2, col="blue")
tr.data3 <- sigmoidal(x=1:max(data), asym=1.0, xmid=median(data), xmod=-2,
                      mod.asym=1.0, scale=1.0)
lines(tr.data3, col="red")
abline(a=1.0, b=0, lty=2)
abline(v=median(data), lty=2)
abline(v=median(data) + 2, lty=2, col="blue")
abline(v=median(data) - 2, lty=2, col="red")

## DEBUGGING
# Seems like the while scaling / modding is conceptually wrong...

# MLP - plain
sigmoidal(11.35, asym=1.0, xmid=13, xmod=-1, mod.asym=1.0, scale=4.0)
# MLP - scaled and modded
t.max <- 40
sigmoidal(11.35, asym=1.0, xmid=(13 + t.max * -0.0166666), mod.asym=1.0, 
          scale=(t.max/15))
