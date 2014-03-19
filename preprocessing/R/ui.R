
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
# 
# http://www.rstudio.com/shiny/
#

library(shiny)

shinyUI(pageWithSidebar(
  
  # Application title
  headerPanel("New Application"),
  
  # Sidebar with a slider input for number of observations
  sidebarPanel(
    sliderInput("xmod", 
                "Xmodificator:", 
                min = -20, 
                max = 20, 
                value = 0)
  ),
  
  # Show a plot of the generated distribution
  mainPanel(
    plotOutput("sigmoidPlot")
  )
))
