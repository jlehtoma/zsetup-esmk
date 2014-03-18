# TODO: Add comment
#
# Author: jlehtoma
###############################################################################

## A function to compare to to matrices in different ways, for example when
## comparing solutions created bu Zonation
## Parameters:
## x - matrix of values
## y - matrix of values
## fun - function that is used for comparison

comp <- function(x, y, fun="correlation", ...) {

	# Check the data
	if (!is.matrix(x) | !is.matrix(y)) {
		stop("Both inputs must be matrices.")
	}
	if (dim(x)[1] != dim(y)[1] | dim(x)[2] != dim(y)[2]) {
			stop("Matrix dimensions do not match.")
		}

	switch(fun,
			correlation = correlation(x, y, ...),
			substraction = substraction(x, y),
			frequency = selection.frequency(x, y, ...),
			coverage = selection.coverage(x, y, ...))
}

compare.solutions <- function(file1, file2, ...) {
	# Read in the solutions
	sol1 <- hg.read.asc.file(file1, rm.nodata=-1)
	sol2 <- hg.read.asc.file(file2, rm.nodata=-1)
	subs <- comp(sol1, sol2, fun="substraction")

	tsh <-  seq(0, 0.9, 0.1)
	corr <- comp(sol1, sol2, fun="correlation", thresholds=tsh)
	cover <- comp(sol1, sol2, fun="coverage", thresholds=tsh)
	return(list(thresholds=cbind(corr$classes, cover), totalcor=corr$total,
					subs=subs))
}

comp.suite <- function(x, input) {
	for (item in x){

		res <- compare.solutions(paste(item[1], ".rank.asc", sep=""),
							     paste(item[2], ".rank.asc", sep=""))

		filename <- paste(input, "comparisons_", item[1], "_", item[2],
					  ".cmp", sep="")

		write.table(res$thresholds, filename, col.names = TRUE, row.names = TRUE,
					quote=FALSE)

		cat(file=filename, paste("Total correlation:", res$totalcor, "\n"),
								 append=TRUE)

		write.asc.file(res$subs, filename, nrow(res$subs),
			ncol(res$subs))

		plot(read.stats(), show=FALSE)

	}
}

correlation <- function(x, y, method="spearman", thresholds=c(0)) {

	res <- c()
	for (i in 1:length(thresholds)) {
		x.sel <- as.vector(x[which(x > thresholds[i])])
		y.sel <- as.vector(y[which(y > thresholds[i])])
		res <- append(res, cor(x.sel, y.sel, method=method))
	}

	res <- data.frame(res, row.names=thresholds)
	colnames(res) <- "correlation"
	# Returns a list [1] threshold class correlations (data frame), [2] total
	# correlation
	return(list(classes=res, total=cor(as.vector(x), as.vector(y),
									   method=method)))
}

selection.coverage <- function(x, y, thresholds) {

	covs <- c()
	total <- c()
	for (thresh in thresholds) {
		sel1 <- which(x >= thresh)
		sel2 <- which(y >= thresh)

		# All produce the same indices -> is this real or not?
		total <- append(total, length(sel1) / length(x))
		covs <- append(covs, sum(sel1 %in% sel2) / length(sel1))
	}

	res <- data.frame(total=total, cover=covs, row.names=thresholds)
	return(res)
	plot(read.stats(), show=FALSE)
}

substraction <- function(x, y) {
	return(x - y)
}