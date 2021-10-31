# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def fibonacci_range(Data, high, low, where):
   
    # Adding a few columns
    Data = adder(Data, 1)

    for i in range(len(Data)):
        
        if Data[i, high] > Data[i - 2, low] and \
           Data[i, high] > Data[i - 3, low] and \
           Data[i, high] > Data[i - 5, low] and \
           Data[i, high] > Data[i - 8, low] and \
           Data[i, high] > Data[i - 13, low]:
               
               Data[i, where] = 1

        elif Data[i, low] < Data[i - 2, high] and \
             Data[i, low] < Data[i - 3, high] and \
             Data[i, low] < Data[i - 5, high] and \
             Data[i, low] < Data[i - 8, high] and \
             Data[i, low] < Data[i - 13, high]:
                           
               Data[i, where] = -1

        else:
            
               Data[i, where] = 0
               
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

        if Chosen[i, 4] == 0:
            
            plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'black', linewidth = 1)
            
    plt.grid()
    
my_data = fibonacci_range(my_data, 1, 2, 4)
  
ohlc_plot_candles(my_data, 250)