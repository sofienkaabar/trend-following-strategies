# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, macd_col, buy, sell):
    
    Data = adder(Data, 10)
    
    for i in range(len(Data)):
        
        if Data[i, macd_col] > 0 and Data[i - 1, macd_col] < 0:
            
               Data[i, buy] = 1
               
        elif Data[i, macd_col] < 0 and Data[i - 1, macd_col] > 0:
            
               Data[i, sell] = -1
               
    return Data

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

def macd(Data, what, long_ema, short_ema, signal_ema, where):
    
    Data = adder(Data, 1)
    
    Data = ema(Data, 2, long_ema,  what, where)
    Data = ema(Data, 2, short_ema, what, where + 1)
    
    Data[:, where + 2] = Data[:, where + 1] - Data[:, where]

    Data = jump(Data, long_ema)
    Data = ema(Data, 2, signal_ema, where + 2, where + 3)
    
    Data = deleter(Data, where, 2)   
    Data = jump(Data, signal_ema)
    
    return Data

my_data = macd(my_data, 3, 26, 12, 9, 4)
my_data = signal(my_data, 4, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 500)

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)

