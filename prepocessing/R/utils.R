# TODO: Add comment
# 
# Author: admin_jlehtoma
###############################################################################

gr.device <- function () {
	if (.Platform$OS.type == "unix") {
		x11()
	} else {
		windows()
	}
}

print.params <- function(name, params, label) {
	print("************************************")
	print(paste("***", name, "***"))
	print(paste(name, "xmod:", params$xmod))
	print(paste(name, "scale:", params$lscale))
	print(paste(name, "median", label, "=", params$median))
	print(paste(name, "mean", label, "=", params$mean))
	print(paste(name, "max", label, "=", params$max))
	# xmodded avdia -> scales xmod to value maximum -> normalizes [0,1]
	print(paste(name, "xmodded", label, "=", params$xmod  / params$max))
	# scaled avidia -> fraction of the used scale parameter of a given max
	print(paste(name, "scaled l", label, "=", params$max / params$lscale))
	print(paste(name, "scaled r", label, "=", params$max / params$rscale))
	print("************************************")
}

read.parameters <- function(inputfile=NA) {
	params  <- list()
	if (is.na(inputfile)) {
		# Set the workspace
		if (.Platform$OS.type == "unix") {
			setwd("/home/jlehtoma/dev/src/gdalscripts/R/")
		} else {
			setwd("C:/Users/admin_jlehtoma/workspace/gdalscripts/R")
		}
    #browser()
		params$new <- read.csv("parameters_new.csv", header=TRUE, sep=";", as.is=TRUE)
		params$old <- read.csv("parameters_old.csv", header=TRUE, sep=";", as.is=TRUE)	
	} else {
		params <- read.csv(inputfile, header=TRUE, sep=";", as.is=TRUE)
	}
	return(params)
}

read.reference.data <- function(inputfile=NA) {
	if (is.na(inputfile)) {
		# Set the workspace
		if (.Platform$OS.type == "unix") {
			setwd("/media/DataVault/Data/Metsakeskukset/Etela-Savo/Metsavara/MV_lpm_puusto")
			#setwd("/media/DataVault/Data/Metsakeskukset/Etela-Savo/Heterogeneity/MSNFI/North_section/tiff/")
		} else {
			setwd("G:/Data/Metsakeskukset/Etela-Savo/Metsavara/MV_lpm_puusto")
		}
	}
	# Read in the table data
	data <- read.table("MV_data_kaikki.csv", header=TRUE, quote = "\"'", sep=";", 
			as.is=TRUE)
	
	# Separate average diameters as an independent data frame
	avdia <- data.frame(koivu=data$koivu_klpm, kuusi=data$kuusi_lpm, 
			manty=data$manty_klpm, muulp=data$muulp_klpm)
	
	# summary(avdia)
	
	# Subset values (< 99 % quantile)
	# Mikä on osuus! Missä fiksattu raja menee?
	# Mitä tehd??n nollille ja kirjausvirheille?
	
	cutoff <- 0.0001
	q_koivu <- quantile(avdia$koivu, probs=(c(0, cutoff, 0.5, (1.0 - cutoff), 1.0)), 
			na.rm=TRUE)
	avdia.koivu <- subset(avdia$koivu, avdia$koivu < q_koivu[4] & avdia$koivu > 0)
	
	q_kuusi <- quantile(avdia$kuusi, probs=(c(0, cutoff, 0.5, (1.0 - cutoff), 1.0)), 
			na.rm=TRUE)
	avdia.kuusi <- subset(avdia$kuusi, avdia$kuusi < q_kuusi[4] & avdia$kuusi > 0)
	
	q_manty <- quantile(avdia$manty, probs=(c(0, cutoff, 0.5, (1.0 - cutoff), 1.0)), 
			na.rm=TRUE)
	avdia.manty <- subset(avdia$manty, avdia$manty < q_manty[4] & avdia$manty > 0)
	
	q_muulp <- quantile(avdia$muulp, probs=(c(0, cutoff, 0.5, (1.0 - cutoff), 1.0)), 
			na.rm=TRUE)
	avdia.muulp <- subset(avdia$muulp, avdia$muulp < q_muulp[4] & avdia$muulp > 0)

	# Create a new list with name of the tree type as key and average diameters 
	# vector as value
	data <- list("KOIVU"=avdia.koivu, "KUUSI"=avdia.kuusi, "MANTY"=avdia.manty, 
			"MLP"=avdia.muulp)

	return(data)
}
