# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 60

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

def vertical_horizontal_indicator(Data, lookback, what, where):
    
    Data = adder(Data, 4)
    
    for i in range(len(Data)):
        
        Data[i, where] = Data[i, what] - Data[i - 1, what]
    
    Data = jump(Data, 1)    
       
    Data[:, where] = abs(Data[:, where])

    for i in range(len(Data)):
        
        Data[i, where + 1] = Data[i - lookback + 1:i + 1, where].sum()
    
    for i in range(len(Data)):
        
        try:
            
            Data[i, where + 2] = max(Data[i - lookback + 1:i + 1, what]) - min(Data[i - lookback + 1:i + 1, what])
            
        except ValueError:
            
            pass
        
    Data = jump(Data, lookback)    
    
    Data[:, where + 3] = Data[:, where + 2] / Data[:, where + 1]
    
    Data = deleter(Data, where, 3)
    
    return Data

my_data = vertical_horizontal_indicator(my_data, lookback, 3, 4)
my_data = ma(my_data, 60, 4, 5)

indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 250)
plt.plot(my_data[-250:, 5], color = 'orange')
