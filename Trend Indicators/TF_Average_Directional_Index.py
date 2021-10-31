
# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 14

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

def atr(Data, lookback, high, low, close, where, genre = 'Smoothed'):
    
    # Adding the required columns
    Data = adder(Data, 2)
    
    # True Range Calculation
    for i in range(len(Data)):
        
        try:
            
            Data[i, where] =   max(Data[i, high] - Data[i, low],
                               abs(Data[i, high] - Data[i - 1, close]),
                               abs(Data[i, low]  - Data[i - 1, close]))
            
        except ValueError:
            pass
        
    Data[0, where] = 0   
           
    # Average True Range Calculation
    Data = ema(Data, 2, (lookback * 2) - 1, where, where + 1)
    
    # Cleaning
    Data = deleter(Data, where, 1)
    Data = jump(Data, lookback)

    return Data

def adx(Data, high, low, close, lookback, where):

    # Adding a few columns
    Data = adder(Data, 10)
    
    # DM+
    for i in range(len(Data)):
        
        if (Data[i, high] - Data[i - 1, high]) > (Data[i - 1, low] - Data[i, low]):
            
            Data[i, where] = Data[i, high] - Data[i - 1, high]
            
        else:
            Data[i, where] = 0
        
    # DM-
    for i in range(len(Data)):
        
        if (Data[i, high] - Data[i - 1, high]) < (Data[i - 1, low] - Data[i, low]):
            
            Data[i, where + 1] = Data[i - 1, low] - Data[i, low]
            
        else:
            
            Data[i, where + 1] = 0
        
    # Smoothing DI+   
    Data = ema(Data, 2, (lookback * 2 - 1), where, where + 2)
    
    # Smoothing DI-
    Data = ema(Data, 2, (lookback * 2 - 1), where + 1, where + 3)
    
    # Smoothing ATR
    Data = atr(Data, (lookback * 2 - 1), high, low, close, where + 4)
    
    Data = jump(Data, lookback)
    
    # DI+
    Data[:, where + 5] = Data[:, where + 2] / Data[:, where + 4]
    
    # DI-
    Data[:, where + 6] = Data[:, where + 3] / Data[:, where + 4]
    
    # ADX
    for i in range(len(Data)):
        Data[i, where + 7] = abs(Data[i, where + 5] - Data[i, where + 6]) / abs(Data[i, where + 5] + Data[i, where + 6]) * 100
    
    Data = ema(Data, 2, (lookback * 2 - 1), where + 7, where + 8)

    Data = jump(Data, lookback)

    Data = deleter(Data, where, 5)    
    
    return Data

my_data = adx(my_data, 1, 2, 3, lookback, 4)

indicator_plot_double(my_data, 0, 1, 2, 3, 7, window = 500)
plt.plot(my_data[-500:, 4] * 100, color = 'orange', linewidth = 1)
plt.plot(my_data[-500:, 5] * 100, color = 'red', linewidth = 1)
