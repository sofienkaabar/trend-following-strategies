# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 13

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

def gri_index(Data, lookback, high, low, where):
    
    Data = adder(Data, 1)
    
    for i in range(len(Data)):
        
        try:
            
            Data[i, where] = abs(np.log(max(Data[i - lookback + 1:i + 1, high]) - min(Data[i - lookback + 1:i + 1, low])) / np.log(lookback))
            
        except ValueError:
            
            pass
        
    return Data

def ohlc_plot_candles(Data, window):
    
    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        if Chosen[i, 4] == Chosen[i - 1, 4]:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)
            
            plt.vlines(x = i, ymin = Chosen[i, 0], ymax = Chosen[i, 3], color = 'black', linewidth = 1.5) 
            
        if Chosen[i, 4] != Chosen[i - 1, 4] and Chosen[i, 3] > Chosen[i, 5]:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'green', linewidth = 1)
            
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'green', linewidth = 1.5)  
            
        if Chosen[i, 4] != Chosen[i - 1, 4] and Chosen[i, 3] < Chosen[i, 5]:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'red', linewidth = 1)
            
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'red', linewidth = 1.5) 
            
    plt.grid()

my_data = gri_index(my_data, lookback, 1, 2, 4)
my_data = ma(my_data, 30, 3, 5)

# indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 500)

ohlc_plot_candles(my_data, 250)
plt.plot(my_data[-250:, 5], label = '30-period Simple Moving Average')
plt.legend()


