# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, close, supertrend_col, buy, sell):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i, close] > Data[i, supertrend_col] and Data[i - 1, close] < Data[i - 1, supertrend_col]:
               
               Data[i, buy] = 1
            
        elif Data[i, close] < Data[i, supertrend_col] and Data[i - 1, close] > Data[i - 1, supertrend_col]:
                              
               Data[i, sell] = -1
                
    return Data

lookback = 10
multiplier = 4

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

def supertrend(Data, multiplier, atr_col, close, high, low, where):
    
    Data = adder(Data, 6)
    
    for i in range(len(Data)):
        
            # Average Price
            Data[i, where] = (Data[i, high] + Data[i, low]) / 2
            # Basic Upper Band
            Data[i, where + 1] = Data[i, where] + (multiplier * Data[i, atr_col])
            # Lower Upper Band
            Data[i, where + 2] = Data[i, where] - (multiplier * Data[i, atr_col])
    
    # Final Upper Band
    for i in range(len(Data)):
        
        if i == 0:
            Data[i, where + 3] = 0
            
        else:  
            if (Data[i, where + 1] < Data[i - 1, where + 3]) or (Data[i - 1, close] > Data[i - 1, where + 3]):
                Data[i, where + 3] = Data[i, where + 1]
            
            else:
                Data[i, where + 3] = Data[i - 1, where + 3]
    
    # Final Lower Band
    for i in range(len(Data)):
        
        if i == 0:
            Data[i, where + 4] = 0
            
        else:  
            if (Data[i, where + 2] > Data[i - 1, where + 4]) or (Data[i - 1, close] < Data[i - 1, where + 4]):
                Data[i, where + 4] = Data[i, where + 2]
            
            else:
                Data[i, where + 4] = Data[i - 1, where + 4]
      
    # SuperTrend
    for i in range(len(Data)):
        
        if i == 0:
            Data[i, where + 5] = 0
        
        elif (Data[i - 1, where + 5] == Data[i - 1, where + 3]) and (Data[i, close] <= Data[i, where + 3]):
            Data[i, where + 5] = Data[i, where + 3]
        
        elif (Data[i - 1, where + 5] == Data[i - 1, where + 3]) and (Data[i, close] >  Data[i, where + 3]):
            Data[i, where + 5] = Data[i, where + 4]
        
        elif (Data[i - 1, where + 5] == Data[i - 1, where + 4]) and (Data[i, close] >= Data[i, where + 4]):
            Data[i, where + 5] = Data[i, where + 4]
        
        elif (Data[i - 1, where + 5] == Data[i - 1, where + 4]) and (Data[i, close] <  Data[i, where + 4]):
            Data[i, where + 5] = Data[i, where + 3]   
            
    # Cleaning columns
    Data = deleter(Data, where, 5)        
    
    return Data

my_data = atr(my_data, lookback, 1, 2, 3, 4)
my_data = supertrend(my_data, multiplier, 4, 3, 1, 2, 5)
my_data = signal(my_data, 3, 5, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 1000)
# plt.plot(my_data[-1000:, 5])

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)
