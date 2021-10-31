# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def heikin_ashi(Data, opening, high, low, close, where):
    
    Data = adder(Data, 4)
    
    # Heiken-Ashi Open
    try:
        
        for i in range(len(Data)):
            Data[i, where] = (Data[i - 1, opening] + Data[i - 1, close]) / 2
            
    except:
        
        pass
    
    # Heiken-Ashi Close
    for i in range(len(Data)):
        Data[i, where + 3] = (Data[i, opening] + Data[i, high] + Data[i, low] + Data[i, close]) / 4
    
    # Heiken-Ashi High
    for i in range(len(Data)):    
        Data[i, where + 1] = max(Data[i, where], Data[i, where + 3], Data[i, high])    
    
    # Heiken-Ashi Low    
    for i in range(len(Data)):    
        Data[i, where + 2] = min(Data[i, where], Data[i, where + 3], Data[i, low])    
        
    # Cleaning
    Data = jump(Data, 1)
    
    return Data

def ohlc_plot_candles(Data, window):
      
    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        plt.vlines(x = i, ymin = Chosen[i, 6], ymax = Chosen[i, 5], color = 'black', linewidth = 1)  
        
        if Chosen[i, 7] > Chosen[i, 4]:
            
            plt.vlines(x = i, ymin = Chosen[i, 4], ymax = Chosen[i, 7], color = 'green', linewidth = 3)  

        if Chosen[i, 7] < Chosen[i, 4]:
            
            plt.vlines(x = i, ymin = Chosen[i, 7], ymax = Chosen[i, 4], color = 'red', linewidth = 3)  
            
        if Chosen[i, 7] == Chosen[i, 4]:
            
            plt.vlines(x = i, ymin = Chosen[i, 7], ymax = Chosen[i, 4] + 0.00001, color = 'black', linewidth = 6)  
            
    plt.grid()
    
my_data = heikin_ashi(my_data, 0, 1, 2, 3, 4)

ohlc_plot_candles(my_data, 100)
