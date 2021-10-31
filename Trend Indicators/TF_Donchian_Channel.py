# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 20

def donchian(Data, low, high, lookback, where, median = 1):
    
    Data = adder(Data, 3)
    
    for i in range(len(Data)):
        
        try:
            
            Data[i, where] = max(Data[i - lookback:i + 1, high])
        
        except ValueError:
            
            pass
        
    for i in range(len(Data)):
        
        try:
            
            Data[i, where + 1] = min(Data[i - lookback:i + 1, low]) 
        
        except ValueError:
            
            pass
        
    if median == 1:
        
        for i in range(len(Data)): 
            
            try:
                
                Data[i, where + 2] = (Data[i, where] + Data[i, where + 1]) / 2 
            
            except ValueError:
                
                pass      
        
    Data = jump(Data, lookback)
    
    return Data

my_data = donchian(my_data, 2, 1, lookback, 4, median = 1)

ohlc_plot_candles(my_data, 100)
plt.plot(my_data[-100:, 4])
plt.plot(my_data[-100:, 5])
plt.plot(my_data[-100:, 6])
