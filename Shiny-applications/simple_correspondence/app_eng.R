# This is an application for conducting simple correspondence analysis on linguistic phenomena illustrating synthetic and analytic constructions in Estonian dialects.
# The input file is a frequency table ("koondKoond.csv") in UTF-8 encoding and with the following structure: cat;EASTERN;MID;NORTHEASTERN;WESTERN;MULGI;COASTAL;INSULAR;SETO;TARTU;VORU;domain;construction. The last two columns are for filtering the phenomena and are left out from the actual analysis.

# 1. Load all the necessary packages (if the packages are not yet installed, so so using install.packages("packagename"))
library(ca)
library(FactoMineR)
library(ggplot2)
library(shiny)

# 2. Read in the data
data = read.csv2("koondKoond.csv", fileEncoding = "UTF-8")

#####################################################################################
###### The application ##############################################################
#####################################################################################

############################
#### UI for CA analyses ####
############################

ui <- shinyUI(fluidPage(
    
    # 3. The title
    titlePanel("Correspondence Analysis"),
    
    # 4. Introduction
    p("This is an application that draws a simple correspondence analysis plot illustrating analytic and synthetic parallel forms in Estonian dialects. The nominal features (locative cases vs. adpositions) and the verbal features (quotatives, passives and negation) can be analysed both separately and jointly. The simple correspondence analysis only displays the frequency-based associations between the dialects and the features, but no intercategorial associations. The other tabs also display the output of the analysis and the input table. To change the choices, press the button 'Update'"), 
    
    # 5. The rest of the UI in two blocks: one contains the specs for the input, the other for the output.
    fluidRow(
        
        ## 6. Input specs
        column(3, 
               
               ### 7. Selection of either nominal or verbal features
               selectInput("domain",label = "Choose nominal or verbal features:",choices = c("nominal", "verbal", "both"), selected = "nominal"),
               
               ### 8. Selection of the construction.
               #### If any of the conditions in the conditional panels is met, a checbox selection, corresponding to the condition, appears
               conditionalPanel("input.domain == 'both'",
                                checkboxGroupInput("category_all", label = "Choose the construction:", choices = levels(data$construction), selected = levels(data$construction))),
               
               conditionalPanel("input.domain == 'nominal'",
                                checkboxGroupInput("category_nominal", label = "Choose the construction:", choices = levels(droplevels(data[data$domain == "nominal", 13])), selected = levels(droplevels(data[data$domain == "nominal", 13])))),
               
               conditionalPanel("input.domain == 'verbal'",
                                checkboxGroupInput("category_verbal", label = "Choose the construction:", choices = levels(droplevels(data[data$domain == "verbal", 13])), selected = levels(droplevels(data[data$domain == "verbal", 13])))),
               
               ### 9. Update button
               actionButton("update", "Update"),
               
               ### 10. Empty rows
               br(),
               br(),
               br(),
               
               ### 11. Colour selection
               selectInput("colours1", label = "Choose the colour of the constructions:", choices = c("black", "green", "blue", "red", "orange", "yellow", "purple", "pink", "grey", "brown"), selected = "black"),
               
               selectInput("colours2", label = "Choose the colour of the dialects:", choices = c("black", "green", "blue", "red", "orange", "yellow", "purple", "pink", "grey", "brown"), selected = "orange"),
               
               ### 12. File type selection
               radioButtons("extension", label = "Choose file extension for downloading:", choices = c("png", "tiff", "pdf"), selected = "png"),
               
               ### 13. Download button
               downloadButton("download", label = "Download the plot")
        ),
        
        ## 16. Output specs
        column(8,
               
               ### 17. The outputs will be displayed in separate tabs
               tabsetPanel(
                   
                   #### 18. The plot tab
                   tabPanel("Plot",
                            conditionalPanel("output.rows > 2", plotOutput("plot")),
                            conditionalPanel("output.rows <= 2", textOutput("text"))),
                   
                   #### 19. The analysis output tab
                   tabPanel("CA",
                            conditionalPanel("output.rows > 2", verbatimTextOutput("catable")),
                            conditionalPanel("output.rows <= 2", textOutput("text2"))),
                   
                   #### 20. The input table tab
                   tabPanel("InputTable", tableOutput("inputtable"))
                            
               )
        )
    )
    
))

#########################################
#### Server for the analyses ############
#########################################

server <- shinyServer(function(input, output) {
    
    # 21. Selection of the input table
    selected_table <- reactive({
        
        ## 22. Change the input table only when the "update" button is pressed
        input$update
        
        isolate({
            withProgress({
                setProgress(message = "Loading...")
                
                ##### 23. If the user selects the nominal features, then...
                if (input$domain == "nominal") {
                    
                    ###### 24. filter the input table for only nominal categories.
                    inputtable0 = droplevels(data[data$domain == "nominal",])
                    inputtable = NULL
                    for (i in input$category_nominal) {
                        inputtable = rbind(inputtable, droplevels(inputtable0[inputtable0$construction == i, 1:11]))
                    }
                
                ##### 25. If the user selects the verbal features, then...        
                } else if (input$domain == "verbal") {
                    
                    ###### 26. filter the input table for only verbal features.
                    inputtable0 = droplevels(data[data$domain == "verbal",])
                    inputtable = NULL
                    for (i in input$category_verbal) {
                        inputtable = rbind(inputtable, droplevels(inputtable0[inputtable0$construction == i, 1:11]))
                    }
                    
                ##### 27. If the user selects both features, then...
                } else {
                    
                    ###### 28. create the input table for all categories.
                    inputtable = NULL
                    for (i in input$category_all) {
                        inputtable = rbind(inputtable, droplevels(data[data$construction == i, 1:11]))
                    }
                }
                
                ##### 29. Set the category column to row names
                rownames(inputtable) <- inputtable[,1]
                inputtable <- inputtable[,-1]
            })
        })
    })
    
    # 30. Displaying the input table
    output$inputtable <- renderTable({
        selected_table()
    })
    
    # 31. A reactive part of the output, which preserves the number of rows in the data table, so that the program would display its own error message instead of R's, when this number is less than 3.
    output$rows <- reactive({
        nrow(selected_table())
    })

    # 32. A function, which enables the server and UI to interact, when the UI does not define an input, but it is still used in the output.
    outputOptions(output, "rows", suspendWhenHidden=FALSE)
    
    # 33. CA analysis
    ca_analysis <- function() {
            CA(selected_table())
    }
    
    # 34. Displaying the CA analysis output
    output$catable <- renderPrint({
        summary(ca_analysis(), nb.dec = 2)
    })
    
    # 35. Displaying a warning message about the plot
    output$text <- renderText({
        "Can't perform the analysis: the construction has less than 3 levels. Add categories."
    })
    
    # 36. Displaying a warning message about the CA table
    output$text2 <- renderText({
        "Can't perform the analysis: the construction has less than 3 levels. Add categories."
    })
    
    # 37. A function for selecting the colour for the constructions
    colorInput1 <- reactive({
        switch(input$colours1, "black" = "black", "green" = "forestgreen", "blue" = "dodgerblue3", "red" = "firebrick3", "yellow" = "goldenrod2", "orange" = "darkorange3", "purple" = "darkorchid4", "pink" = "deeppink3", "grey" = "grey40", "brown" = "chocolate4")
    })
    
    # 38. A function for selecting the colour for the dialects
    colorInput2 <- reactive({
        switch(input$colours2, "black" = "black", "green" = "forestgreen", "blue" = "dodgerblue3", "red" = "firebrick3", "yellow" = "goldenrod2", "orange" = "darkorange3", "purple" = "darkorchid4", "pink" = "deeppink3", "grey" = "grey40", "brown" = "chocolate4")
    })
    
    # 39. A function for drawing the interactive plot and downloading it
    plotInput <- function() {
        lab_els = c(rownames(selected_table()), colnames(selected_table()))
        leg_end = c(rep("construction", nrow(selected_table())), rep("dialect", 10))
        cx_dia = data.frame(lab_els, leg_end, rbind(ca_analysis()$row$coord[,1:2], ca_analysis()$col$coord[,1:2]))
        
        ggplot(data = data.frame(lab_els, leg_end, cx_dia),
               aes(x = Dim.1, y = Dim.2),
               label = lab_els) +
            theme_bw() +
            geom_hline(yintercept = 0, colour = "azure4") +
            geom_vline(xintercept = 0, colour = "azure4") +
            geom_text(aes(
                colour = leg_end,
                size = leg_end,
                label = lab_els))+
            scale_colour_manual(values = c(colorInput1(), colorInput2())) +
            scale_size_manual(values = c(5,6)) +
            labs(x = paste("1. dimension (", round(ca_analysis()$eig[1,2]), "%)"), y = paste("2. dimension (", round(ca_analysis()$eig[2,2]), "%)")) +
            ggtitle("Simple Correspondence Analysis") +
            theme(plot.title = element_text(face="italic", color="black", size=20)) +
            theme(axis.title.y = element_text(size = 15, angle = 90)) +
            theme(axis.title.x = element_text(size = 15, angle = 00)) +
            theme(legend.text = element_text(size = 15)) +
            theme(legend.position = "top") +
            theme(legend.title = element_blank())
    }
    
    # 41. The plot output
    output$plot <- renderPlot({
            plotInput()
    })
    
    # 42. Downloading the file (NB! might not work in RStudio viewer, should be used in browser view)
    output$download <- downloadHandler(
        filename = function() {paste("CA_", input$domain, ".", input$extension, sep="")},
        content = function(file) {
            ggsave(file, plot = plotInput(), device = input$extension, width = 19, height = 12, units = "in", dpi = 600)
        }
    )
    
})

################################
#### Running the application ####
################################

shinyApp(ui = ui, server = server)

