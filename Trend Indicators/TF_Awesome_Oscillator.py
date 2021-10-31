# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback_short_ma = 5
lookback_long_ma  = 34

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

def awesome_oscillator(Data, high, low, long_ma, short_ma, where):
    
    # Adding columns
    Data = adder(Data, 10)
    
    # Mid-point Calculation
    Data[:, where] = (Data[:, high] + Data[:, low]) / 2
    
    # Calculating the short-term Simple Moving Average
    Data = ma(Data, short_ma, where, where + 1)
    
    # Calculating the long-term Simple Moving Average
    Data = ma(Data, long_ma, where, where + 2)
    
    # Calculating the Awesome Oscillator
    Data[:, where + 3] = Data[:, where + 1] - Data[:, where + 2]

    # Removing Excess Columns/Rows
    Data = jump(Data, long_ma)  
    Data = deleter(Data, where, 3)   
    
    return Data

def indicator_plot_double_awesome(Data, indicator, window = 250):
    
  fig, ax = plt.subplots(2, figsize = (10, 5))
  Chosen = Data[-window:, ]
    
  for i in range(len(Chosen)):
        
    ax[0].vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
   
  ax[0].grid()
    
  for i in range(len(Chosen)):
        
      if Chosen[i, indicator] > Chosen[i - 1, indicator]:
          ax[1].vlines(x = i, ymin = 0, ymax = Chosen[i, indicator], color = 'green', linewidth = 1)  
        
      if Chosen[i, indicator] < Chosen[i - 1, indicator]:
          ax[1].vlines(x = i, ymin = Chosen[i, indicator], ymax = 0, color = 'red', linewidth = 1)  
            
  ax[1].grid() 
  ax[1].axhline(y = 0, color = 'black', linewidth = 0.5)

my_data = awesome_oscillator(my_data, 1, 2, lookback_long_ma, lookback_short_ma, 4)

indicator_plot_double_awesome(my_data, 4, window = 250)
