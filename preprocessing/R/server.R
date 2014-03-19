
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
# 
# http://www.rstudio.com/shiny/
#

library(shiny)

source("utils.R")
source("function.forms.R")
source("function.plots.R")

# Create a new list with name of the tree type as key and average diameters 
# vector as value
cache.file <- "../../cache/refdata.Rdata"
if (file.exists(cache.file)) {
  message("Cached reference data found, loading...")
  load(cache.file)
} else {
  reference.data <- read.reference.data("../../data/MV_data_kaikki.csv")
  message("Saving reference data to cache")
  save(reference.data, file=cache.file)
}

params <- read.table("../data/parameters-esmk.csv", header=TRUE,
                     as.is=TRUE, sep=",")
item <- reference.data[[4]]

mean <- 13.68
meadian <- 13
max <- 60
mod_asym <- 1
lscale <- 4
rscale <- 4
xrange <- 50

shinyServer(function(input, output) {
   
  output$sigmoidPlot <- renderPlot({
    
    transformed <- transform.sigmoidal(item, xmod=input$xmod, 
                                       mod.asym=mod_asym,
                                       scale=c(lscale, rscale),
                                       xrange=xrange)
    
    # Plotcurves. Max value is not calculated from the data, but is 
    # obtained as a parameter							
    sigmoidal.plot(transformed, xrange=1:xrange, main="Test", col="black",  
                   xlab="Lapimitta", ylab="Arvo", add=FALSE)
    
  })
  
})
