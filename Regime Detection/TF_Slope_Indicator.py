# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

lookback = 20

def slope_indicator(Data, lookback, what, where):
        
    Data = adder(Data, 1)
    
    for i in range(len(Data)):
        
        Data[i, where] = (Data[i, what] - Data[i - lookback, what]) / lookback
        
    Data = jump(Data, lookback)
    
    return Data 

def ohlc_plot_candles(Data, window):
      
    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        if Chosen[i, 4] > 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'green', linewidth = 1)
            
            plt.vlines(x = i, ymin = Chosen[i, 0], ymax = Chosen[i, 3], color = 'green', linewidth = 1) 
            
        if Chosen[i, 4] < 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'red', linewidth = 1)
            
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'red', linewidth = 1)  
            
    plt.grid()
    
my_data = slope_indicator(my_data, lookback, 3, 4)

ohlc_plot_candles(my_data, 250)

# indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 500)
# plt.axhline(y = 0, color = 'black', linestyle = 'dashed', linewidth = 1)
