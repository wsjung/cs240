################################
# TIME SERIES ANALYSIS         #
################################

fround <- function(x,places=0) {
  return (format(round(x, digits=places), nsmall=places))
}
################################

#time series packages
library("tseries")
library("forecast")
merged <- NULL

iterations <- 10

for(j in 1:iterations){

#loading in the data
BCHini <- read.csv("BCH-USD_10_2_18.csv")
BTCini <- read.csv("BTC-USD_10_2_18.csv")
EOSini <- read.csv("EOS-USD_10_2_18.csv")
ETHini <- read.csv("ETH-USD_10_2_18.csv")
XRPini <- read.csv("XRP-USD_10_2_18.csv")

BCH <- BCHini[(nrow(BCHini)-399):(nrow(BCHini)-iterations+j),]
BTC <- BTCini[(nrow(BTCini)-399):(nrow(BTCini)-iterations+j),]
EOS <- EOSini[(nrow(EOSini)-399):(nrow(EOSini)-iterations+j),]
ETH <- ETHini[(nrow(ETHini)-399):(nrow(ETHini)-iterations+j),]
XRP <- XRPini[(nrow(XRPini)-399):(nrow(XRPini)-iterations+j),]

#formatting column names
names(BCH) <- c("date","open","high","low","close","adjclose","volume")
names(BTC) <- c("date","open","high","low","close","adjclose","volume")
names(EOS) <- c("date","open","high","low","close","adjclose","volume")
names(ETH) <- c("date","open","high","low","close","adjclose","volume")
names(XRP) <- c("date","open","high","low","close","adjclose","volume")

#creating time series
BCHTS <- ts(BCH$adjclose)
BTCTS <- ts(BTC$adjclose)
EOSTS <- ts(EOS$adjclose)
ETHTS <- ts(ETH$adjclose)
XRPTS <- ts(XRP$adjclose)

#recording number of entries in time series
BCHEntries <- length(BCHTS)
BTCEntries <- length(BTCTS)
EOSEntries <- length(EOSTS)
ETHEntries <- length(ETHTS)
XRPEntries <- length(XRPTS)

#we assume none of the time series are going to be stationary, so lets take the differences
BCHDiff <- diff(BCHTS, differences = 1)
BCHDiffNum <- 1
BTCDiff <- diff(BTCTS, differences = 1)
BTCDiffNum <- 1
EOSDiff <- diff(EOSTS, differences = 1)
EOSDiffNum <- 1
ETHDiff <- diff(ETHTS, differences = 1)
ETHDiffNum <- 1
XRPDiff <- diff(XRPTS, differences = 1)
XRPDiffNum <- 1

#checking for stationary condition using ADF test
#adjusting differences if necessary
if(adf.test(BCHDiff)["p.value"] > 0.05){
  BCHDiff <- diff(BCHTS, differences = 2)
  BCHDiffNum <- 2
}
if(adf.test(BTCDiff)["p.value"] > 0.05){
  BTCDiff <- diff(BTCTS, differences = 2)
  BTCDiffNum <- 2
}
if(adf.test(EOSDiff)["p.value"] > 0.05){
  EOSDiff <- diff(EOSTS, differences = 2)
  EOSDiffNum <- 2
}
if(adf.test(ETHDiff)["p.value"] > 0.05){
  ETHDiff <- diff(ETHTS, differences = 2)
  ETHDiffNum <- 2
}
if(adf.test(XRPDiff)["p.value"] > 0.05){
  XRPDiff <- diff(XRPTS, differences = 2)
  XRPDiffNum <- 2
}

#setting default lagged values to 1
BCHP <- 1
BTCP <- 1
EOSP <- 1
ETHP <- 1
XRPP <- 1

#setting default lagged errors to 1
BCHQ <- 1
BTCQ <- 1
EOSQ <- 1
ETHQ <- 1
XRPQ <- 1

#conducting PACF AND ACF tests to determine the model selection
BCHPACF <- pacf(BCHDiff)$acf
BTCPACF <- pacf(BTCDiff)$acf
EOSPACF <- pacf(EOSDiff)$acf
ETHPACF <- pacf(ETHDiff)$acf
XRPPACF <- pacf(XRPDiff)$acf

BCHACF <- acf(BCHDiff)$acf
BTCACF <- acf(BTCDiff)$acf
EOSACF <- acf(EOSDiff)$acf
ETHACF <- acf(ETHDiff)$acf
XRPACF <- acf(XRPDiff)$acf

#calculating individual confidence intervals
BCHInt <- qnorm(c(0.025, 0.975))/sqrt(pacf(BCHDiff)$n.used)
BTCInt <- qnorm(c(0.025, 0.975))/sqrt(pacf(BTCDiff)$n.used)
EOSInt <- qnorm(c(0.025, 0.975))/sqrt(pacf(EOSDiff)$n.used)
ETHInt <- qnorm(c(0.025, 0.975))/sqrt(pacf(ETHDiff)$n.used)
XRPInt <- qnorm(c(0.025, 0.975))/sqrt(pacf(XRPDiff)$n.used)

#time to decide on our ARIMA model!
for(i in 2:15){
  #finding P and Q for BCH
  if(BCHPACF[i] < BCHInt[1] | BCHPACF[i] > BCHInt[2]){
    BCHP <- i
  }
  if(BCHACF[i] < BCHInt[1] | BCHACF[i] > BCHInt[2]){
    BCHQ <- i
  }
  
  #finding P and Q for BTC
  if(BTCPACF[i] < BTCInt[1] | BTCPACF[i] > BTCInt[2]){
    BTCP <- i
  }
  if(BTCACF[i] < BTCInt[1] | BTCACF[i] > BTCInt[2]){
    BTCQ <- i
  }
  
  #finding P and Q for EOS
  if(EOSPACF[i] < EOSInt[1] | EOSPACF[i] > EOSInt[2]){
    EOSP <- i
  }
  if(EOSACF[i] < EOSInt[1] | EOSACF[i] > EOSInt[2]){
    EOSQ <- i
  }
  
  #finding P and Q for ETH
  if(ETHPACF[i] < ETHInt[1] | ETHPACF[i] > ETHInt[2]){
    ETHP <- i
  }
  if(ETHACF[i] < ETHInt[1] | ETHACF[i] > ETHInt[2]){
    ETHQ <- i
  }
  
  #finding P and Q for XRP
  if(XRPPACF[i] < XRPInt[1] | XRPPACF[i] > XRPInt[2]){
    XRPP <- i
  }
  if(XRPACF[i] < XRPInt[1] | XRPACF[i] > XRPInt[2]){
    XRPQ <- i
  }
}

#creating our ARIMA models
BCHModel <- arima(BCHTS, order = c(BCHP, BCHDiffNum, BCHQ))
BTCModel <- arima(BTCTS, order = c(BTCP, BTCDiffNum, BTCQ))
EOSModel <- arima(EOSTS, order = c(EOSP, EOSDiffNum, EOSQ))
ETHModel <- arima(ETHTS, order = c(ETHP, ETHDiffNum, ETHQ))
XRPModel <- arima(XRPTS, order = c(XRPP, XRPDiffNum, XRPQ))

#calculating forecasts
BCHFcast <- forecast(BCHModel, h = 5)
BTCFcast <- forecast(BTCModel, h = 5)
EOSFcast <- forecast(EOSModel, h = 5)
ETHFcast <- forecast(ETHModel, h = 5)
XRPFcast <- forecast(XRPModel, h = 5)

#formatting as data frame
BCHpred <- as.data.frame(BCHFcast)
BTCpred <- as.data.frame(BTCFcast)
EOSpred <- as.data.frame(EOSFcast)
ETHpred <- as.data.frame(ETHFcast)
XRPpred <- as.data.frame(XRPFcast)

merged <- rbind(merged,BCHpred, BTCpred, EOSpred, ETHpred, XRPpred)
}

merged['Series'] = rep(c(rep('BCH',times=5),rep('BTC',times=5),rep('EOS',times=5),rep('ETH',times=5),rep('XRP',times=5)),times=iterations)
write.csv(merged, file = "History.csv", row.names = FALSE)