
# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

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

def fma(Data, where):
    
    # Adding Columns
    Data = adder(Data, 2)

    # Calculating Different Moving Averages
    Data = ema(Data, 2, 5,    1, where)    
    Data = ema(Data, 2, 8,    1, where + 1)    
    Data = ema(Data, 2, 13,   1, where + 2)    
    Data = ema(Data, 2, 21,   1, where + 3)    
    Data = ema(Data, 2, 34,   1, where + 4)    
    Data = ema(Data, 2, 55,   1, where + 5)    
    Data = ema(Data, 2, 89,   1, where + 6)    
    Data = ema(Data, 2, 144,  1, where + 7)    
    Data = ema(Data, 2, 233,  1, where + 8)    
    Data = ema(Data, 2, 377,  1, where + 9)    
    Data = ema(Data, 2, 610,  1, where + 10)    
    Data = ema(Data, 2, 987,  1, where + 11)    
    Data = ema(Data, 2, 1597, 1, where + 12) 
    Data = ema(Data, 2, 2584, 1, where + 13) 
    Data = ema(Data, 2, 4181, 1, where + 14) 

    # Calculating the High FMA
    Data[:, where + 15] = (Data[:, where]      + \
                          Data[:,  where + 1]  + \
                          Data[:,  where + 2]  + \
                          Data[:,  where + 3]  + \
                          Data[:,  where + 4]  + \
                          Data[:,  where + 5]  + \
                          Data[:,  where + 6]  + \
                          Data[:,  where + 7]  + \
                          Data[:,  where + 8]  + \
                          Data[:,  where + 9]  + \
                          Data[:,  where + 10] + \
                          Data[:,  where + 11] + \
                          Data[:,  where + 12] + \
                          Data[:,  where + 13] + \
                          Data[:,  where + 14]) / 15
    
    Data = deleter(Data, where, 15)
    
    # Calculating Different Moving Averages
    Data = ema(Data, 2, 5,    2, where + 1)    
    Data = ema(Data, 2, 8,    2, where + 2)    
    Data = ema(Data, 2, 13,   2, where + 3)    
    Data = ema(Data, 2, 21,   2, where + 4)    
    Data = ema(Data, 2, 34,   2, where + 5)    
    Data = ema(Data, 2, 55,   2, where + 6)    
    Data = ema(Data, 2, 89,   2, where + 7)    
    Data = ema(Data, 2, 144,  2, where + 8)    
    Data = ema(Data, 2, 233,  2, where + 9)    
    Data = ema(Data, 2, 377,  2, where + 10)    
    Data = ema(Data, 2, 610,  2, where + 11)    
    Data = ema(Data, 2, 987,  2, where + 12)    
    Data = ema(Data, 2, 1597, 2, where + 13) 
    Data = ema(Data, 2, 2584, 2, where + 14) 
    Data = ema(Data, 2, 4181, 2, where + 15) 

    # Calculating the High FMA
    Data[:, where + 16] = (Data[:, where + 1]  + \
                          Data[:,  where + 2]  + \
                          Data[:,  where + 3]  + \
                          Data[:,  where + 4]  + \
                          Data[:,  where + 5]  + \
                          Data[:,  where + 6]  + \
                          Data[:,  where + 7]  + \
                          Data[:,  where + 8]  + \
                          Data[:,  where + 9]  + \
                          Data[:,  where + 10] + \
                          Data[:,  where + 11] + \
                          Data[:,  where + 12] + \
                          Data[:,  where + 13] + \
                          Data[:,  where + 14] + \
                          Data[:,  where + 15]) / 15
    
    Data = deleter(Data, where + 1, 15)
    
    return Data

my_data = fma(my_data, 4)

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 4], label = 'Fibonacci Moving Average - High')
plt.plot(my_data[-500:, 5], label = 'Fibonacci Moving Average - Low')
plt.legend()
