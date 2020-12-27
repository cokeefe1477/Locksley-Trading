PROJECT DESCRIPTION

    My term project is entitled "Locksley", which is a play on the popular stock 
    trading app Robinhood (the cartoon character Robinhood was born in Locksley).
    Like any stock trading app, Locksley users can trade stocks. The trading
    methods in Locksley include buying/selling stocks, shorting/returning stocks,
    and placing limit orders. Locksley users can trade in real-time thanks to 
    data from Yahoo Finance and see real-time profits. What sets Locksley apart from other 
    trading apps or brokerages is that users are able to see the expected return and 
    volatility of their portfolio, based on historical prices of the stocks in their 
    portfolio. The expected return and volatility trackers serve as a predictive mechanism
    since the rational trader prefers a higher return at lower risk. Another
    feature that sets Locksley apart is that users are able to optimize their
    portfolio. There are risk-return metrics that balance risk vs. return based
    on portfolios and the weights assigned to each individual stock in the 
    portfolio. Maximizing metrics such as the Sharpe ratio, Sortino ratio, and 
    Treynor ratio indicate the point on the efficient frontier that an investor
    should invest so as to efficiently balance the risk vs. return. Locksley
    users are able to select which ratio they think is best and apply the ratio
    maximizing weights to their portfolio.

HOW TO RUN THE PROJECT

    The main file the user should run is entitled "Locksley.py". This file 
    contains all the code for the portfolio and optimization techniques. The user
    should also keep the file entitled "Save_Port.txt" in the same directory as
    Locksley.py since that is the text file the user writes to (and reads from)
    when they save their portfolio for later use. Finally, the user should have
    the file entitled "cmu_112_graphics.py" in the same directory as "Locksley.py"
    since that is the main graphics framework through which the app runs.

LIBRARIES

    Users must first install the following modules before importing them: 
    yfinance, matplotlib, pandas, numpy. Users must import the following standard
    packages: math, copy, random, decimal, statistics. Users must also import
    the cmu_112_graphics.py file.

SHORTCUT COMMANDS

    Pressing 'r' on the intro page loads the most recent saved portfolio. Pressing
    's' on the main portfolio page saves the portfolio in the Save_Port.txt file
    that can be reloaded the next time the user opens the app.

OTHER COMMANDS

    Clicking on the ticker scroll pauses the scroll and prompts you to select "View
    Info", which will take you to the stock info page. On the stock info page, the
    numbers represent the number of shares you want to trade, and can be selected by
    clicking on them. Clicking on "Buy", "Short", or "Limit" performs that action. If
    you click "Limit", you must enter a price into the terminal. Clicking on "Optimize
    Portfolio" on the portfolio page takes you to a page with optimization choices. 
    Clicking "Sharpe", "Sortino", or "Treynor" calculates the portfolio weights to 
    maximize the selected ratio. Clicking "Apply" applies those weights to your portfolio.

