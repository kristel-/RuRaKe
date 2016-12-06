# This is an application for combining the data from Andrus Saareste's Small Atlas of Estonian Dialects (1955) with the data from Estonian Dialect Corpus.
# This is illustrated with 3 alternating phenomena: sui vs suvi ('summer'), suurem vs suuremb ('bigger'), and ei ole vs pole ('is not').
# One of the input files is a frequency table ("koondfreqdata.csv") in UTF-8 encoding and with the following structure: Parish_id;ei_ole;pole;sui;suvi;suurem;suuremb;Dialect_en. 
# Excerpts of Kristel Uiboaed's scripts have been used for plotting linguistic data using shapefiles and ggplot.

# 1. Load all the necessary packages (if the packages are not yet installed, so so using install.packages("packagename"))
library(shiny)
library(rgdal)
library(rgeos)
library(maptools)
library(ggplot2)
library(plyr)
library(dplyr)
library(Hmisc)
library(gridExtra)

# 2. Read in data and convert the projections of atlas data
freqdata = read.csv("koondandmed.csv", encoding = "UTF-8", sep=";") # Frequency data table
# The atlas data and the map for Estonian parishes are in the form of shapefiles. The folders containing the shapefiles are in the working directory. The CRS has to be converted for further processing.
atlasSuvi_sui = spTransform(readOGR("./suvi", "suvi"), CRS("+proj=longlat +datum=NAD83")) # Atlas data
atlasSuurem_suuremb = spTransform(readOGR("./suurem", "komp_suurem_uus"), CRS("+proj=longlat +datum=NAD83")) # Atlas data
atlasEiole_pole = spTransform(readOGR("./ML", "ei_ole_windows-1257", encoding = "UTF-8"), CRS("+proj=longlat +datum=NAD83")) # Atlas data
estParish <- spTransform(readOGR("./estParishDialects", "estParishDialects"), CRS("+proj=longlat +datum=NAD83")) # Parish map shapefile

#####################################
##### 3. Dialect map attributes #####
#####################################
# First, create a dialect data frame from the shapefile (this is necessary for plotting with ggplot)
dialect.df <- fortify(estParish, region="Dialect_en"); names(dialect.df)[names(dialect.df)=="id"] <- "Dialect_en"
# Join all rows (parishes) with the same value in the "Dialect_en" column into one polygon
dialects <- gUnaryUnion(estParish, id = estParish$Dialect_en)

####################################
##### 4. Parish map attributes #####
####################################
# Create a parish data frame
parish.df <- fortify(estParish, region="Parish_id"); names(parish.df)[names(parish.df)=="id"] <- "Parish_id"

########################
##### 5. Map Theme #####
########################
# Create a theme for plotting
mapAxisTheme <- theme(panel.grid.major = element_blank(),
                      panel.grid.minor = element_blank(),
                      axis.ticks = element_blank(),
                      axis.text.x = element_blank(),
                      axis.text.y = element_blank())

####################################
##### 6. Corpus frequency data #####
####################################
# Read in the frequency data for the Estonian Dialect Corpus (contain frequencies for annotated tokens per dialect), necessary for normalization
norm_dialect = read.csv2("norm_dialect.csv", fileEncoding = "UTF-8"); norm_dialect = norm_dialect[order(norm_dialect$Dialect_en),]
# Read in the frequency data for the Estonian Dialect Corpus (contain frequencies for annotated tokens per parish), necessary for normalization
norm_parish = read.csv2("norm_parish.csv", fileEncoding = "UTF-8")

##########################################################

############
#### UI ####
############

ui <- shinyUI(fluidPage(
    
    # 7. Title of the application
    titlePanel("Combining atlas data with corpus frequency data"),
    
    # 8. Introduction
    p("This is an application that combines data from Andrus Saareste's dialect maps with corresponding data from the Corpus of Estonian Dialects. The corpus frequencies are normalized and can be generalized to either parishes or dialects. The atlas data can be displayed either by symbols or text. Generating the map for the first time may take a few seconds."),
    
    # 9. The rest of the UI in two sections: one contains the specs for the input (in three columns in the top of the page), the other for the output (2 maps on the rest of the page).
    fluidRow(
        
        # 10. Selection of user input categories
        column(4,
               
               # 11. Selection of the cetegory (suvi/sui, suurem/suuremb, ei ole/pole)
               selectInput("category", label="Category:", choices=c("suvi/sui", "suurem/suuremb", "ei ole/pole"), selected="suvi/sui"),
               
               # 12. Selection of the level of generalization
               selectInput("level", label="Level:", choices=c("Parishes", "Dialects"), selected="Parishes"),
               
               # 13. Update button
               actionButton("update", label="Update")),
        
        column(4,
               
               # 14. Map colour selection
               selectInput("colours", label = "Colour of the map:", choices = c("green", "blue", "red", "orange", "yellow", "purple", "pink", "grey", "brown"), selected = "green"),
               
               # 15. Selection of the display element
               selectInput("element", label="Display symbols or text:", choices=c("Symbols", "Text"), selected="Text")),
        
        column(4,
               
               # 16. Selection of the file extension for downloading
               radioButtons("extension", label = "File extension for downloading:", choices = c("png", "tiff", "pdf"), selected = "png"),
               
               # 17. Download button
               downloadButton("download", label = "Download")),
        
        # 18. output plots
        plotOutput("plot", height="800px")
        )
    )
)

################
#### Server ####
################

server <- shinyServer(function(input, output) {
    
    # 19. Create a reactive input table for one of the parallel forms from corpus frequency data
    selected_table1 <- reactive({
        
        # 20. Change the input table only when the "update" button is pressed
        input$update
        
        isolate({
            withProgress({
                setProgress(message="Loading")
                
                # 21. If the user has specified 'Parishes' as the level of generalization...
                if(input$level == "Parishes"){
                    
                    # 22. and 'suvi/sui' as the preferred construction to be displayed...
                    if(input$category=="suvi/sui"){
                        
                        # 23. choose only the column containing parishes and the column named 'suvi' from the original data frame
                        cat1 <- droplevels(freqdata[,c(1,5)]); names(cat1) = c("Parish_id", "Freq_PAR")
                    }
                    
                    # 24. or 'suurem/suuremb' as the preferred construction to be displayed...
                    else if(input$category=="suurem/suuremb"){
                        
                        # 25. choose only the column containing parishes and the column named 'suurem' from the original data frame
                        cat1 <- droplevels(freqdata[,c(1,6)]); names(cat1) = c("Parish_id", "Freq_PAR")
                        }
                    
                    # 26. or 'ei ole/pole' as the preferred construction to be displayed...
                    else{
                        
                        # 27. choose only the column containing parishes and the column named 'ei_ole' from the original data frame
                        cat1 <- droplevels(freqdata[,c(1,2)]); names(cat1) = c("Parish_id", "Freq_PAR")
                    }
                    
                    # 28. Normalize the parish frequencies by the mean token frequencies in the corpus
                    cat1$Freq_norm = suppressWarnings(round(cat1$Freq_PAR*mean(norm_parish[norm_parish$Parish_id %in% cat1$Parish_id,]$Freq)/norm_parish[norm_parish$Parish_id %in% cat1$Parish_id,]$Freq))
                    
                    # 29. Merge the frequency data with the data slot in the parish shapefile (by 'Parish_id')
                    estParishesData1 <- merge(estParish@data, cat1, by = "Parish_id", all.x = T, all.y = T, sort = F)
                    
                    # 30. Set corpus frequencies for only those parishes that are present both in the corpus and in the atlas data. Those not present in the corpus data get a frequency of 0.
                    estParishesData1 <- estParishesData1 %>% mutate(Freq_norm = ifelse(is.na(Freq_norm), 0, Freq_norm))
                    
                    # 31. Join the corpus+data slot data frame with parish data frame containing the coordinates (by 'Parish_id')
                    estParishesData1DF <- arrange(join(estParishesData1, parish.df, "Parish_id"), order)
                }
                
                # 32. If the user has specified 'Dialects' as the level of generalization...
                else if (input$level=="Dialects"){
                    
                    # 33. and 'suvi/sui' as the preferred construction to be displayed...
                    if(input$category=="suvi/sui"){
                        
                        # 34. choose only the column containing dialects and the column named 'suvi' from the original data frame
                        cat1 <- droplevels(freqdata[,c(8,5)])
                    }
                    
                    # 35. or 'suurem/suuremb' as the preferred construction to be displayed...
                    else if(input$category=="suurem/suuremb"){
                        
                        # 36. choose only the column containing dialects and the column named 'suurem' from the original data frame
                        cat1 <- droplevels(freqdata[,c(8,6)])
                    }
                    
                    # 37. or 'ei ole/pole' as the preferred construction to be displayed...
                    else{
                        
                        # 38. choose only the column containing dialects and the column named 'ei_ole' from the original data frame
                        cat1 <- droplevels(freqdata[,c(8,2)])
                    }
                    
                    # 39. Sum the construction frequencies for each dialect
                    cat1 <- aggregate(cat1[,2] ~ cat1[,1], cat1, sum); names(cat1) = c("Dialect_en", "Freq_DIA")
                    
                    # 40. Normalize the dialect frequencies by the mean token frequencies in the corpus
                    cat1$Freq_norm <- suppressWarnings(round(cat1$Freq_DIA*mean(norm_dialect[norm_dialect$Dialect_en %in% cat1$Dialect_en,]$Freq)/norm_dialect[norm_dialect$Dialect_en %in% cat1$Dialect_en,]$Freq))
                    
                    # 41. Merge the frequency data with the data slot in the parish shapefile (by 'Dialect_en')
                    estParishesData1 <- merge(estParish@data, cat1, by = "Dialect_en", all.x = T, all.y = T, sort = F)
                    
                    # 42. Set corpus frequencies for only those dialects that are present both in the corpus and in the atlas data. Those not present in the corpus data get a frequency of 0.
                    estParishesData1 <- estParishesData1 %>% mutate(Freq_norm = ifelse(is.na(Freq_norm), 0, Freq_norm))
                    
                    # 43. Join the corpus+data slot data frame with parish data frame containing the coordinates (by 'Parish_id')
                    estParishesData1DF <- arrange(join(estParishesData1, dialect.df, "Dialect_en"), order)
                    }
                })
            })
        })
    
    # 44. Create a reactive input table for the other parallel form from corpus frequency data
    selected_table2 <- reactive({
        
        # 45. Repeat steps 20-43 for the other parallel forms
        
        input$update
        isolate({
            withProgress({
                setProgress(message="Loading")
                if(input$level == "Parishes"){
                    if(input$category=="suvi/sui"){
                        cat2 <- droplevels(freqdata[,c(1,4)]); names(cat2) = c("Parish_id", "Freq_PAR")
                    }
                    else if(input$category=="suurem/suuremb"){
                        cat2 <- droplevels(freqdata[,c(1,7)]); names(cat2) = c("Parish_id", "Freq_PAR")
                    }
                    else{
                        cat2 <- droplevels(freqdata[,c(1,3)]); names(cat2) = c("Parish_id", "Freq_PAR")
                    }
                    cat2$Freq_norm = suppressWarnings(round(cat2$Freq_PAR*mean(norm_parish[norm_parish$Parish_id %in% cat2$Parish_id,]$Freq)/norm_parish[norm_parish$Parish_id %in% cat2$Parish_id,]$Freq))
                    estParishesData2 <- merge(estParish@data, cat2, by = "Parish_id", all.x = T, all.y = T, sort = F)
                    estParishesData2 <- estParishesData2 %>% mutate(Freq_norm = ifelse(is.na(Freq_norm), 0, Freq_norm))
                    estParishesData2DF <- arrange(join(estParishesData2, parish.df, "Parish_id"), order)
                }
                else{
                    if(input$category=="suvi/sui"){
                        cat2 <- droplevels(freqdata[,c(8,4)])
                    }
                    else if(input$category=="suurem/suuremb"){
                        cat2 <- droplevels(freqdata[,c(8,7)])
                    }
                    else{
                        cat2 <- droplevels(freqdata[,c(8,3)])
                    }
                    cat2 <- aggregate(cat2[,2] ~ cat2[,1], cat2, sum); names(cat2) = c("Dialect_en", "Freq_DIA")
                    cat2$Freq_norm <- suppressWarnings(round(cat2$Freq_DIA*mean(norm_dialect[norm_dialect$Dialect_en %in% cat2$Dialect_en,]$Freq)/norm_dialect[norm_dialect$Dialect_en %in% cat2$Dialect_en,]$Freq))
                    estParishesData2 <- merge(estParish@data, cat2, by = "Dialect_en", all.x = T, all.y = T, sort = F)
                    estParishesData2 <- estParishesData2 %>% mutate(Freq_norm = ifelse(is.na(Freq_norm), 0, Freq_norm))
                    estParishesData2DF <- arrange(join(estParishesData2, dialect.df, "Dialect_en"), order)
                    }
                })
            })
        })
    
    # 46. Reactive function which chooses the right atlas data based on the user's choice
    atlas <- reactive({
        
        input$update
        isolate({
            withProgress({
                if(input$category=="suvi/sui"){
                    atlasData = atlasSuvi_sui
                    }
                else if(input$category=="suurem/suuremb"){
                    atlasData = atlasSuurem_suuremb
                    }
                else{
                    atlasData = atlasEiole_pole
                }
                atlasData = droplevels(as.data.frame(atlasData)[!is.na(as.data.frame(atlasData)$Keelend),])
                })
            })
        })
    
    # 47. Reactive function which chooses either text or symbols for plotting, based on the user's choice
    symbols_text <- reactive({
        if(input$element=="Symbols"){
            
            # 48. symbols
            geom_point(data = atlas(), aes(shape = Keelend, x = coords.x1, y = coords.x2), size = 4, inherit.aes = F)
        }
        else{
            
            # 49. text
            geom_text(data = atlas(), aes(label = Keelend, x = coords.x1, y = coords.x2, size = 0.5), show.legend=F, inherit.aes = F)
        }
    })
    
    # 50. Reactive function which chooses the colour for plotting the corpus frequency data
    colours <- reactive({
        colour <- switch(input$colours, "green" = "forestgreen", "blue" = "dodgerblue3", "red" = "firebrick3", "yellow" = "goldenrod2", "orange" = "darkorange3", "purple" = "darkorchid4", "pink" = "deeppink3", "grey" = "grey40", "brown" = "chocolate4")
    })
    
    # 51. Reactive function which chooses the title for the first plot
    title1 <- reactive({
        
        input$update
        isolate({
            withProgress({
                if(input$category=="suvi/sui"){
                    title = "suvi"
                }
                else if(input$category=="suurem/suuremb"){
                    title = "suurem"
                }
                else{
                    title = "ei ole"
                }
                })
            })
        })
    
    # 52. Reactive function which chooses the title for the second plot
    title2 <- reactive({
        
        input$update
        isolate({
            withProgress({
                if(input$category=="suvi/sui"){
                    title = "sui"
                }
                else if(input$category=="suurem/suuremb"){
                    title = "suuremb"
                }
                else{
                    title = "pole"
                }
            })
        })
    })
    
    # 53. Plotting function for the two maps
    plotInput <- function() {
        category1 <- ggplot(data=selected_table1(), aes(x=long, y=lat, fill=Freq_norm, group = group)) +
            geom_polygon(colour="black") +
            scale_fill_gradient(low="white", high=colours()) +
            labs(x="", y="") +
            theme_bw() +
            mapAxisTheme +
            theme(legend.text=element_text(size=18), legend.title = element_text(size=15, face="bold")) +
            symbols_text() +
            scale_shape_manual(values=seq(0,18)) +
            ggtitle(title1()) +
            guides(fill = F)
        
        category2 <- ggplot(data=selected_table2(), aes(x=long, y=lat, fill=Freq_norm, group=group)) +
            geom_polygon(colour="black") +
            scale_fill_gradient(low="white", high=colours()) +
            labs(x="", y="") +
            theme_bw() +
            mapAxisTheme +
            theme(legend.text=element_text(size=18), legend.title = element_text(size=15, face="bold")) +
            symbols_text() +
            scale_shape_manual(values=seq(0,18)) +
            ggtitle(title2()) +
            guides(fill=F)
        
        grid.arrange(category1, category2, ncol=2)
    }
    
    # 54. Plot output, using the plotting function
    output$plot <- renderPlot({
        plotInput()
    })
    
    # 55. Download function
    output$download <- downloadHandler(
        filename = function() {paste(input$category, ".", input$extension, sep="")},
                content = function(file) {
                    ggsave(file, plot = plotInput(), device = input$extension, width = 19, height = 12, units = "in", dpi = 600)
                }
            )
})

########################################
#### Run the application ####
shinyApp(ui = ui, server = server)