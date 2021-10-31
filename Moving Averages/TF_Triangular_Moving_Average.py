
# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 100


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

my_data = ma(my_data, lookback, 3, 4)
my_data = ma(my_data, lookback, 4, 5)

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 5], label = '100-period Triangular Moving Average')
plt.legend()
