# This is an application for combining the data from Andrus Saareste's Small Atlas of Estonian Dialects (1955) with the data from Estonian Dialect Corpus.
# This is illustrated with 3 alternating phenomena: sui vs suvi ('summer'), suurem vs suuremb ('bigger'), and ei ole vs pole ('is not').
# One of the input files is a frequency table ("koondfreqdata.csv") in UTF-8 encoding and with the following structure: Parish_id;ei_ole;pole;sui;suvi;suurem;suuremb;Dialect_en. 

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
atlasSuvi_sui = spTransform(readOGR("./suvi", "suvi"), CRS("+proj=longlat +datum=NAD83")) # Atlas data
atlasSuurem_suuremb = spTransform(readOGR("./suurem", "komp_suurem_uus"), CRS("+proj=longlat +datum=NAD83")) # Atlas data
atlasEiole_pole = spTransform(readOGR("./ei_ole", "ei_ole_windows-1257", encoding = "UTF-8"), CRS("+proj=longlat +datum=NAD83")) # Atlas data
estParish <- spTransform(readOGR("./estParishDialects", "estParishDialects"), CRS("+proj=longlat +datum=NAD83")) # Parish map shapefile


#####################################
##### 3. Dialect map attributes #####
#####################################
dialect.df <- fortify(estParish, region="Dialect_en"); names(dialect.df)[names(dialect.df)=="id"] <- "Dialect_en"
dialects <- gUnaryUnion(estParish, id = estParish$Dialect_en)
centroidsDial <- as.data.frame(coordinates(dialects)); names(centroidsDial) <- c("Longitude", "Latitude"); centroidsDial$Dialect <- rownames(centroidsDial)

####################################
##### 4. Parish map attributes #####
####################################
parish.df <- fortify(estParish, region="Parish_id"); names(parish.df)[names(parish.df)=="id"] <- "Parish_id"
idListPar <- estParish@data$Parish_id
centroidsPar <- as.data.frame(coordinates(estParish)); names(centroidsPar) <- c("Longitude", "Latitude")
centrPar.id <- data.frame(id=idListPar, centroidsPar)
parWithCentr <- merge(parish.df, centrPar.id, by.x="Parish_id", by.y="id")

########################
##### 5. Map Theme #####
########################
mapAxisTheme <- theme(panel.grid.major = element_blank(),
                      panel.grid.minor = element_blank(),
                      axis.ticks = element_blank(),
                      axis.text.x = element_blank(),
                      axis.text.y = element_blank())

#################################
##### Corpus frequency data #####
#################################
norm_dialect = read.csv2("norm_dialect.csv", fileEncoding = "UTF-8"); norm_dialect = norm_dialect[order(norm_dialect$Dialect_en),]
norm_parish = read.csv2("norm_parish.csv", fileEncoding = "UTF-8")

##########################################################

ui <- shinyUI(fluidPage(
    titlePanel("Combining atlas data with corpus frequency data"),
    p("This is an application that combines data from Andrus Saareste's dialect maps with corresponding data from the Corpus of Estonian Dialects. The corpus frequencies are normalized and can be generalized to either parishes or dialects. The atlas data can be displayed either by symbols or text. Generating the map for the first time may take a few seconds."),
    fluidRow(
        column(4,
               selectInput("category", label="Category:", choices=c("suvi/sui", "suurem/suuremb", "ei ole/pole"), selected="suvi/sui"),
               selectInput("level", label="Level:", choices=c("Parishes", "Dialects"), selected="Parishes"),
               actionButton("update", label="Update")),
        column(4,
               selectInput("colours", label = "Colour of the map:", choices = c("green", "blue", "red", "orange", "yellow", "purple", "pink", "grey", "brown"), selected = "green"),
               selectInput("element", label="Display symbols or text:", choices=c("Symbols", "Text"), selected="Text")),
        column(4,
               radioButtons("extension", label = "File extension for downloading:", choices = c("png", "tiff", "pdf"), selected = "png"),
               downloadButton("download", label = "Download")),
    
    plotOutput("plot", height="800px")
    )
    )
)

server <- shinyServer(function(input, output) {
    
    selected_table1 <- reactive({
        
        input$update
        isolate({
            withProgress({
                setProgress(message="Loading")
                if(input$level == "Parishes"){
                    if(input$category=="suvi/sui"){
                        cat1 <- droplevels(freqdata[,c(1,5)]); names(cat1) = c("Parish_id", "Freq_PAR")
                        }
                    else if(input$category=="suurem/suuremb"){
                        cat1 <- droplevels(freqdata[,c(1,6)]); names(cat1) = c("Parish_id", "Freq_PAR")
                        }
                    else{
                        cat1 <- droplevels(freqdata[,c(1,2)]); names(cat1) = c("Parish_id", "Freq_PAR")
                    }
                    cat1$Freq_norm = suppressWarnings(round(cat1$Freq_PAR*mean(norm_parish[norm_parish$Parish_id %in% cat1$Parish_id,]$Freq)/norm_parish[norm_parish$Parish_id %in% cat1$Parish_id,]$Freq))
                    estParishesData1 <- merge(estParish@data, cat1, by = "Parish_id", all.x = T, all.y = T, sort = F)
                    estParishesData1 <- estParishesData1 %>% mutate(Freq_norm = ifelse(is.na(Freq_norm), 0, Freq_norm))
                    estParishesData1DF <- arrange(join(estParishesData1, parish.df, "Parish_id"), order)
                }
                else if (input$level=="Dialects"){
                    
                    if(input$category=="suvi/sui"){
                        cat1 <- droplevels(freqdata[,c(8,5)])
                    }
                    else if(input$category=="suurem/suuremb"){
                        cat1 <- droplevels(freqdata[,c(8,6)])
                    }
                    else{
                        cat1 <- droplevels(freqdata[,c(8,2)])
                    }
                    cat1 <- aggregate(cat1[,2] ~ cat1[,1], cat1, sum); names(cat1) = c("Dialect_en", "Freq_DIA")
                    cat1$Freq_norm <- suppressWarnings(round(cat1$Freq_DIA*mean(norm_dialect[norm_dialect$Dialect_en %in% cat1$Dialect_en,]$Freq)/norm_dialect[norm_dialect$Dialect_en %in% cat1$Dialect_en,]$Freq))
                    estParishesData1 <- merge(estParish@data, cat1, by = "Dialect_en", all.x = T, all.y = T, sort = F)
                    estParishesData1 <- estParishesData1 %>% mutate(Freq_norm = ifelse(is.na(Freq_norm), 0, Freq_norm))
                    estParishesData1DF <- arrange(join(estParishesData1, dialect.df, "Dialect_en"), order)
                }
                })
            })
        })
    
    selected_table2 <- reactive({
        
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
    
    symbols_text <- reactive({
        if(input$element=="Symbols"){
            geom_point(data = atlas(), aes(shape = Keelend, x = coords.x1, y = coords.x2), size = 4, inherit.aes = F)
        }
        else{
            geom_text(data = atlas(), aes(label = Keelend, x = coords.x1, y = coords.x2, size = 0.5), show.legend=F, inherit.aes = F)
        }
    })
    
    colours <- reactive({
        colour <- switch(input$colours, "green" = "forestgreen", "blue" = "dodgerblue3", "red" = "firebrick3", "yellow" = "goldenrod2", "orange" = "darkorange3", "purple" = "darkorchid4", "pink" = "deeppink3", "grey" = "grey40", "brown" = "chocolate4")
    })
    
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
    
    output$plot <- renderPlot({
        plotInput()
    })
    
    output$download <- downloadHandler(
        filename = function() {paste(input$category, ".", input$extension, sep="")},
                content = function(file) {
                    ggsave(file, plot = plotInput(), device = input$extension, width = 19, height = 12, units = "in", dpi = 600)
                }
            )
})

shinyApp(ui = ui, server = server)