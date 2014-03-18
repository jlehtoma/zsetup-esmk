# TODO: Add comment
# 
# Author: jlehtoma
###############################################################################

sigmoidal.plot <- function(x, xrange, add=FALSE, ...) {
	
	#hist(x, xlab="Lapimitta", ylab="Frekvenssi", col="grey", border=FALSE, ...)
	#abline(v=median(x), col="red")
	#abline(v=mean(x), col="blue")
	
	#par("usr")
	#par(usr=c(par("usr")[1:2], 0, 1.0))
	
	if (!add) {
		plot(xrange, x, type="l", lwd=2.0, ...)
	} else {
		lines(xrange, x, type="l", lwd=1.5, ...)
	}
}

spline.plot <- function(data, ...) {
	
	x. <- 1:length(data)
	#browser()
	plot(x., data)
	curve(splinefun(x., data, method="mono")(x), add=TRUE, n = 200)
	#browser()
	axis(4)	
}
