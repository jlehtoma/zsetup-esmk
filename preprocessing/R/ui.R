
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
# 
# http://www.rstudio.com/shiny/
#

library(shiny)

shinyUI(pageWithSidebar(
  
  # Application title
  headerPanel("Conservation benefit functions"),
  
  # Sidebar with a slider input for number of observations
  sidebarPanel(
    selectInput("treespp", "Choose tree species:", 
                choices = c("Birch", "Other deciduous", "Pine", "Spruce")),
    sliderInput("xmod", 
                "X modificator:", 
                min = -20, 
                max = 20, 
                value = 0),
    sliderInput("mod_asym", 
                "Assymetry modificator:", 
                min = 0.9,
                max = 1.1, 
                value = 1.0),
    sliderInput("lscale", 
                "Left scale modifier:", 
                min = 0,
                max = 10, 
                value = 4),
    sliderInput("rscale", 
                "Right scale modifier:", 
                min = 0,
                max = 10, 
                value = 4)
  ),
  
  # Show a plot of the generated distribution
  mainPanel(
    plotOutput("sigmoidPlot"),
    tableOutput("paramview")
  )
))
