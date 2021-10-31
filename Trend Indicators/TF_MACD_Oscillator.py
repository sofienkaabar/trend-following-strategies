# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Parameters
long_ema   = 26
short_ema  = 12
signal_ema = 9

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

def indicator_plot_double_macd(Data, MACD_line, MACD_signal, window = 250):

    fig, ax = plt.subplots(2, figsize = (8, 5))

    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        ax[0].vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
   
    ax[0].grid() 

    for i in range(len(Chosen)):
        
        if Chosen[i, MACD_line] > 0:
            ax[1].vlines(x = i, ymin = 0, ymax = Chosen[i, MACD_line], color = 'green', linewidth = 1)  
        
        if Chosen[i, MACD_line] < 0:
            ax[1].vlines(x = i, ymin = Chosen[i, MACD_line], ymax = 0, color = 'red', linewidth = 1)  

        if Chosen[i, MACD_line] == 0:
            ax[1].vlines(x = i, ymin = Chosen[i, MACD_line], ymax = 0, color = 'black', linewidth = 1)  
            
    ax[1].grid() 
    ax[1].axhline(y = 0, color = 'black', linewidth = 0.5, linestyle = '--')
    
    ax[1].plot(Data[-window:, MACD_signal], color = 'blue', linewidth = 0.75, linestyle = 'dashed')
    
my_data = macd(my_data, 3, 26, 12, 9, 4)

indicator_plot_double_macd(my_data, 4, 5, window = 250)
