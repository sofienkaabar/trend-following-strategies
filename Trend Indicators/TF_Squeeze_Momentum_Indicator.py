# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

boll_lookback = 60
kelt_lookback = 60
boll_vol      = 10
multiplier    = 20

# Mass imports 
my_data = mass_import(0, horizon)

def signal(Data):
    
    for i in range(len(Data)):   
        
       # Bullish Signal
       if Data[i, 9] == 0.001 and Data[i - 1, 9] != 0.001 and Data[i, 8] > 0:
           
                Data[i, 10] = 1 
                
       # Bearish Signal
       if Data[i, 9] == 0.001 and Data[i - 1, 9] != 0.001 and Data[i, 8] < 0: 
           
                Data[i, 11] = -1
       
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

def bollinger_bands(Data, boll_lookback, standard_distance, what, where):
       
    # Adding a few columns
    Data = adder(Data, 2)
    
    # Calculating means
    Data = ma(Data, boll_lookback, what, where)

    Data = volatility(Data, boll_lookback, what, where + 1)
    
    Data[:, where + 2] = Data[:, where] + (standard_distance * Data[:, where + 1])
    Data[:, where + 3] = Data[:, where] - (standard_distance * Data[:, where + 1])
    
    Data = jump(Data, boll_lookback)
    
    Data = deleter(Data, where, 2)
        
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

def keltner_channel(Data, ma_lookback, atr_lookback, multiplier, what, where):
    
    # Adding a few columns
    Data = adder(Data, 3)
    
    Data = ema(Data, 2, ma_lookback, what, where)
    
    Data = atr(Data, atr_lookback, 2, 1, 3, where + 1)
    
    Data[:, where + 2] = Data[:, where] + (Data[:, where + 1] * multiplier)
    Data[:, where + 3] = Data[:, where] - (Data[:, where + 1] * multiplier)

    Data = deleter(Data, where, 2)
    Data = jump(Data, ma_lookback)

    return Data

def squeeze(Data, boll_lookback, boll_vol, kelt_lookback, multiplier, close, where):
    
    # Adding a few columns
    Data = adder(Data, 10)
    
    # Adding Bollinger Bands
    Data = bollinger_bands(Data, boll_lookback, boll_vol, close, where)
    
    # Adding Keltner Channel
    Data = keltner_channel(Data, kelt_lookback, kelt_lookback, multiplier, close, where + 2)
    
    # Donchian Middle Point
    for i in range(len(Data)):
    
        try:
            
            Data[i, where + 4] = max(Data[i - boll_lookback + 1:i + 1, 1])
    
        except ValueError:
            
            pass

    for i in range(len(Data)):
    
        try:
            
            Data[i, where + 5] = min(Data[i - boll_lookback + 1:i + 1, 2])
    
        except ValueError:
            
            pass    

    Data[:, where + 6] = (Data[:, where + 4] + Data[:, where + 5]) / 2
    Data = deleter(Data, where + 4, 2)
    
    # Calculating Simple Moving Average on the Market
    Data = ma(Data, boll_lookback, close, where + 5)

    # Calculating Delta
    for i in range(len(Data)):
      
        Data[i, where + 6] = Data[i, close] - ((Data[i, where + 4] + Data[i, where + 5]) / 2)
    
    # Final Smoothing
    Data = ma(Data, boll_lookback, where + 6, where + 7)
    
    # Cleaning
    Data = deleter(Data, where + 4, 3)
    
    # Squeeze Detection
    for i in range(len(Data)):
        
        if Data[i, where] < Data[i, where + 2] and Data[i, where + 1] > Data[i, where + 3]:
            
            Data[i, where + 5] = 0.001
        
    return Data

def indicator_plot_squeeze(Data, window = 250):

    fig, ax = plt.subplots(2, figsize = (10, 5))

    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        ax[0].vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
   
    ax[0].grid() 

    for i in range(len(Chosen)):
        
        if Chosen[i, 8] > Chosen[i - 1, 8]:
            ax[1].vlines(x = i, ymin = 0, ymax = Chosen[i, 8], color = 'blue', linewidth = 1)  
        
        if Chosen[i, 8] < Chosen[i - 1, 8]:
            ax[1].vlines(x = i, ymin = Chosen[i, 8], ymax = 0, color = 'brown', linewidth = 1)  

        if Chosen[i, 8] == Chosen[i - 1, 8]:
            ax[1].vlines(x = i, ymin = Chosen[i, 8], ymax = 0, color = 'black', linewidth = 1)  
            
    ax[1].grid() 
    ax[1].axhline(y = 0, color = 'black', linewidth = 1.0, linestyle = '--')

    for i in range(len(Chosen)):
        
        if Chosen[i, 9] == 0.001:
            
            x = i
            y = Chosen[i, 8] + (-Chosen[i, 8])
        
            ax[1].annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 5, headlength = 3, headwidth = 3, facecolor = 'red', color = 'red'))
        
        elif Chosen[i, 9] == 0:
            
            x = i
            y = Chosen[i, 8] + (-Chosen[i, 8])
        
            ax[1].annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 5, headlength = 3, headwidth = 3, facecolor = 'green', color = 'green'))
       
        
my_data = squeeze(my_data, boll_lookback, boll_vol, kelt_lookback, multiplier, 3, 4)
    
indicator_plot_squeeze(my_data, window = 300)


