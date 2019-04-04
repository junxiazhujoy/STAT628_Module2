library(shiny)
ui <- fluidPage(
  titlePanel("Get suggestion for you business"),
  h5("Enter business id and choose words to get the corresponding summary and suggestion."),
  sidebarPanel(
    numericInput("business_id",label="business_id",value=130241),
    selectInput("words","words",c('beer','beer select','draft beer','craft beer','cocktail')),
    submitButton("Update")
  ),
  mainPanel(
    tabsetPanel(
      tabPanel("Summary",
               h4(textOutput("rating")),
               h4(textOutput("noword")),
               h4(plotOutput('pie')),
               h4(textOutput('average'))
      ),
      tabPanel("Detail",
               h5("This page shows the top 5 high frequency adjective words."),
               h4(textOutput("positive")),
               h4(textOutput("negative"))
      ),
      tabPanel("Suggestion",
               h4(textOutput("suggestion"))
      )
  )))

server <- function(input, output) {
  #summary
  rate<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      index=which(dat$business_id==id)
      cat("average rating:",round(dat[index,'stars'],2))
    }else cat("business_id is not in the list!")
  })
  output$rating<-renderPrint({
    rate()
  })
  
  pieplot<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      pos_count=dat[index,'pos_count']
      neg_count=dat[index,'neg_count']
      counts=c(pos_count,neg_count)
      label <-c("positive", "negative")
      if(sum(counts)!=0){
        piepercent<-round(100*counts/sum(counts), 1)
        piepercent<-paste(piepercent, "%", sep = "")
        pie(counts,labels=piepercent, main="Percentage of positive and negative words",col=c("skyblue1", "skyblue4"))
        legend("topright",label, cex=, fill=c("skyblue1", "skyblue4"))
      }
    }
  })
  output$pie<-renderPlot({
    pieplot()
  })
  
  ave<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    neg_ave=round(100*sum(dat[,'neg_count'])/sum(dat[,'all_mention']),1)
    pos_ave=round(100*sum(dat[,'pos_count'])/sum(dat[,'all_mention']),1)
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      pos_count=dat[index,'pos_count']
      neg_count=dat[index,'neg_count']
      counts=c(pos_count,neg_count)
      if(sum(counts)!=0){
        piepercent<-round(100*counts/sum(counts), 1)
        if(piepercent[1]>pos_ave){
          cat("The ",words," in this business is above average(",pos_ave,"%).",sep="")
        }else if(piepercent[1]<pos_ave){
          cat("The ",words," in this business is below average(",pos_ave,"%).",sep="")
        }else cat("The ",words," in this business is at the average level(",pos_ave,"%).",sep="")
      }
    }
  })
  output$average<-renderPrint({
    ave()
  })
  
  noword<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    neg_ave=round(100*sum(dat[,'neg_count'])/sum(dat[,'all_mention']),1)
    pos_ave=round(100*sum(dat[,'pos_count'])/sum(dat[,'all_mention']),1)
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      pos_count=dat[index,'pos_count']
      neg_count=dat[index,'neg_count']
      counts=c(pos_count,neg_count)
      if(sum(counts)==0)  cat("There is no corresponding adjective words near",words)
    }
  })
  output$noword<-renderPrint({
    noword()
  })
  #detail
  pos<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      #as.character(dat[index,'pos_top5'])
      topwords=sub(pattern="\\[(.*)\\]"   , replacement="\\1", x=as.character(dat[index,'pos_top5']))
      topwords=unlist(strsplit(x=topwords, split=",|'| "))
      topwords=topwords[nchar(topwords)!=0]
      if(length(topwords)>0){
        #for(i in 1:length(topwords)){
        #  cat(topwords[i],"\n\n",sep="")
        #}
        #data.frame('positive'=topwords)
        cat("positive words: ")
        cat(topwords,sep=", ")
      }else cat("positive words: no words")
    }else cat("business_id is not in the list!")
  })
  output$positive<-renderPrint({
    pos()
  })
  
  neg<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      #as.character(dat[index,'neg_top5'])
      topwords=sub(pattern="\\[(.*)\\]"   , replacement="\\1", x=as.character(dat[index,'neg_top5']))
      topwords=unlist(strsplit(x=topwords, split=",|'| "))
      topwords=topwords[nchar(topwords)!=0]
      if(length(topwords)>0){
        cat("negative words: ")
        cat(topwords,sep=", ")
      }else cat("negative words: no words")
    }
  })
  output$negative<-renderPrint({
    neg()
  })
  #suggestion
  sugg<-reactive({
    words=input$words
    if(words=='beer')  dat=read.csv("beer_adj.csv")
    else if(words=='beer select') dat=read.csv("select_adj.csv")
    else if(words=='craft beer') dat=read.csv("craft_adj.csv")
    else if(words=='draft beer') dat=read.csv("draft_adj.csv")
    else if(words=='cocktail') dat=read.csv("cocktail_adj.csv")
    
    neg_ave=round(100*sum(dat[,'neg_count'])/sum(dat[,'all_mention']),1)
    pos_ave=round(100*sum(dat[,'pos_count'])/sum(dat[,'all_mention']),1)
    
    id=input$business_id
    index=which(dat$business_id==id)
    if(length(index)!=0){
      pos_count=dat[index,'pos_count']
      neg_count=dat[index,'neg_count']
      counts=c(pos_count,neg_count)
      if(sum(counts)!=0){
        piepercent<-round(100*counts/sum(counts), 1)
        if(piepercent[1]>pos_ave){
          cat("The",words,"in this business has good reivews. Just keep doing that!")
        }else {
          cat("The",words,"in this business is not good.")
          cat("You need to improve the level of",words,"!")
        }
      }else cat("There are no words can be used to give suggestion.")
    }else cat("business_id is not in the list!")
  })
  output$suggestion<-renderPrint({
    sugg()
  })
}
  
shinyApp(ui=ui,server=server)
