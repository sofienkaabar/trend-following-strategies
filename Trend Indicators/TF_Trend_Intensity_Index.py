# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 10

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

def trend_intensity_indicator(Data, lookback, what, where):

    Data = adder(Data, 5)
    
    # Calculating the Moving Average
    Data = ma(Data, lookback, what, where)

    # Deviations
    for i in range(len(Data)):
        
        if Data[i, what] > Data[i, where]:
            Data[i, where + 1] = Data[i, what] - Data[i, where]
        
        if Data[i, what] < Data[i, where]:
            Data[i, where + 2] = Data[i, where] - Data[i, what]
              
    # Trend Intensity Index
    for i in range(len(Data)):
            
        Data[i, where + 3] = np.count_nonzero(Data[i - lookback + 1:i + 1, where + 1])
            
    for i in range(len(Data)):
            
        Data[i, where + 4] = np.count_nonzero(Data[i - lookback + 1:i + 1, where + 2])
        
    for i in range(len(Data)):
        
        Data[i, where + 5] = ((Data[i, where + 3]) / (Data[i, where + 3] + Data[i, where + 4])) * 100
        
    Data = deleter(Data, where, 5)
     
    return Data

my_data = trend_intensity_indicator(my_data, lookback, 3, 4)

indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 250)
