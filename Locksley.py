# Connor O'Keefe
# cokeefe

from cmu_112_graphics import *
import math, copy, random, decimal, statistics
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 


# Pandas documentation used: https://pandas.pydata.org/pandas-docs/stable/reference/general_functions.html
# YFinance documentation used: https://pypi.org/project/yfinance/
# Numpy documentation used: https://numpy.org/doc/stable/reference/index.html
# Matplotlib documentation used: https://matplotlib.org/3.1.0/index.html
# Sharpe ratio formulas come from 70-391 (Finance) taught at Carnegie Mellon
    # Sharpe ratio formula refreshed at https://www.investopedia.com/terms/s/sharperatio.asp
# Portfolio standard deviation formula from 70-391 simplified to matrix multiplication formula described in https://www.youtube.com/watch?v=5wresdHooHQ
# Sortino ratio formulas come from 99-520 (Machine Learning and Finance) taught at Carnegie Mellon
    # Sortino ratio formula refreshed at https://www.investopedia.com/terms/s/sortinoratio.asp
# Portfolio downside deviation formula from 99-520 simplified to formula described in https://www.youtube.com/watch?v=cMqDfSm5d8M
# Treynor ratio formulas come from 99-520 (Machine Learning and Finance) taught at Carnegie Mellon
    # Treynor ratio formula refreshed at https://www.investopedia.com/terms/t/treynorratio.asp
# Portfolio beta formula from 99-520 simplified to formula described in https://xplaind.com/749317/portfolio-beta#:~:text=Portfolio%20beta%20is%20a%20measure,individual%20stocks%20in%20a%20portfolio.
# Reading/writing text file notes viewed on CMU 15-112 course website at: https://www.cs.cmu.edu/~112/notes/hw7.html


# Taken from the 15-112 course website within the hw7 starter file provided at:
# https://www.cs.cmu.edu/~112/notes/hw7.html
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

# Taken from the 15-112 course website notes on strings:
# https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# Taken from the 15-112 course website notes on strings:
# https://www.cs.cmu.edu/~112/notes/notes-strings.html
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# function designed to get the current price of any inputted stock from Yahoo Finance
def getCurrentPrice(stock):
    stock = stock.upper()
    ticker = yf.Ticker(stock)
    tickerHist = ticker.history(period = "1d", interval = "1m")
    currentPrice = tickerHist.iloc[len(tickerHist) - 1]["Open"]
    return currentPrice

# starts the app (function framework taken from 15-112 course website at https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html)
def appStarted(app):

    app.timerDelay = 500

    # boolean trackers for entering different game modes
    app.gameStarted = False
    app.portfolioPage = False
    app.instructionsPage = False

    # starting amounts from intro page selection
    app.startAmount = None
    app.investing = None
    app.buyingPower = None
    app.totalInvested = 0
    app.totalBought = 0
    app.totalShort = 0

    # info for main portfolio table
    app.portMargin = 10
    app.portCols = 9
    app.portRows = 7
    app.portBoard = [([None] * app.portCols) for row in range(app.portRows)]
    app.colHeaders = ["Ticker", "Shares", "Bought At", "Current Price", "Current Value", "Profit", "% of Type", "% of Portfolio", "Action"]
    for i in range(len(app.colHeaders)):
        app.portBoard[0][i] = app.colHeaders[i]

    # info for main portfolio page
    app.expectedReturn = 0
    app.volatility = 0
    app.totalProfit = 0
    app.oldProfit = 0
    app.expChange = False
    app.accountValueLst = []

    # info for scrolling ticker board
    app.tickerCols = 10
    app.tickerRows = 2
    app.tickerBoard = [([None] * app.tickerCols) for row in range(app.tickerRows)]
    app.tickerIndex = 0
    app.scrollPause = False
    app.infoSelect = False
    app.tickSelectRow = None
    app.tickSelectCol = None
    app.tempTicker = None
    app.tempPrice = None
    app.drawInfo = False
    app.potentialStocks = ["FTDR", "LUV", "PFE", "AAPL", "MSFT", "AMZN", "T", "SNAP", "TWTR", "TSLA", "DIS", "BABA", "FB", "GE", "F", "AAL", "DAL", "GPRO", "GOLF"]

    # info for buy page
    app.shareCols = 12
    app.shareRows = 1
    app.sharePossible = ["1", "2", "3", "4", "5", "10", "20", "50", "100", "Limit", "Buy", "Short"]
    app.shareBoard =  [([None] * app.shareCols) for row in range(app.shareRows)]
    for i in range(len(app.sharePossible)):
        app.shareBoard[0][i] = app.sharePossible[i]
    app.selectedShares = None
    app.selectedCol = None
    app.actionCol = None
    app.boughtStocks = dict()
    app.longStocks = []
    app.statRows = 9
    app.statCols = 2
    app.statBoard = [([None] * app.statCols) for row in range(app.statRows)]
    app.keyStats = ["Company", "Price", "Stock History", "Dividend Yield", "Volume", "Forward P/E", "Forward EPS", "Beta", "Shares Outstanding"]
    for row in range(app.statRows):
        app.statBoard[row][0] = app.keyStats[row]
    app.statBoard[2][1] = "View Graph"
    app.limitStocks = dict()

    # info for optimization page
    app.drawOpti = False
    app.optiRatios = None
    app.maxSharpe = None
    app.maxSortino = None
    app.maxTreynor = None
    app.ratioSelected = None
    app.optiRows = 5
    app.optiCols = 2
    app.maxBoard = [([None] * app.optiCols) for row in range(app.optiRows)]
    app.selectOpti = False
    app.selectRows = 1
    app.selectCols = 3
    app.selectBoard = [([None] * app.selectCols) for row in range(app.selectRows)]
    app.selectBoard[0][0] = "Sharpe"
    app.selectBoard[0][1] = "Sortino"
    app.selectBoard[0][2] = "Treynor"
    app.riskReturnBoard = [([None] * (3)) for row in range(app.portRows - 2)]
    app.riskReturnBoard[0][0] = "Stock"
    app.riskReturnBoard[0][1] = "Exp. Return"
    app.riskReturnBoard[0][2] = "Volatility"

# toggles any key presses (function framework taken from 15-112 course website at https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html)
def keyPressed(app, event):

    # displays instructions page
    if event.key == "i":
        app.instructionsPage = not app.instructionsPage

    # reloads the previously saved portfolio and sets key info by reading a txt file
    elif not app.gameStarted and event.key == "r":
        lastPortfolio = readFile("Save_Port.txt")
        lines = lastPortfolio.splitlines()
        startInfo = lines[0].strip().split(' ')
        app.startAmount = float(startInfo[0])
        app.investing = float(startInfo[1])
        app.buyingPower = float(startInfo[2])
        app.totalProfit = float(startInfo[3])
        app.expectedReturn = float(startInfo[4])
        app.volatility = float(startInfo[5])
        app.totalBought = float(startInfo[6])
        app.totalShort = float(startInfo[7])
        app.totalInvested = float(startInfo[8])
        app.oldProfit = float(startInfo[9])
        for row in range(1, app.portRows):
            for col in range(app.portCols):
                if col in [1, 2, 3, 4, 5, 6, 7] and (lines[row].strip().split(' ')[col] != 'None'):
                    app.portBoard[row][col] = float(lines[row].strip().split(' ')[col])
                else:
                    app.portBoard[row][col] = lines[row].strip().split(' ')[col]
        for row in range(app.portRows):
            for col in range(app.portCols):
                if app.portBoard[row][col] == 'None':
                    app.portBoard[row][col] = None
        app.gameStarted = True
        app.portfolioPage = True

    # saves the portfolio by writing it to a txt file
    if app.portfolioPage and event.key == 's':
        contentsToWrite = f'{app.startAmount} {app.investing} {app.buyingPower} {app.totalProfit} {app.expectedReturn} {app.volatility} {app.totalBought} {app.totalShort} {app.totalInvested} {app.oldProfit}\n'
        for row in range(1, app.portRows):
            for col in range(app.portCols):
                if col == (app.portCols - 1):
                    contentsToWrite += f'{app.portBoard[row][col]}\n'
                else:
                    contentsToWrite += f'{app.portBoard[row][col]} '
        writeFile("Save_Port.txt", contentsToWrite)

# toggles any mouse presses (function framework taken from 15-112 course website at https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html)
def mousePressed(app, event):
    
    # establishes initial buying variables on title screen
    if not app.gameStarted:
        if ((7*app.width/16) <= event.x <= (9*app.width/16)) and ((15*app.height/32) <= event.y <= (17*app.height/32)):
            app.startAmount = 50000
            app.investing = 50000
            app.buyingPower = 50000
            app.gameStarted = True
            app.portfolioPage = True
        elif ((7*app.width/16) <= event.x <= (9*app.width/16)) and ((19*app.height/32) <= event.y <= (21*app.height/32)):
            app.startAmount = 10000
            app.investing = 10000
            app.buyingPower = 10000
            app.gameStarted = True
            app.portfolioPage = True
        elif ((7*app.width/16) <= event.x <= (9*app.width/16)) and ((23*app.height/32) <= event.y <= (25*app.height/32)):
            app.startAmount = 5000
            app.investing = 5000
            app.buyingPower = 5000
            app.gameStarted = True
            app.portfolioPage = True
        elif ((7*app.width/16) <= event.x <= (9*app.width/16)) and ((27*app.height/32) <= event.y <= (29*app.height/32)):
            app.startAmount = 1000
            app.investing = 1000
            app.buyingPower = 1000
            app.gameStarted = True
            app.portfolioPage = True
    else:
        # enter the game
        if app.portfolioPage and clickInScroll(app, event.x, event.y) and not app.infoSelect:
            # we click on a stock to stop the ticker 
            clickRow, clickCol = getScrollCell(app, event.x, event.y)
            if app.tickerBoard[0][clickCol] != None:
                app.scrollPause = True
                app.infoSelect = True
                # temporary variables to track for later draw functions
                app.tickSelectRow = clickRow
                app.tickSelectCol = clickCol
                app.tempTicker = app.tickerBoard[0][clickCol]
                app.tempPrice = app.tickerBoard[1][clickCol]
                # temporarily changes the text for the specific stock cell
                app.tickerBoard[0][clickCol] = "View Info"
                app.tickerBoard[1][clickCol] = "Exit"
        elif app.portfolioPage and clickInScroll(app, event.x, event.y) and app.infoSelect and not app.drawInfo:
            # once we select a stock, we have two options: View Info and Exit
            clickRow, clickCol = getScrollCell(app, event.x, event.y)
            if clickCol == app.tickSelectCol:
                if clickRow == 1:
                    # exit the selected cell and return to normal
                    app.tickerBoard[0][clickCol] = app.tempTicker
                    app.tickerBoard[1][clickCol] = app.tempPrice
                    app.scrollPause = False
                    app.infoSelect = False
                if clickRow == 0:
                    # enter the drawInfo page which includes an option to buy and graphs
                    app.portfolioPage = False
                    app.drawInfo = True
                    tickerObject = yf.Ticker(app.tempTicker)
                    tickerInfo = ["shortName", "", "", "dividendYield", "regularMarketVolume", "forwardPE", "forwardEps", "beta", "sharesOutstanding"]
                    # retrieves key info from Yahoo Finance
                    for row in range(app.statRows):
                        if row == 2:
                            pass
                        elif row == 1:
                            app.statBoard[row][1] = app.tempPrice
                        else:
                            if tickerObject.info[tickerInfo[row]] == None:
                                app.statBoard[row][1] = "None"
                            else:
                                app.statBoard[row][1] = tickerObject.info[tickerInfo[row]]
        # toggle for buying stocks, area is subject to change
        elif not app.portfolioPage and app.drawInfo:
            if clickInShares(app, event.x, event.y):
                clickRow, clickCol = getShareCell(app, event.x, event.y)
                # if we click a number, change our selected shares amount
                if clickCol < (app.shareCols - 3):
                    app.selectedShares = int(app.shareBoard[clickRow][clickCol])
                    app.selectedCol = clickCol
                # limit buys
                elif (clickCol == app.shareCols - 3) and (app.selectedShares != None):
                    app.actionCol = clickCol
                    limitPrice = input("Type a limit price:")
                    app.limitStocks[app.tempTicker] = [app.selectedShares, float(limitPrice)]
                    app.portfolioPage = True
                    app.expChange = True
                    app.drawInfo = False
                    app.scrollPause = False
                    app.infoSelect = False
                    app.tickerBoard[0][app.tickSelectCol] = app.tempTicker
                    app.tickerBoard[1][app.tickSelectCol] = app.tempPrice
                    app.selectedCol = None
                    app.actionCol = None
                # buying stocks
                elif (clickCol == app.shareCols - 2) and (app.selectedShares != None) and (app.selectedShares * app.tempPrice <= app.buyingPower):
                    # change buying power and investing amount
                    app.timerDelay -= 70
                    app.actionCol = clickCol
                    app.buyingPower -= round(app.selectedShares * getCurrentPrice(app.tempTicker), 2)
                    for row in range(1, app.portRows - 2):
                        # if the stock is already in portfolio, add the selected shares
                        if app.tempTicker == app.portBoard[row][0]:
                            app.portBoard[row][1] += app.selectedShares
                            app.portBoard[row][2] = round(((app.boughtStocks[app.tempTicker] * app.portBoard[row][2]) + (app.selectedShares * app.tempPrice))/(app.boughtStocks[app.tempTicker] + app.selectedShares), 2)
                            app.boughtStocks[app.tempTicker] += app.selectedShares
                            app.totalBought += round(app.selectedShares * app.tempPrice, 2)
                            break
                        # if the stock is not in the portfolio, create a new line in the portfolio with all the necessary info
                        elif app.portBoard[row][0] == None:
                            app.portBoard[row][0] = app.tempTicker
                            app.portBoard[row][1] = app.selectedShares
                            app.portBoard[row][2] = app.tempPrice
                            app.portBoard[row][3] = app.tempPrice
                            app.portBoard[row][4] = round(app.portBoard[row][1] * app.tempPrice, 2)
                            app.totalInvested += round(app.portBoard[row][1] * app.tempPrice, 2)
                            app.totalBought += app.portBoard[row][1] * app.tempPrice
                            app.portBoard[row][5] = 0
                            app.portBoard[row][6] = round((app.portBoard[row][1] * app.tempPrice)/app.totalBought, 2)
                            app.portBoard[row][7] = round((app.portBoard[row][1] * app.tempPrice)/abs(app.totalInvested), 2)
                            app.portBoard[row][8] = "Sell"
                            app.boughtStocks[app.tempTicker] = app.selectedShares
                            app.longStocks.append(app.tempTicker)
                            break
                    # after buying, return to the main portfolio page and revert ticker scroll to original
                    app.portfolioPage = True
                    app.expChange = True
                    app.drawInfo = False
                    app.scrollPause = False
                    app.infoSelect = False
                    app.tickerBoard[0][app.tickSelectCol] = app.tempTicker
                    app.tickerBoard[1][app.tickSelectCol] = app.tempPrice
                    app.selectedCol = None
                    app.actionCol = None

                # shorting stocks
                elif (clickCol == app.shareCols - 1) and (app.selectedShares != None) and (app.selectedShares * app.tempPrice * 1.5 <= app.buyingPower): # we require 1.5x buying power on short sales
                    app.timerDelay -= 70
                    app.actionCol = clickCol
                    # cannot buy stocks you have already shorted
                    if app.tempTicker in app.longStocks:
                        print("Cannot short a security you have already bought!")
                    else:
                        app.buyingPower -= round(app.selectedShares * getCurrentPrice(app.tempTicker), 2)
                        for row in range(app.portRows - 2, app.portRows):
                            # if stock has already been shorted, subtract the selected shares
                            if app.tempTicker == app.portBoard[row][0]:
                                app.portBoard[row][1] -= app.selectedShares
                                app.portBoard[row][2] = ((app.boughtStocks[app.tempTicker] * abs(app.portBoard[row][2])) + (app.selectedShares * app.tempPrice))/(abs(app.boughtStocks[app.tempTicker]) + app.selectedShares)
                                app.boughtStocks[app.tempTicker] -= app.selectedShares
                                app.totalShort += round(app.selectedShares * app.tempPrice, 2)
                                break
                            # if the stock has not already been shorted, create a new line with all necessary info
                            elif app.portBoard[row][0] == None:
                                app.portBoard[row][0] = app.tempTicker
                                app.portBoard[row][1] = 0 - app.selectedShares
                                app.portBoard[row][2] = app.tempPrice
                                app.portBoard[row][3] = app.tempPrice
                                app.portBoard[row][4] = round(app.portBoard[row][1] * app.tempPrice, 2)
                                app.totalInvested += round(app.portBoard[row][1] * app.tempPrice, 2)
                                app.totalShort += round(app.portBoard[row][1] * app.tempPrice, 2)
                                app.portBoard[row][5] = 0
                                app.portBoard[row][6] = round((app.portBoard[row][1] * app.tempPrice)/app.totalShort, 2)
                                app.portBoard[row][7] = round((app.portBoard[row][1] * app.tempPrice)/app.totalInvested, 2)
                                app.portBoard[row][8] = "Return"
                                app.boughtStocks[app.tempTicker] = 0 - app.selectedShares
                                break
                        # after shorting, return to the main portfolio page and revert ticker scroll to original
                        app.portfolioPage = True
                        app.expChange = True
                        app.drawInfo = False
                        app.scrollPause = False
                        app.infoSelect = False
                        app.tickerBoard[0][app.tickSelectCol] = app.tempTicker
                        app.tickerBoard[1][app.tickSelectCol] = app.tempPrice
                        app.selectedCol = None
                        app.actionCol = None
            # if we click the X, exit the page
            elif clickInX(app, event.x, event.y):
                app.portfolioPage = True
                app.drawInfo = False
                app.scrollPause = False
                app.infoSelect = False
                app.tickerBoard[0][app.tickSelectCol] = app.tempTicker
                app.tickerBoard[1][app.tickSelectCol] = app.tempPrice
            # clicking in the stats board will display a graph if the selected cell is View Graph
            elif clickInStats(app, event.x, event.y):
                (clickRow, clickCol) = getStatsCell(app, event.x, event.y)
                if (clickRow, clickCol) == (2, 1):
                    tickerObject = yf.Ticker(app.tempTicker)
                    data = tickerObject.history(period = "1y", interval = "1d")
                    plt.plot(data["Close"])
                    plt.ylabel("Closing Price")
                    plt.show()
                    plt.close()
        elif clickInPort(app, event.x, event.y) and not app.drawInfo:
            clickRow, clickCol = getPortCell(app, event.x, event.y)
            # sells all shares of stocks that were previously bought
            if app.portBoard[clickRow][clickCol] == "Sell":
                app.timerDelay += 70
                app.totalBought -= app.portBoard[clickRow][4]
                app.totalInvested -= app.portBoard[clickRow][4]
                app.buyingPower += round(app.portBoard[clickRow][4], 2)
                app.oldProfit += app.portBoard[clickRow][5]
                app.longStocks.remove(app.portBoard[clickRow][0])
                del app.boughtStocks[app.portBoard[clickRow][0]]
                app.portBoard.pop(clickRow)
                app.portBoard.insert(app.portRows - 3, ([None] * app.portCols))
                app.expChange = True
                if app.portBoard[1][0] == None:
                    app.buyingPower = app.investing
            # returns all share of stocks that were previously shorted
            elif app.portBoard[clickRow][clickCol] == "Return":
                app.timerDelay += 70
                app.totalInvested -= app.portBoard[clickRow][4]
                app.totalShort -= app.portBoard[clickRow][4]
                app.buyingPower += round((abs(app.portBoard[clickRow][1])) * (app.portBoard[clickRow][2] - app.portBoard[clickRow][3]), 2)
                app.buyingPower += round(abs(app.portBoard[clickRow][1]) * app.portBoard[clickRow][2], 2)
                app.investing += round(app.portBoard[clickRow][4], 2)
                app.investing += round(abs(app.portBoard[clickRow][1]) * app.portBoard[clickRow][2], 2)
                app.oldProfit += app.portBoard[clickRow][5]
                del app.boughtStocks[app.portBoard[clickRow][0]]
                app.portBoard.pop(clickRow)
                app.portBoard.append([None] * app.portCols)
                app.expChange = True
                if app.portBoard[1][0] == None:
                    app.buyingPower = app.investing
        # enters the optimization choices page
        elif app.portfolioPage and clickInOpti(app, event.x, event.y):
            if len(app.longStocks) < 2:
                print("Cannot optimize a portfolio with one stock!") # later create a popup error message
            else:
                # draw the risk-return board with exp. return and volatility for each long security
                app.portfolioPage = False
                app.drawOpti = True
                for row in range(1, app.portRows - 2):
                    if app.portBoard[row][0] != None and app.portBoard[row][0] != 'None':
                        app.riskReturnBoard[row][0] = app.portBoard[row][0]
                        app.riskReturnBoard[row][1] = round(expectedReturn2D(app.portBoard[row][0], yf.download(app.portBoard[row][0], period = "2y", interval = "1wk")), 2)
                        app.riskReturnBoard[row][2] = round(getSTDEV2D(app.portBoard[row][0], yf.download(app.portBoard[row][0], period = "2y", interval = "1wk")), 2)
        # clicking in "Portfolio History" displays a graph of account value history
        elif app.portfolioPage and clickInPortHistory(app, event.x, event.y):
            plt.plot(app.accountValueLst)
            plt.ylabel("Account Value")
            plt.xticks([], " ")
            plt.show()
            plt.close()
        # pressing "Apply" on the optimization page applies the optimum weights to our portfolio
        elif app.drawOpti and clickInOptiApply(app, event.x, event.y) and app.selectOpti:
            for i in range(len(app.longStocks)):
                if app.portBoard[i+1][0] != None:
                    # updates info
                    currPrice = getCurrentPrice(app.portBoard[i+1][0])
                    app.portBoard[i+1][6] = int(app.optiWeights[i])
                    app.portBoard[i+1][4] = round(app.totalBought * app.optiWeights[i], 2)
                    app.portBoard[i+1][3] = round(currPrice, 2)
                    app.portBoard[i+1][1] = round(app.portBoard[i+1][4] / currPrice, 2)
                    app.boughtStocks[app.portBoard[i+1][0]] += app.portBoard[i+1][1]
            for i in range(1, len(app.portBoard)):
                # updates info
                if app.portBoard[i][0] != None:
                    if almostEqual(int(app.portBoard[i][1]), 0):
                        app.timerDelay += 70
                        app.oldProfit += app.portBoard[i][5]
                        app.totalBought -= app.portBoard[i][4]
                        app.totalInvested -= app.portBoard[i][4]
                        app.buyingPower += round(app.portBoard[i][4], 2)
                        app.longStocks.remove(app.portBoard[i][0])
                        del app.boughtStocks[app.portBoard[i][0]]
                        app.portBoard.pop(i)
                        app.portBoard.insert(app.portRows - 3, ([None] * app.portCols))
                        app.expChange = True
            # resets board with optimum weights
            for row in range(app.optiRows):
                for col in range(app.optiCols):
                    app.maxBoard[row][col] = None
            app.ratioSelected = None
            app.portfolioPage = True
            app.drawOpti = False
            app.expChange = True
            app.selectOpti = False
        # selects the ratio to optimize the portfolio on
        elif app.drawOpti and clickInOptions(app, event.x, event.y):
            app.selectOpti = True
            (clickRow, clickCol) = getOptionsCell(app, event.x, event.y)
            app.ratioSelected = clickCol
            if (clickRow, clickCol) == (0, 0):
                # allows for different number of long positions
                if len(app.longStocks) == 4:
                    app.optiWeights, app.maxSharpe = maxSharpeRatio4(app.longStocks)
                elif len(app.longStocks) == 3:
                    app.optiWeights, app.maxSharpe = maxSharpeRatio3(app.longStocks)
                elif len(app.longStocks) == 2:
                    app.optiWeights, app.maxSharpe = maxSharpeRatio2(app.longStocks)
                app.maxBoard[0][0] = "Max Sharpe"
                app.maxBoard[0][1] = round(app.maxSharpe, 4)
                for i in range(len(app.longStocks)):
                    j = i + 1
                    app.maxBoard[j][0] = app.longStocks[i]
                    app.maxBoard[j][1] = app.optiWeights[i]
            elif (clickRow, clickCol) == (1, 0):
                # allows for different number of long positions
                if len(app.longStocks) == 4:
                    app.optiWeights, app.maxSortino = maxSortinoRatio4(app.longStocks)
                elif len(app.longStocks) == 3:
                    app.optiWeights, app.maxSortino = maxSortinoRatio3(app.longStocks)
                elif len(app.longStocks) == 2:
                    app.optiWeights, app.maxSortino = maxSortinoRatio2(app.longStocks)
                app.maxBoard[0][0] = "Max Sortino"
                app.maxBoard[0][1] = round(app.maxSortino, 4)
                for i in range(len(app.longStocks)):
                    j = i + 1
                    app.maxBoard[j][0] = app.longStocks[i]
                    app.maxBoard[j][1] = app.optiWeights[i]
            elif (clickRow, clickCol) == (2, 0):
                # allows for different number of long positions
                if len(app.longStocks) == 4:
                    app.optiWeights, app.maxTreynor = maxTreynorRatio4(app.longStocks)
                elif len(app.longStocks) == 3:
                    app.optiWeights, app.maxTreynor = maxTreynorRatio3(app.longStocks)
                elif len(app.longStocks) == 2:
                    app.optiWeights, app.maxTreynor = maxTreynorRatio2(app.longStocks)
                app.maxBoard[0][0] = "Max Treynor"
                app.maxBoard[0][1] = round(app.maxTreynor, 4)
                for i in range(len(app.longStocks)):
                    j = i + 1
                    app.maxBoard[j][0] = app.longStocks[i]
                    app.maxBoard[j][1] = app.optiWeights[i]
        # clicking in X returns to main portfolio page
        elif app.drawOpti and clickInX(app, event.x, event.y):
            app.portfolioPage = True
            app.drawOpti  = False
            app.scrollPause = False
            app.infoSelect = False

# toggles for the timer (function framework taken from 15-112 course website at https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html)
def timerFired(app):
    timerTicker(app)
    timerPriceUpdates(app)
    timerProfitUpdate(app)
    timerExpReturnUpdate(app)
    timerLimitBuys(app)

# checks if any of the limit orders have hit, and adds them to portfolio if so
def timerLimitBuys(app):
    if app.portfolioPage and len(app.limitStocks) > 0:
        limitBuys = []
        for stock in app.limitStocks:
            currPrice = getCurrentPrice(stock)
            if currPrice <= app.limitStocks[stock][1]:
                limitBuys.append(stock)
                app.timerDelay -= 70
                app.buyingPower -= round(app.limitStocks[stock][0] * currPrice, 2)
                for row in range(1, app.portRows - 2):
                    if stock == app.portBoard[row][0]:
                        app.portBoard[row][1] += app.limitStocks[stock][0]
                        app.portBoard[row][2] = round(((app.boughtStocks[app.tempTicker] * app.portBoard[row][2]) + (app.limitStocks[stock][0] * currPrice))/(app.boughtStocks[app.tempTicker] + app.limitStocks[stock][0]), 2)
                        app.boughtStocks[app.tempTicker] += app.limitStocks[stock][0]
                        app.totalBought += round(app.limitStocks[stock][0] * app.limitStocks[stock][1], 2)
                        break
                    elif app.portBoard[row][0] == None:
                        app.portBoard[row][0] = stock
                        app.portBoard[row][1] = app.limitStocks[stock][0]
                        app.portBoard[row][2] = app.limitStocks[stock][1]
                        app.portBoard[row][3] = currPrice
                        app.portBoard[row][4] = round(app.portBoard[row][1] * app.limitStocks[stock][1], 2)
                        app.totalInvested += round(app.portBoard[row][1] * app.limitStocks[stock][1], 2)
                        app.totalBought += app.portBoard[row][1] * app.limitStocks[stock][1]
                        app.portBoard[row][5] = 0
                        app.portBoard[row][6] = round((app.portBoard[row][1] * app.limitStocks[stock][1])/app.totalBought, 2)
                        app.portBoard[row][7] = round((app.portBoard[row][1] * app.limitStocks[stock][1])/abs(app.totalInvested), 2)
                        app.portBoard[row][8] = "Sell"
                        app.boughtStocks[app.tempTicker] = app.limitStocks[stock][0]
                        app.longStocks.append(stock)
                        break
        for stock in limitBuys:
            del app.limitStocks[stock]

# updates the total profit by adding all the current portfolio profits plus any old profits
def timerProfitUpdate(app):
    if app.portfolioPage:
        app.totalProfit = app.oldProfit
        for row in range(1, app.portRows):
            if app.portBoard[row][0] != None:
                app.totalProfit += app.portBoard[row][5]
        app.totalProfit = round(app.totalProfit, 2)
        for row in range(1, app.portRows):
            if app.portBoard[row][0] != None and app.portBoard[row][0] != 'None':
                app.boughtStocks[app.portBoard[row][0]] = app.portBoard[row][1]

# updates the portfolio expected return and volatility on the main portfolio page if there are any changes in the portfolio
def timerExpReturnUpdate(app):
    if app.portfolioPage:
        if app.expChange:
            app.expectedReturn = 0
            app.volatility = 0
            stocks = []
            weights = []
            if len(app.boughtStocks) > 0:
                for row in range(1, app.portRows):
                    if app.portBoard[row][0] != None:
                        stocks.append(app.portBoard[row][0])
                        weights.append(app.portBoard[row][7])
                        data = yf.download(app.portBoard[row][0], period = "2y", interval = "1wk")
                        expReturn = expectedReturn2D(app.portBoard[row][0], data)
                        weighted = expReturn * app.portBoard[row][7]
                        app.expectedReturn += weighted
                if len(stocks) == 1:
                    data = yf.download(stocks[0], period = "2y", interval = "1wk")
                    app.volatility = round(getSTDEV2D(stocks[0], data), 2)
                elif len(stocks) > 1:
                    data = yf.download(' '.join(stocks), period = "2y", interval = "1wk")
                    app.volatility = round(portSTDEV(stocks, weights, data), 2)
            app.expectedReturn = round(app.expectedReturn, 2)
    app.expChange = False

# makes the ticker scroll with updated stock prices
def timerTicker(app):
    if app.portfolioPage and not app.scrollPause:
        newStock = app.potentialStocks[app.tickerIndex % (len(app.potentialStocks))]
        newStockPrice = getCurrentPrice(newStock)
        newStockPrice = round(newStockPrice, 2)
        app.tickerBoard[0].pop()
        app.tickerBoard[1].pop()
        app.tickerBoard[0].insert(0, newStock)
        app.tickerBoard[1].insert(0, newStockPrice)
        app.tickerIndex += 1

# updates the info for each stock in the portfolio based on most recent stock price
def timerPriceUpdates(app):
    app.accountValueLst.append(app.investing)
    if app.portfolioPage:
        for row in range(1, app.portRows):
            # updates prices and profit for long securities
            if (app.portBoard[row][0] != None and app.portBoard[row][0] != 'None'):
                if not isinstance(app.portBoard[row][1], str): 
                    if app.portBoard[row][1] > 0:
                        currPrice = getCurrentPrice(app.portBoard[row][0])
                        app.totalInvested -= app.portBoard[row][4]
                        app.totalBought -= app.portBoard[row][5]
                        app.portBoard[row][3] = round(currPrice, 2)
                        app.portBoard[row][4] = round(app.portBoard[row][1] * currPrice, 2)
                        app.portBoard[row][5] = round((app.portBoard[row][3] - app.portBoard[row][2]) * app.portBoard[row][1], 2)
                        app.totalInvested += app.portBoard[row][4]
                        app.totalBought += app.portBoard[row][5]
                        app.portBoard[row][6] = round((app.portBoard[row][1] * currPrice)/app.totalBought, 2)
                        app.portBoard[row][7] = round((app.portBoard[row][1] * currPrice)/abs(app.totalInvested), 2)
            # updates prices and profit for short securities
            elif (app.portBoard[row][0] != None and app.portBoard[row][0] != 'None') and not isinstance(app.portBoard[row][1], str) and float(app.portBoard[row][1]) < 0:
                currPrice = getCurrentPrice(app.portBoard[row][0])
                app.totalInvested -= app.portBoard[row][4]
                app.totalShort -= app.portBoard[row][5]
                app.portBoard[row][3] = round(currPrice, 2)
                app.portBoard[row][4] = round(app.portBoard[row][1] * currPrice, 2)
                app.portBoard[row][5] = round((app.portBoard[row][2] - app.portBoard[row][3]) * abs(app.portBoard[row][1]), 2)
                app.totalInvested += app.portBoard[row][4]
                app.totalShort += app.portBoard[row][5]
                app.portBoard[row][6] = round((app.portBoard[row][1] * currPrice)/app.totalShort, 2)
                app.portBoard[row][7] = round((app.portBoard[row][1] * currPrice)/abs(app.totalInvested), 2)
            app.investing = round(app.startAmount + app.totalProfit, 2)
            app.buyingPower = round(app.buyingPower, 2)

def redrawAll(app, canvas):

    # draws intro splash page
    if not app.gameStarted and not app.instructionsPage:
        drawIntro(app, canvas)
    # draws instructions page
    elif app.instructionsPage:
        drawInstructions(app, canvas)
    # draws menu and mode selections
    elif app.gameStarted and app.portfolioPage and not app.instructionsPage:
        drawPortfolioPage(app, canvas)
    # draws stock info and buying page
    elif app.gameStarted and app.drawInfo and not app.instructionsPage:
        drawStockInfo(app, canvas)
    # draws the optimization options page
    elif app.gameStarted and app.drawOpti and not app.instructionsPage:
        drawOptiOptions(app, canvas)

# draws the instructions page
def drawInstructions(app, canvas):
    canvas.create_text(app.portMargin, app.portMargin, text = "TITLE SCREEN INSTRUCTIONS", font = "Arial 18 bold", anchor = "nw", fill = "yellow")
    canvas.create_text(2 * app.portMargin, app.portMargin + 30, text = "On the title screen, there are two options. If you would like to start a new portfolio, select a starting amount of\nmoney to begin trading. If you would like to load your previous trading session, press 'r', and begin trading.", font = "Arial 12", anchor = "nw")
    canvas.create_text(app.portMargin, app.portMargin + 68, text = "MAIN PORTFOLIO PAGE INSTRUCTIONS", font = "Arial 18 bold", anchor = "nw", fill = "red")
    canvas.create_text(2 * app.portMargin, app.portMargin + 98, text = "On the main portfolio page, we see a stock ticker scroll with live prices of select NYSE stocks. If we select a\nstock, we get an option to 'View Info', which will take you to an information page to buy/short/limit stocks.\nThe large grid tracks all of the stocks that are bought and shorted. Up to four long stocks and two short stocks\ncan be traded. In between the ticker scroll and portfolio board are 6 trackers. Starting amount is how much\nmoney you started with, account value is total buying power + profit, buying power is how much can be used to\ntrade stocks, profit is how much money you've made with your current portfolio, expected return is how much\nthe current holdings are expected to make annually, and volatility is the annual volatility of current holdings.\nFinally, clicking 'Optimize Portfolio' takes you to a selection to optimize current long holdings, and clicking\n'Portfolio History' shows a history of account value. To save your portfolio for future trading sessions, press 's'.", font = "Arial 12", anchor = "nw")
    canvas.create_text(app.portMargin, app.portMargin + 260, text = "STOCK INFO PAGE INSTRUCTIONS", font = "Arial 18 bold", anchor = "nw", fill = "green")
    canvas.create_text(2 * app.portMargin, app.portMargin + 290, text = "On the stock info page, we first notice a stock info grid containing key stats about the stock and company.\nThere is also a selection to view a graph of historical prices. At the top of the screen, we see an option to select\nshares. Click on the number of shares you want to trade, and then select whether you want to buy, short, or place\na limit order. If you buy or short the shares, they will immediately appear on your portfolio page. If you select a\nlimit, you will be asked to input a price, and if the stock dips below that price, it will immediately be bought\nfor you.", font = "Arial 12", anchor = "nw")
    canvas.create_text(app.portMargin, app.portMargin + 400, text = "OPTIMIZING PAGE INSTRUCTIONS", font = "Arial 18 bold", anchor = "nw", fill = "blue")
    canvas.create_text(2 * app.portMargin, app.portMargin + 430, text = "On the optimizing page, there is a table with the expected return and volatility for each individual long stock in\nthe current portfolio. At the top of the screen, there are three optimum portfolio selections (Sharpe, Sortino,\nTreynor) that assign weights to the current long stocks by maximizing the selected risk-return ratio. If you so\nchoose, you may select to apply the ratio maximizing weights to your portfolio.", font = "Arial 12", anchor = "nw")

# draws info for the optimization page
def drawOptiOptions(app, canvas):
    drawXOut(app, canvas)
    drawOptions(app, canvas)
    drawMaxGrid(app, canvas)
    drawRiskReturn(app, canvas)

# main function for drawing risk return board on optimization page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawRiskReturn(app, canvas):
    for row in range(len(app.riskReturnBoard)):
        for col in range(len(app.riskReturnBoard[0])):
            drawCellForRiskReturn(app, canvas, row, col)

# draws individual cells for risk return board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForRiskReturn(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsForRiskReturn(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.riskReturnBoard[row][col])

# gets width and height for cells for risk return board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForRiskReturn(app):
    # helper function to determine column width and row height for portfolio list
    gridWidth  = app.width/4
    gridHeight = app.height/2
    columnWidth = gridWidth / len(app.riskReturnBoard[0])
    rowHeight = gridHeight / len(app.riskReturnBoard)
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for risk return board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForRiskReturn(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForRiskReturn(app)
    x0 = 3*app.width/16 + col * colW
    x1 = x0 + colW
    y0 = 3*app.height/8 + row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# main function for drawing optimization options board on optimization page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawOptions(app, canvas):
    for row in range(app.selectRows):
        for col in range(app.selectCols):
            drawCellForOptions(app, canvas, row, col)

# draws individual cells for otimization options board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForOptions(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsForOptions(app, row, col)
    if col == app.ratioSelected:
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'green')
    else:
        canvas.create_rectangle(x0, y0, x1, y1)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.selectBoard[row][col], font = 'Arial 28 bold')

# gets width and height for cells for optimization options board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForOptions(app):
    # helper function to determine column width and row height for portfolio list
    gridWidth  = 6*app.width/8
    gridHeight = app.height/9
    columnWidth = gridWidth / app.selectCols
    rowHeight = gridHeight / app.selectRows
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for optimization options board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForOptions(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForOptions(app)
    x0 = app.width/8 + col * colW
    x1 = x0 + colW
    y0 = row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# sees if click occurred in optimization options
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInOptions(app, x, y):
    return ((app.width/8 <= x <= 7*app.width/8) and
            (0 <= y <= app.height/9))

# returns the cell that was clicked in the optimization options
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getOptionsCell(app, x, y):
    colW, rowH = widthAndHeightForOptions(app)
    row = int((y - 0) / rowH)
    col = int((x - app.width/8) / colW)
    return row, col

# main function for drawing the maximum weights board on optimization page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawMaxGrid(app, canvas):
    for row in range(app.optiRows):
        for col in range(app.optiCols):
            drawCellForMaxGrid(app, canvas, row, col)
    canvas.create_rectangle(9*app.width/16, 2*app.height/8, 13*app.width/16, 3*app.height/8, fill = 'light green')
    canvas.create_text(11*app.width/16, 5*app.height/16, text = "Apply!", font = 'Arial 12 bold')

# draws individual cells for maximum weights board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForMaxGrid(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsForMaxGrid(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.maxBoard[row][col])

# gets width and height for cells for maximum weights board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForMaxGrid(app):
    # helper function to determine column width and row height for portfolio list
    gridWidth  = app.width/4
    gridHeight = app.height/2
    columnWidth = gridWidth / app.optiCols
    rowHeight = gridHeight / app.optiRows
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for maximum weights board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForMaxGrid(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForMaxGrid(app)
    x0 = 9*app.width/16 + col * colW
    x1 = x0 + colW
    y0 = 3*app.height/8 + row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# sees if click occurred in "Apply" cell
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInOptiApply(app, x, y):
    return ((9*app.width/16 <= x <= 13*app.width/16) and (2*app.height/8 <= y <= 3*app.height/8))

# draws the stock information page
def drawStockInfo(app, canvas):
    drawXOut(app, canvas)
    drawShareOptions(app, canvas)
    drawKeyStats(app, canvas)

# main function for drawing the key stats board on optimization page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawKeyStats(app, canvas):
    for row in range(app.statRows):
        for col in range(app.statCols):
            drawCellForStats(app, canvas, row, col)

# draws individual cells for key stats board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForStats(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsForStats(app, row, col)
    if (row, col) == (2, 1):
        canvas.create_rectangle(x0, y0, x1, y1, fill = "light yellow")
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.statBoard[row][col])
    else:
        canvas.create_rectangle(x0, y0, x1, y1)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.statBoard[row][col])

# gets width and height for cells for key stats board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForStats(app):
    # helper function to determine column width and row height for share selection
    statWidth  = app.width/3
    statHeight = 2*app.height/3
    columnWidth = statWidth / app.statCols
    rowHeight = statHeight / app.statRows
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for key stats board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForStats(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForStats(app)
    x0 = app.width/3 + col * colW
    x1 = x0 + colW
    y0 = app.height/4 + row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# sees if click occurred in key stats grid
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInStats(app, x, y):
    return ((app.width/3 <= x <= 2*app.width/3) and
            (app.height/4 <= y <= app.height/4 + 2*app.height/3))

# returns the cell that was clicked in the key stats board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getStatsCell(app, x, y):
    colW, rowH = widthAndHeightForStats(app)
    row = int((y - app.height/4) / rowH)
    col = int((x - app.width/3) / colW)
    return row, col

# main function for drawing the share options board on stock info page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawShareOptions(app, canvas):
    for row in range(app.shareRows):
        for col in range(app.shareCols):
            if col == app.selectedCol or col == app.actionCol:
                drawCellForShares(app, canvas, row, col, 'green', 3)
            elif col == (app.shareCols - 3) or col == (app.shareCols - 2) or col == (app.shareCols - 1):
                drawCellForShares(app, canvas, row, col, 'light grey', 5)
            else:
                drawCellForShares(app, canvas, row, col, None, 2)

# creates X to X Out of stock info page
def drawXOut(app, canvas):
    canvas.create_rectangle(app.width - 20, 0, app.width, 20, fill = 'red')
    canvas.create_line(app.width - 20, 0, app.width, 20)
    canvas.create_line(app.width, 0, app.width - 20, 20)

# sees if click occurred in X
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInX(app, x, y):
    return ((app.width - 20 <= x <= app.width) and (0 <= y <= 20))

# draws individual cells for share selection board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForShares(app, canvas, row, col, color, thickness):
    x0, y0, x1, y1 = getCellBoundsForShares(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = thickness)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.shareBoard[row][col])

# gets width and height for cells for share selection board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForShares(app):
    # helper function to determine column width and row height for share selection
    shareWidth  = app.width - 2*app.portMargin
    shareHeight = app.height/8
    columnWidth = shareWidth / app.shareCols
    rowHeight = shareHeight / app.shareRows
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for share selection board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForShares(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForShares(app)
    x0 = app.portMargin + col * colW
    x1 = x0 + colW
    y0 = 3 * app.portMargin + row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# sees if click occurred in share selection board
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInShares(app, x, y):
    return ((app.portMargin <= x <= app.width - app.portMargin) and
            (app.portMargin <= y <= 3 * app.portMargin + app.height/8))

# returns the cell that was clicked in the share selection board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getShareCell(app, x, y):
    colW, rowH = widthAndHeightForShares(app)
    row = int((y - 3 * app.portMargin) / rowH)
    col = int((x - app.portMargin) / colW)
    return row, col


# draws intro splash page
def drawIntro(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text = 'Locksley', font = 'Arial 48 bold',
                        anchor = 's', fill = 'green')
    canvas.create_text(app.width/2, 3*app.height/8, text = "Select a portfolio amount!", font = 'Arial 24 bold',
                        anchor = 's')
    canvas.create_text(app.width/2, 3*app.height/8, text = "Or press 'r' to load your most recent saved portfolio!", font = 'Arial 24 bold',
                        anchor = 'n')
    canvas.create_text(app.width/2, app.height, text = "Press 'i' at any time to view instructions!", font = 'Arial 24 bold',
                        anchor = 's')                    
    drawPortSelections(app, canvas)

# draws buttons for initial buying power selection
def drawPortSelections(app, canvas):
    x0 = 7*app.width/16
    x1 = 9*app.width/16
    y0 = 15*app.height/32
    yDiff = app.height/16
    y1 = y0 + yDiff
    amounts = ["$50,000", "$10,000", "$5,000", "$1,000"]
    for i in range(0, 8, 2):
        canvas.create_rectangle(x0, y0 + i*yDiff, x1, y1 + i*yDiff, fill = 'light grey', outline = 'black', width = 4)
        index = i//2
        canvas.create_text((x0+x1)/2, ((y0 + i*yDiff)+(y1 + i*yDiff))/2, text = amounts[index], font = 'Arial 14 bold')

# parent draw function for main portfolio page
def drawPortfolioPage(app, canvas):
    drawStartAmounts(app, canvas)
    drawPortfolio(app, canvas)
    drawTickerScroll(app, canvas)
    drawPortOptions(app, canvas)

# creates spaces to view portfolio statistics
def drawPortOptions(app, canvas):
    if app.totalProfit >= 0:
        canvas.create_text(app.width/2, 3*app.height/16, text = 'Total Profit: $', anchor = 'se', font = 'Arial 12 bold', fill = 'green')
    else:
        canvas.create_text(app.width/2, 3*app.height/16, text = 'Total Profit: -$', anchor = 'se', font = 'Arial 12 bold', fill = 'green')
    canvas.create_text(app.width/2, 3*app.height/16, text = f'{abs(app.totalProfit)}', anchor = 'sw', font = 'Arial 12 bold', fill = 'green')
    canvas.create_text(app.width/2, 4*app.height/16, text = 'Exp. Return: ', anchor = 'se', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, 4*app.height/16, text = f'{app.expectedReturn}', anchor = 'sw', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, 5*app.height/16, text = 'Volatility: ', anchor = 'se', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, 5*app.height/16, text = f'{app.volatility}', anchor = 'sw', font = 'Arial 12 bold')
    canvas.create_rectangle(5*app.width/8, 3*app.height/16, 7*app.width/8, 4*app.height/16, fill = 'light green')
    canvas.create_text(6*app.width/8, 7*app.height/32, text = 'Optimize Portfolio', font = 'Arial 12 bold')
    canvas.create_rectangle(5*app.width/8, 4*app.height/16, 7*app.width/8, 5*app.height/16, fill = 'light blue')
    canvas.create_text(6*app.width/8, 9*app.height/32, text = 'Portfolio History', font = 'Arial 12 bold')

# sees if click occurred in "Optimize Portfolio" cell
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInOpti(app, x, y):
    return ((5*app.width/8 <= x <= 7*app.width/8) and
            (3*app.height/16 <= y <= 4*app.height/16))

# sees if click occurred in "Portfolio History" cell
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInPortHistory(app, x, y):
    return ((5*app.width/8 <= x <= 7*app.width/8) and
            (4*app.height/16 <= y <= 5*app.height/16))

# creates text trackers for financials
def drawStartAmounts(app, canvas):
    canvas.create_text(app.width/4, 3*app.height/16, text = 'Starting Amount: $', anchor = 'se', font = 'Arial 12 bold')
    canvas.create_text(app.width/4, 3*app.height/16, text = f'{app.startAmount}', anchor = 'sw', font = 'Arial 12 bold')
    canvas.create_text(app.width/4, 4*app.height/16, text = 'Account Value: $', anchor = 'se', font = 'Arial 12 bold')
    canvas.create_text(app.width/4, 4*app.height/16, text = f'{app.investing}', anchor = 'sw', font = 'Arial 12 bold')
    canvas.create_text(app.width/4, 5*app.height/16, text = 'Buying Power: $', anchor = 'se', font = 'Arial 12 bold')
    canvas.create_text(app.width/4, 5*app.height/16, text = f'{app.buyingPower}', anchor = 'sw', font = 'Arial 12 bold')

# main function for drawing the portfolio board on stock info page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawPortfolio(app, canvas):
    for row in range(app.portRows):
        for col in range(app.portCols):
            drawCellForPortTable(app, canvas, row, col)

# draws individual cells for portfolio board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForPortTable(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsForPortTable(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1)
    if app.portBoard[row][col] != None and app.portBoard[row][col] != 'None':
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.portBoard[row][col])

# gets width and height for cells for portfolio
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForPortTable(app):
    # helper function to determine column width and row height for portfolio list
    portWidth  = app.width - 2*app.portMargin
    portHeight = (2*app.height)/3 - app.portMargin
    columnWidth = portWidth / app.portCols
    rowHeight = portHeight / app.portRows
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for portfolio
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForPortTable(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForPortTable(app)
    x0 = app.portMargin + col * colW
    x1 = x0 + colW
    y0 = (app.height)/3 + row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# sees if click occurred in portfolio
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInPort(app, x, y):
    return ((app.portMargin <= x <= app.width - app.portMargin) and
            (app.height/3 <= y <= app.height - app.portMargin))

# returns the cell that was clicked in the portfolio
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getPortCell(app, x, y):
    colW, rowH = widthAndHeightForPortTable(app)
    row = int((y - app.height/3) / rowH)
    col = int((x - app.portMargin) / colW)
    return row, col

# main function for drawing the ticker board on stock info page
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawTickerScroll(app, canvas):
    for row in range(app.tickerRows):
        for col in range(app.tickerCols):
            drawCellForTickerScroll(app, canvas, row, col)

# draws individual cells for ticker board
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def drawCellForTickerScroll(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsForTickerScroll(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = app.tickerBoard[row][col])

# gets width and height for cells for ticker
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def widthAndHeightForTickerScroll(app):
    # helper function to determine column width and row height for ticker scroll
    tickerWidth  = app.width - 2*app.portMargin
    tickerHeight = app.height/8
    columnWidth = tickerWidth / app.tickerCols
    rowHeight = tickerHeight / app.tickerRows
    return (columnWidth, rowHeight)

# gets cell bounds for each cell for ticker
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBoundsForTickerScroll(app, row, col):
    # returns 2 diagonal points used to draw rectangle in grid
    colW, rowH = widthAndHeightForTickerScroll(app)
    x0 = app.portMargin + col * colW
    x1 = x0 + colW
    y0 = app.portMargin + row * rowH
    y1 = y0 + rowH
    return (x0, y0, x1, y1)

# sees if click occurred in ticker
# framework taken from the 15-112 Piazza website:
# https://piazza.com/class/ke208q10xpk75w?cid=3791
def clickInScroll(app, x, y):
    return ((app.portMargin <= x <= app.width - app.portMargin) and
            (app.portMargin <= y <= app.portMargin + app.height/8))

# returns the cell that was clicked in the ticker
# framework taken from the 15-112 course website animation notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getScrollCell(app, x, y):
    colW, rowH = widthAndHeightForTickerScroll(app)
    row = int((y - app.portMargin) / rowH)
    col = int((x - app.portMargin) / colW)
    return row, col

# returns a list of weekly stock returns over the past 2 years
def getReturns(ticker, data):
    returnsLst = []
    for i in range(len(data) - 1):
        current = data.iloc[i]['Adj Close'][ticker]
        future = data.iloc[i + 1]['Adj Close'][ticker]
        rateReturn = (future/current) - 1
        returnsLst.append(rateReturn)
    return returnsLst

# returns a list of weekly stock returns over the past 2 years (Note: this is when the data is only for one stock)
def getReturns2D(ticker, data):
    returnsLst = []
    for i in range(len(data) - 1):
        current = data.iloc[i]['Adj Close']
        future = data.iloc[i + 1]['Adj Close']
        rateReturn = (future/current) - 1
        returnsLst.append(rateReturn)
    return returnsLst

# returns the yearly expected return a stock is expected to earn in the future
def expectedReturn(ticker, data):
    returnsLst = getReturns(ticker, data)
    total = 0
    elems = 0
    for elem in returnsLst:
        if not math.isnan(elem):
            total += elem
            elems += 1
    annualized = (total/elems) * 52
    return annualized

# returns the yearly expected return a stock is expected to earn in the future (Note: this is when the data is only for one stock)
def expectedReturn2D(ticker, data):
    returnsLst = getReturns2D(ticker, data)
    total = 0
    elems = 0
    for elem in returnsLst:
        if not math.isnan(elem):
            total += elem
            elems += 1
    annualized = (total/elems) * 52
    return annualized

# returns the yearly expected return of all long stocks in a portfolio
def portfolioExpReturn(port, weights, data):
    annualReturn = 0
    for i in range(len(port)):
        annualReturn += weights[i] * expectedReturn(port[i], data)
    return annualReturn

# returns the yearly standard deviation (or volatility) of a stock
def getSTDEV(ticker, data):
    returnsLst = getReturns(ticker, data)
    stdev = statistics.pstdev(returnsLst)
    annualized = stdev * math.sqrt(52)
    return annualized

# returns the yearly standard deviation (or volatility) of a stock (Note: this is when the data is only for one stock)
def getSTDEV2D(ticker, data):
    returnsLst = getReturns2D(ticker, data)
    stdev = statistics.pstdev(returnsLst)
    annualized = stdev * math.sqrt(52)
    return annualized

# returns the yearly standard deviation (or volatility) for an entire portfolio
def portSTDEV(port, weights, data):
    portReturnsDict = {}
    minLength = None
    for ticker in port:
        returns = getReturns(ticker, data)
        portReturnsDict[ticker] = returns
        if minLength == None:
            minLength = len(returns)
        elif len(returns) < minLength:
            minLength = len(returns)
    for ticker in portReturnsDict:
        portReturnsDict[ticker] = portReturnsDict[ticker][:minLength]
    # use matrix multiplication on the weights and covariances of each stock to get variance
    # weights * covariance matrix * weights(transposed) 
    returnsDF = pd.DataFrame(portReturnsDict)
    covMatrix = returnsDF.cov()
    covArray = pd.DataFrame.to_numpy(covMatrix)
    weightsArray = np.array(weights)
    first = np.matmul(weightsArray, covArray)
    weeklyVariance = np.matmul(first, np.transpose(weightsArray))
    weeklySTDev = math.sqrt(weeklyVariance)
    yearlySTDev = weeklySTDev * math.sqrt(52)
    return yearlySTDev

# determines the Sharpe ratio of a portfolio
def portSharpeRatio(tickerLst, tickerWeights, data):
    portAverage = portfolioExpReturn(tickerLst, tickerWeights, data)
    portStd = portSTDEV(tickerLst, tickerWeights, data)
    riskFree = 0.01
    sharpe = (portAverage - riskFree)/portStd
    return sharpe

# max Sharpe ratio for a portfolio of 4 stocks
def maxSharpeRatio4(tickerLst):
    maxSharpe = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 1001, 125):
        for j in range(0, 1001-i, 125):
            for k in range(0, 1001-i-j, 125):
                for l in range(0, 1001-i-j-k, 125):
                    if almostEqual(i+j+k+l, 1000):
                        ratio = portSharpeRatio(tickerLst, [i/1000, j/1000, k/1000, l/1000], data)
                        if ratio > maxSharpe:
                            maxSharpe = ratio
                            maxWeights = [i/1000, j/1000, k/1000, l/1000]
    return maxWeights, maxSharpe

# max Sharpe ratio for a portfolio of 3 stocks
def maxSharpeRatio3(tickerLst):
    maxSharpe = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 11):
        for j in range(0, 11-i):
            for k in range(0, 11-i-j):
                if almostEqual(i+j+k, 10):
                    ratio = portSharpeRatio(tickerLst, [i/10, j/10, k/10], data)
                    if ratio > maxSharpe:
                        maxSharpe = ratio
                        maxWeights = [i/10, j/10, k/10]
    return maxWeights, maxSharpe

# max Sharpe ratio for a portfolio of 2 stocks
def maxSharpeRatio2(tickerLst):
    maxSharpe = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 26):
        for j in range(0, 26-i):
            if almostEqual(i+j, 25):
                ratio = portSharpeRatio(tickerLst, [i/25, j/25], data)
                if ratio > maxSharpe:
                    maxSharpe = ratio
                    maxWeights = [i/25, j/25]
    return maxWeights, maxSharpe

# gets the downside deviation of a portfolio of stocks
def portDownsideDeviation(port, weights, data):
    yrExp = portfolioExpReturn(port, weights, data)
    weekExp = yrExp/52
    riskFree = 0.01
    weeklyReturnsLst = []
    belowAvgLst = []
    for i in range(len(data) - 1):
        total = 0
        for j in range(len(port)):
            current = data.iloc[i]['Adj Close'][port[j]]
            future = data.iloc[i + 1]['Adj Close'][port[j]]
            if not math.isnan(current) and not math.isnan(future):
                total += weights[j] * ((future/current) - 1)
        weeklyReturnsLst.append(total)
    for elem in weeklyReturnsLst:
        riskPremium = elem - riskFree
        if riskPremium < weekExp:
            belowAvgLst.append(elem)
    downsideDeviation = statistics.pstdev(belowAvgLst)
    annualDDEV = downsideDeviation * math.sqrt(52)
    return annualDDEV

# returns the Sortino ratio of a portfolio
def portSortinoRatio(tickerLst, tickerWeights, data):
    portAverage = portfolioExpReturn(tickerLst, tickerWeights, data)
    portDDEV = portDownsideDeviation(tickerLst, tickerWeights, data)
    riskFree = 0.01
    sortino = (portAverage - riskFree)/portDDEV
    return sortino

# max Sortino ratio for a portfolio of 4 stocks
def maxSortinoRatio4(tickerLst):
    maxSortino = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 1001, 125):
        for j in range(0, 1001-i, 125):
            for k in range(0, 1001-i-j, 125):
                for l in range(0, 1001-i-j-k, 125):
                    if almostEqual(i+j+k+l, 1000):
                        ratio = portSortinoRatio(tickerLst, [i/1000, j/1000, k/1000, l/1000], data)
                        if ratio > maxSortino:
                            maxSortino = ratio
                            maxWeights = [i/1000, j/1000, k/1000, l/1000]
    return maxWeights, maxSortino

# max Sortino ratio for a portfolio of 3 stocks
def maxSortinoRatio3(tickerLst):
    maxSortino = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 11):
        for j in range(0, 11-i):
            for k in range(0, 11-i-j):
                if almostEqual(i+j+k, 10):
                    ratio = portSortinoRatio(tickerLst, [i/10, j/10, k/10], data)
                    if ratio > maxSortino:
                        maxSortino = ratio
                        maxWeights = [i/10, j/10, k/10]
    return maxWeights, maxSortino

# max Sortino ratio for a portfolio of 2 stocks
def maxSortinoRatio2(tickerLst):
    maxSortino = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 26):
        for j in range(0, 26-i):
            if almostEqual(i+j, 25):
                ratio = portSortinoRatio(tickerLst, [i/25, j/25], data)
                if ratio > maxSortino:
                    maxSortino = ratio
                    maxWeights = [i/25, j/25]
    return maxWeights, maxSortino

# calculates the portfolio beta
def portBeta(port, weights, data):
    totalBeta = 0
    for i in range(len(port)):
        tickerObject = yf.Ticker(port[1])
        stockBeta = tickerObject.info["beta"]
        weighted = stockBeta * weights[i]
        totalBeta += weighted
    return totalBeta

# calculates the portfolio Treynor ratio
def portTreynorRatio(tickerLst, tickerWeights, data):
    portAverage = portfolioExpReturn(tickerLst, tickerWeights, data)
    portfolioBeta = portBeta(tickerLst, tickerWeights, data)
    riskFree = 0.01
    treynor = (portAverage-riskFree)/portfolioBeta
    return treynor

# max Treynor ratio for a portfolio of 4 stocks
def maxTreynorRatio4(tickerLst):
    maxTreynor = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 101, 20):
        for j in range(0, 101-i, 20):
            for k in range(0, 101-i-j, 20):
                for l in range(0, 101-i-j-k, 20):
                    if almostEqual(i+j+k+l, 100):
                        ratio = portTreynorRatio(tickerLst, [i/100, j/100, k/100, l/100], data)
                        if ratio > maxTreynor:
                            maxTreynor = ratio
                            maxWeights = [i/100, j/100, k/100, l/100]
    return maxWeights, maxTreynor

# max Treynor ratio for a portfolio of 3 stocks
def maxTreynorRatio3(tickerLst):
    maxTreynor = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 1001, 125):
        for j in range(0, 1001-i, 125):
            for k in range(0, 1001-i-j, 125):
                if almostEqual(i+j+k, 125):
                    ratio = portTreynorRatio(tickerLst, [i/125, j/125, k/125], data)
                    if ratio > maxTreynor:
                        maxTreynor = ratio
                        maxWeights = [i/125, j/125, k/125]
    return maxWeights, maxTreynor

# max Treynor ratio for a portfolio of 2 stocks
def maxTreynorRatio2(tickerLst):
    maxTreynor = 0
    maxWeights = None
    data = yf.download(' '.join(tickerLst), period = "2y", interval = "1wk")
    for i in range(0, 11):
        for j in range(0, 11-i):
            if almostEqual(i+j, 10):
                ratio = portTreynorRatio(tickerLst, [i/10, j/10], data)
                if ratio > maxTreynor:
                    maxTreynor = ratio
                    maxWeights = [i/10, j/10]
    return maxWeights, maxTreynor

runApp(width = 800, height = 600)