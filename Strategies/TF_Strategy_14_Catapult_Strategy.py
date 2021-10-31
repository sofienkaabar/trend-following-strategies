# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, rvi_col, signal):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i,     rvi_col] < 30 and \
           Data[i - 1, rvi_col] > 30 and \
           Data[i - 2, rvi_col] > 30 and \
           Data[i - 3, rvi_col] > 30 and \
           Data[i - 4, rvi_col] > 30 and \
           Data[i - 5, rvi_col] > 30:
               
               Data[i, signal] = 1
                           
    return Data

lookback_rvi = 21
lookback_rsi = 14
lookback_ma  = 200

def ma(Data, lookback, close, where): 
    
    Data = adder(Data, 1)
    
    for i in range(len(Data)):
           
            try:
                Data[i, where] = (Data[i - lookback + 1:i + 1, close].mean())
            
            except IndexError:
                pass
            
    # Cleaning
    Data = jump(Data, lookback)
    
    return Data

def ema(Data, alpha, lookback, what, where):
    
    alpha = alpha / (lookback + 1.0)
    beta  = 1 - alpha
    
    # First value is a simple SMA
    Data = ma(Data, lookback, what, where)
    
    # Calculating first EMA
    Data[lookback + 1, where] = (Data[lookback + 1, what] * alpha) + (Data[lookback, where] * beta)

    # Calculating the rest of EMA
    for i in range(lookback + 2, len(Data)):
            try:
                Data[i, where] = (Data[i, what] * alpha) + (Data[i - 1, where] * beta)
        
            except IndexError:
                pass
            
    return Data 

def rsi(Data, lookback, close, where, width = 1, genre = 'Smoothed'):
    
    # Adding a few columns
    Data = adder(Data, 5)
    
    # Calculating Differences
    for i in range(len(Data)):
        
        Data[i, where] = Data[i, close] - Data[i - width, close]
     
    # Calculating the Up and Down absolute values
    for i in range(len(Data)):
        
        if Data[i, where] > 0:
            
            Data[i, where + 1] = Data[i, where]
            
        elif Data[i, where] < 0:
            
            Data[i, where + 2] = abs(Data[i, where])
            
    # Calculating the Smoothed Moving Average on Up and Down absolute values    
    lookback = (lookback * 2) - 1 # From exponential to smoothed
    Data = ema(Data, 2, lookback, where + 1, where + 3)
    Data = ema(Data, 2, lookback, where + 2, where + 4)

    # Calculating the Relative Strength
    Data[:, where + 5] = Data[:, where + 3] / Data[:, where + 4]
    
    # Calculate the Relative Strength Index
    Data[:, where + 6] = (100 - (100 / (1 + Data[:, where + 5])))

    # Cleaning
    Data = deleter(Data, where, 6)
    Data = jump(Data, lookback)

    return Data

def relative_volatility_index(Data, lookback, close, where):

    # Calculating Volatility
    Data = volatility(Data, lookback, close, where)
    
    # Calculating the RSI on Volatility
    Data = rsi(Data, lookback, where, where + 1) 
    
    # Cleaning
    Data = deleter(Data, where, 1)
    
    return Data

my_data = ma(my_data, lookback_ma, 3, 4)
my_data = rsi(my_data, lookback_rsi, 3, 5)
my_data = relative_volatility_index(my_data, lookback_rvi, 3, 6)
my_data = signal(my_data, 6, 7)

def trading_signal(Data, close, signal, rsi_col, ma_col, buy, sell):
    
    for i in range(len(Data)):
        
        if Data[i, signal] == 1 and Data[i, rsi_col] > 50 and Data[i, close] > Data[i, ma_col]:
            
            Data[i, buy] = 1

        if Data[i, signal] == 1 and Data[i, rsi_col] < 50 and Data[i, close] < Data[i, ma_col]:
            
            Data[i, sell] = -1
            
    return Data

my_data = trading_signal(my_data, 3, 7, 5, 4, 8, 9)
my_data = deleter(my_data, 4, 2)

# signal_chart_bars(my_data, 3, 6, 7, window = 1000)

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)
