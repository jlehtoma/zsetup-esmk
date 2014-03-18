# Script to describe rastere stats. Uses rgdal for IO-operations.
#
# Author: jlehtoma
###############################################################################

################################################################################
# Helper functions

gr.device <- function () {
  if (.Platform$OS.type == "unix") {
    x11()
  } else {
    windows()
  }
}

# Check that rgdal is available

if (!require('rgdal')) {
	install.packages('rgdal')
}

read.toMatrix <- function(file) {
    return(as.matrix(readGDAL(file)))
}

load.data <- function(files) {
  # Initiate the data list
  data <- vector("list", length(files))

  # Read in the data
  for (i in 1:length(files)) {
    data[[i]] <- read.toMatrix(files[i])
  }
  return(data)
}

describe <- function(files, lab=c(""), saveimg=FALSE, savestats=FALSE) {

  # Name of the sub-folder for saving images
  subfolder = "plots"
  
  if (savestats) {
    out_file <- paste("stats_", names(files)[1], ".csv", sep="")
  }

  # If labels are not provided, just use file names
  if (length(lab) <= 1) {
    lab <- files[[1]]
  }

  data <- load.data(files[[1]])

  # See if the provided labels are valid
  if (length(data) != length(labels)) {
    print("Data and label dimension do not match, using file names.")
    lab <- files[[1]]
  }

  # Get the number of data items to be described
  items <- length(data)
  # Set the plot parameters accordingly
  op <- par(mfcol=c(1, items))

  # Loop through the data items and do a histograms
  for (i in 1:items) {
    h <- hist(data[[i]], main=names(files), xlab=lab[i])
    if (savestats) {
      write(paste("\nBreaks for ", lab[i]), file=out_file, append=TRUE)
      write.table(data.frame("break"=h$breaks), file=out_file, append=TRUE, sep=";")
      write(paste("\nCounts for ", lab[i]), file=out_file, append=TRUE)
      write.table(data.frame("counts"=h$counts), file=out_file, append=TRUE, sep=";")
    }
  }

  if (saveimg) {
    # Check if sub folder exists in the current workspace
    #if (!file.exists(subfolder)) {
    #  dir.create(subfolder)
    #  print("Created sub-directory for plots.")
    #}

    savePlot(paste("hist_", lab[1], ".png", sep=""))
    dev.off()
  }

  # Set up new graphics device
  gr.device()

  # Transform the input data list to vectors
  indata <- sapply(data, as.vector)

  bxpl <- boxplot(data, main=names(files), names=labels)
  if (saveimg) {
    savePlot(paste("bxplot_", lab[1], ".png", sep=""))
    dev.off()
  }
  if (savestats) {
    stats <- data.frame(bxpl$stats)
    colnames(stats) <- lab
    rownames(stats) <- c("Low whisk", "Low hinge", "Median", "Up hinge", "Up whisk")
    write(paste("\nStats for", cat(lab)), file=out_file, append=TRUE)
    write.table(stats, file=out_file, append=TRUE, sep=";")
  }
  rm(data)
}

# Set the workspace
if (.Platform$OS.type == "unix") {
    setwd("")
} else {
    setwd("C:/Data/Staging/IndexStats/img")
}

input.files <- list("manty"=c("MH_PUULAJI_1_index.img", 
                              "MV_PUULAJI_1_index.img",
                              "MLVMI_PUULAJI_1_index.img"),
					          "kuusi"=c("MH_PUULAJI_2_index.img", 
                              "MV_PUULAJI_2_index.img",
                              "MLVMI_PUULAJI_2_index.img"),
					          "koivu"=c("MH_PUULAJI_3_index.img", 
                              "MV_PUULAJI_3_index.img",
                              "MLVMI_PUULAJI_3_index.img"),
					          "mlp"=c("MH_PUULAJI_4_index.img", 
                              "MV_PUULAJI_4_index.img",
                              "MLVMI_PUULAJI_4_index.img"))

labels <- c("MH-LTI", "MK-MV", "Metla-MLVMI")

for (i in 1:length(input.files)) {
  describe(input.files[i], labels,  saveimg=TRUE, savestats=TRUE)
}