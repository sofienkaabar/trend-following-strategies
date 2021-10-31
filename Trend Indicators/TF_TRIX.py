# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 5

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 20

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
   
def lwma(Data, lookback, what):
    
    weighted = []
    for i in range(len(Data)):
            try:
                total = np.arange(1, lookback + 1, 1)
                
                matrix = Data[i - lookback + 1: i + 1, what:what + 1]
                matrix = np.ndarray.flatten(matrix)
                matrix = total * matrix
                wma = (matrix.sum()) / (total.sum())
                weighted = np.append(weighted, wma)

            except ValueError:
                pass
    
    Data = Data[lookback - 1:, ]
    weighted = np.reshape(weighted, (-1, 1)) 
    Data = np.concatenate((Data, weighted), axis = 1)   
    
    return Data

def trix(Data, lookback, what, where):
    
    # First EMA
    Data = ema(Data, 2, lookback, what, where)
    Data = jump(Data, lookback)
    
    # Second EMA
    Data = ema(Data, 2, lookback, where, where + 1)
    Data = jump(Data, lookback)
       
    # Third EMA
    Data = ema(Data, 2, lookback, where + 1, where + 2)  
    Data = jump(Data, lookback)
    
    # TRIX
    Data = adder(Data, 1)
    for i in range(len(Data)):
        
        Data[i, where + 3] = (Data[i, where + 2] / Data[i - 1, where + 2]) - 1
   
    Data = deleter(Data, where, 3)
   
    return Data

my_data = trix(my_data, lookback, 3, 4)

indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 250)
plt.axhline(y = 0, color = 'black')
