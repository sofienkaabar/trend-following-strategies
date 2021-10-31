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

# Calling the 13-period EMA
my_data = ema(my_data, 2, 13, 3, 4)

# Calling the MACD function using the default parameters
my_data = macd(my_data, 3, 26, 12, 9, 5)

# Removing the signal line as we do not need it in the Elder System
my_data = deleter(my_data, 6, 1)

def elder_system_plot(Data, window):
      
    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        if Chosen[i, 3] > Chosen[i, 4] and Chosen[i, 5] > 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'green', linewidth = 1)  
            
            plt.vlines(x = i, ymin = Chosen[i, 0], ymax = Chosen[i, 3], color = 'green', linewidth = 1)
            
            
        if Chosen[i, 3] < Chosen[i, 4] and Chosen[i, 5] < 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'red', linewidth = 1)  
            
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'red', linewidth = 1)  
            
        if Chosen[i, 3] < Chosen[i, 4] and Chosen[i, 5] > 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
            
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0] + 0.00001, color = 'black', linewidth = 1)
        
        if Chosen[i, 3] > Chosen[i, 4] and Chosen[i, 5] < 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
            
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0] + 0.00001, color = 'black', linewidth = 1)  
            
    plt.grid()
    
elder_system_plot(my_data, 250)    
