# clear variables and close windows
rm(list = ls(all = TRUE))
graphics.off()



library(Quandl)
library(dplyr)
library(readr)
library(quantmod)
library(xtable)


eth <- Quandl("BITFINEX/ETHUSD", api_key="-GNJxjPntak8s-AxpM5o")
ethts <- Quandl("BITFINEX/ETHUSD", api_key="-GNJxjPntak8s-AxpM5o", type = "xts")

#chartSeries(ethts, type = "candlesticks", show.grid = TRUE, name = "ETH Price w/ Volume")
#barChart(ethts,theme='white.mono',bar.type='hlc', name = "ETH Price w/ Volume")




btc <- Quandl("BITFINEX/BTCUSD", api_key="-GNJxjPntak8s-AxpM5o")
btcts <- Quandl("BITFINEX/ETHUSD", api_key="-GNJxjPntak8s-AxpM5o", type = "xts")

#chartSeries(btcts, type = "candlesticks", show.grid = TRUE, name = "BTC Price w/ Volume")
#barChart(btcts,theme='white.mono',bar.type='hlc', name = "BTC Price w/ Volume")






#chartSeries(ethts,TA="addVo();addBBands();addCCI();addDEMA();addZLEMA()")



eth %>%
  select(High, Low, Last, Volume) %>%
  summary(eth)

tbl = t(summary(eth))
s = print.xtable(xtable(tbl,digits=c(0,4,4,2,2,2,2)),hline.after=c(-1,-1,0,nrow(tbl),nrow(tbl)))
s = print.xtable(xtable(tbl,digits=4,hline.after=c(-1,-1,0,nrow(tbl),nrow(tbl))))
write(s,paste0('statistics_log_return_',ifelse(monthly,'monthly','daily'),'_latex.txt'))




btc %>%
  select(High, Low, Last, Volume) %>%
  summary(btc)



tbl1 = t(summary(btc))
s = print.xtable(xtable(tbl1,digits=c(0,4,4,2,2,2,2)),hline.after=c(-1,-1,0,nrow(tbl1),nrow(tbl1)))
s = print.xtable(xtable(tbl1,digits=4,hline.after=c(-1,-1,0,nrow(tbl1),nrow(tbl1))))
write(s,paste0('statistics_log_return_',ifelse(monthly,'monthly','daily'),'_latex.txt'))






###


library(ggplot2)
library(scales)


# Standard Plot
ggplot(eth, aes(x = eth$Date, y = eth$Last)) +
  labs(x = "Date", y = "Price") +
  geom_line() +
  scale_x_date(labels = date_format("%Y-%m-%d")) +
  theme_bw() + theme(panel.border = element_blank(), panel.grid.major = element_blank(),
                     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))


####



#!!!!!

library(quantmod)


portfolio = c("BTC-USD","ETH-USD","LTC-USD","XRP-USD","ADA-USD")

getSymbols(portfolio, src="yahoo", from="2017-01-01")

tail(`BTC-USD`)
tail(`ETH-USD`)


barChart(`ETH-USD`,theme='white.mono',bar.type='hlc')
chartSeries(`ETH-USD`,theme='white.mono', TA="addVo();addBBands();addCCI();addDEMA();addZLEMA()")


barChart(`BTC-USD`,theme='white.mono',bar.type='hlc')
chartSeries(`BTC-USD`,theme='white.mono', TA="addVo();addBBands();addCCI();addDEMA();addZLEMA()")




#####


# General File Preperation

# Reset Workspace
rm(list = ls(all = TRUE))

# Load Necessary Packages
libraries = c("jsonlite", "curl", "zoo")
lapply(libraries, function(x)
  if (!(x %in% installed.packages())) {
    install.packages(x)
  }
)
lapply(libraries, library, quietly = TRUE, character.only = TRUE)

#-------------------------------------------------------------------------------

# Graph CRIX - based on website

# Get Data
json_file <- "http://data.thecrix.de/data/crix.json"
crix <- fromJSON(json_file)
crix$date <- as.Date(crix$date)

# Regular Crix
plot(crix, type = "l", col = "steelblue", lwd = 3, xlab = "Date", ylab = "", cex.lab = 1.5, xaxt = "n")
axis.Date(1,at = seq(min(crix$date),max(crix$date),by = "6 mon"), format = "%m-%Y")
title(ylab = "Performance of CRIX", line = 2, cex.lab = 1.5)

# Log(Crix)
plot(crix$date, log(crix$price), type = "l", col = "steelblue", lwd = 2, xlab = "Date", ylab = "", cex.lab = 2, xaxt = "n")
axis.Date(1,at = seq(min(crix$date),max(crix$date),by = "6 mon"), format = "%m-%Y")
title(ylab = "Performance of log(CRIX)", line = 2, cex.lab = 2)

# Log Returns Crix
plot(crix$date[-1], diff(log(crix$price)), type = "l", col = "steelblue", lwd = 2, xlab = "Date", ylab = "", cex.lab = 1.5, xaxt = "n")
axis.Date(1,at = seq(min(crix$date),max(crix$date),by = "6 mon"), format = "%m-%Y")
title(ylab = "Log returns of CRIX", line = 2, cex.lab = 1.6)






#-------------------------------------------------------------------------------

### Alternative
# Graph CRIX - based on stored csv (not up-to-date)

# Get Data
crix <- read.csv("crixdata.csv", header=TRUE, sep=";")
crix$date = as.Date(crix$date)

# Regular Crix
plot(crix, type = "l", col = "steelblue", lwd = 2, xlab = "Date", ylab = "", cex.lab = 2, xaxt = "n")
axis.Date(1,at = seq(min(crix$date),max(crix$date),by = "6 mon"), format = "%m-%Y")
title(ylab = "Performance of CRIX", line = 2, cex.lab = 2)

# Log Log(Crix)
plot(crix$date, log(crix$price), type = "l", col = "steelblue", lwd = 2, xlab = "Date", ylab = "", cex.lab = 2, xaxt = "n")
axis.Date(1,at = seq(min(crix$date),max(crix$date),by = "6 mon"), format = "%m-%Y")
title(ylab = "Performance of log(CRIX)", line = 2, cex.lab = 2)






















# 
# 
# ####
# 
# 
# 
# 
# 
# 
# 
# library(coinmarketcapr)
# get_valid_currencies()
# get_global_marketcap()
# get_crypto_listings()
# plot_top_currencies()
# latest_marketcap <- get_global_marketcap('EUR')
# all_coins <- get_marketcap_ticker_all()
# 
# 
# 
# 
# library(coinmarketcapr)
# plot_top_currencies('USD',5)
# 
# 
# library(coinmarketcapr)
# #install.packages("treemap")
# library(treemap)
# 
# df <- get_marketcap_ticker_all()
# df1 <- na.omit(df[,c('id','market_cap_usd')])
# df1$market_cap_usd <- as.numeric(df1$market_cap_usd)
# df1$formatted_market_cap <-  paste0(df1$id,'\n','$',format(df1$market_cap_usd,big.mark = ',',scientific = F, trim = T))
# treemap(df1, index = 'formatted_market_cap', vSize = 'market_cap_usd', title = 'Cryptocurrency Market Cap', fontsize.labels=c(12, 8), palette='RdYlGn')
# 
# 
# 
# 
# 
# 
# 
# library(coinmarketcapr)
# plot_top_5_currencies()
# 
# 
# 
# 
# library(treemap)
# df1 <- na.omit(market_today[,c('id','market_cap_usd')])
# df1$market_cap_usd <- as.numeric(df1$market_cap_usd)
# df1$formatted_market_cap <-  paste0(df1$id,'\n','$',format(df1$market_cap_usd,big.mark = ',',scientific = F, trim = T))
# treemap(df1, index = 'formatted_market_cap', vSize = 'market_cap_usd', title = 'Cryptocurrency Market Cap', fontsize.labels=c(12, 8), palette='RdYlGn')
# 
# 
# 
# 
# ######
# 
# 
# 
# 
# 
# 
# 
# library(coinmarketcapr)
# library(jsonlite)
# library(ggplot2)
# library(curl)
# 
# 
# 
# 
# plot_top_5_currencies(currency = "USD", k = 5, bar_color = "grey")
# 
# plot_top_currencies(currency = "USD", k = 5, bar_color = "grey")
# 
# 
# 
# 
# plot_top_currencies('EUR')
# plot_top_currencies('GBP')
# 
# 
# 
# plot_top_currencies()
# get_marketcap_ticker_all()
# get_global_marketcap()
# 
# 
# library(tidyverse)
# market_today <- get_marketcap_ticker_all()
# market_today <- as_tibble(market_today)
# market_today <- market_today %>% mutate(
#   rank = as.numeric(rank), 
#   price_usd = as.numeric(price_usd),
#   price_btc = as.numeric(price_btc),
#   X24h_volume_usd = as.numeric(X24h_volume_usd),
#   market_cap_usd = as.numeric(market_cap_usd),
#   available_supply = as.numeric(available_supply),
#   total_supply = as.numeric(total_supply),
#   max_supply = as.numeric(max_supply),
#   percent_change_1h = as.numeric(percent_change_1h),
#   percent_change_24h = as.numeric(percent_change_24h),
#   percent_change_7d = as.numeric(percent_change_7d),
#   last_updated = as.numeric(last_updated)
# )
# market_today <- filter(market_today, rank <= 5)
# market_today
# 

