# TODO: Add comment
#
# Author: jlehtoma
###############################################################################

create.batch.file <- function(filename = "run_multiple.bat", exe="zig2c.exe",
							  param="-r", dat, spp, output, uc=0.0, ds=0,
							  am=1.0, win=1, append=FALSE) {
	line <- paste("call", exe, param, dat, spp, output, uc, ds, am, win, "\n")

	task <- ifelse(append, "edited", "created")
	cat(line, file=filename, append=append)

	cat(paste("\n<<<", task, "batch file"), filename)
}

create.spp.file <- function(filename="filelist.spp", weight=1.0, alpha=1.0,
							bqp=1, bqp.p=1, cellrem=1, sppfiles) {
	for (i in 1:length(sppfiles)) {
		append <- ifelse (i == 1, FALSE, TRUE)
		line <- paste(weight, alpha, bqp, bqp.p, cellrem, sppfiles[i], "\n")
		cat(line, file=filename, append=append)
	}
	cat(paste("\n<<< Created spp file"), filename)
}

read.curves <- function(infile) {

	# Read in all the lines from curves input file
	# TODO: this is really slow
	lines <- readLines(infile)
	# Scan the lines until the header line is found
	for (i in 1:length(lines)) {
		if (grepl("Prop_landscape_lost", lines[i])) {
			# Mark the header line index
			lines <- i
		}
	}

	# Read in the curves file skipping the beginning lines
	dat <- data.frame(read.table(infile, as.is=TRUE, header=FALSE,
					             skip=lines))
	# Standard header entries
	header <- c("Prop_landscape_lost", "cost_needed_for_top_fraction",
			"min_prop_rem", "ave_prop_rem", "W_prop_rem", "ext-1", "ext-2")
	# Populate the rest of the header lines with sp headers.
	for (i in 1:(ncol(dat) - length(header))) {
		header <- append(header, paste("sp", i, sep=""))
	}
	colnames(dat) <- header
	# Assign S3 type class
	class(dat) <- "z.curve.plot"
	return(dat)
}

read.stats <- function(wildcard=".cmp$") {

	data <- list()

	# Get all the comparisons (.cmp) files
	# TODO: fix the wildcard so that it's strict about the extension
	files <- list.files(pattern=wildcard)

	# Loop over the comparison files

	for (i in 1:length(files)) {

		thresh <- read.table(files[i], nrows=10, as.is=TRUE, header=TRUE)
		lines <- readLines(files[i])
		tot <- grep("Total correlation", lines, value=TRUE)
		tot <- as.numeric(tail(strsplit(tot, ":")[[1]], 1))
		data[[files[i]]] <- list(thresh=thresh, total=tot)
	}
	class(data) <- "z.comp.plot"
	return(data)

}

plot.z.comp.plot <- function(x, y, show=TRUE, ...) {

	xrange <- seq(0.1, 1, .1)
	yrange <- seq(0.1, 1, .1)
	#browser()
	# Data structure of x:
	# list
	#	-comparison (list)
	#		-thresh (data frame)
	#		-total	(num)

	# Correlations
	windows()
	plot(xrange, yrange, type="n",  xlab="Features alone",
			ylab="Correlation", ylim=c(-0.1, 1.0))

	abline(h=0, col="grey")
	comparisons <- length(x)
	colors <- rainbow(comparisons)
	linetype <- c(1:comparisons)

	for (i in 1:comparisons){
		data <- x[[i]]$thresh
		#browser()
		lines(xrange, data$correlation, type="l", lwd=1.5,
			  lty=linetype[i], col=colors[i])
	}
	legend("topright", legend=names(x), col=colors,
			lty = linetype)
	savePlot("comparisons_correlation.png", type="png")
	if (!show) {
		dev.off()
	}

	#browser()
	windows()
	# Coverages
	plot(xrange, yrange, type="n",  xlab="Features alone",
			ylab="Coverage proportion" )
	abline(h=1, col="grey")
	for (i in 1:comparisons){
		data <- x[[i]]$thresh
		#browser()
		lines(xrange, data$cover, type="l", lwd=1.5,
				lty=linetype[i], col=colors[i])
	}
	legend("bottomleft", legend=names(x), col=colors,
			lty = linetype)
	text(10, 20, "foo")
	savePlot("comparisons_coverage.png", type="png")
	if (!show) {
		dev.off()
	}
}

plot.z.curve.plot <- function(x, y, ...) {
	nlines <- length(x) - 7
	nelems <- length(x[[8]])
	p <- palette(rainbow(nlines))
	plot(x[[8]], type="l", col=p[1], main="Performance curves",
			ylab="Proportion of ditribution lost",
			xlab="Fraction of landscape lost",
			xaxt="n")
	for (i in 9:length(x)) {
		points(x[[i]], type="l", col=p[length(x) + 2 - i])
	}
	axis(1, at=seq(0, nelems, nelems/10), labels=seq(0.0, 1, 0.1))
	legend("topright", legend=names(x[8:length(x)]), col=p,
			lty = rep(1, nlines))
}

#path <- "C:/Users/jlehtoma/Documents/EclipseWorkspace/Framework/trunk/framework/zonation/correct_output/3/"
#file <- "op1.curves.txt"
#df <- read.curves(paste(path, file, sep=""))
#plot(df)
#setwd(path)
#data <- read.stats()
#plot(data)