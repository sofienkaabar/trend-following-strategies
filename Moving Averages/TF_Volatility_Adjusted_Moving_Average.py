# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback_volatility_short = 3
lookback_volatility_long  = 233

def volatility_adjusted_moving_average(Data, lookback_volatility_short, lookback_volatility_long, close, where):
    
    # Adding Columns
    Data = adder(Data, 2)
    
    # Calculating Standard Deviations
    Data = volatility(Data, lookback_volatility_short, close, where)
    Data = volatility(Data, lookback_volatility_long, close, where + 1)
    
    # Calculating Alpha
    for i in range(len(Data)):
        
        Data[i, where + 2] = 0.2 * (Data[i, where] / Data[i, where + 1])
   
    # Calculating the First Value of VIDYA
    Data[1, where + 3] = (Data[1, where + 2] * Data[1, close]) + ((1 - Data[1, where + 2]) * Data[0, close])
        
    # Calculating the Rest of VIDYA
    for i in range(2, len(Data)):
        
        Data[i, where + 3] = (Data[i, where + 2] * Data[i, close]) + ((1 - Data[i, where + 2]) * Data[i - 1, where + 3])

    # Cleaning
    Data = deleter(Data, where, 3) 
    Data = jump(Data, 1)
    
    return Data

my_data = volatility_adjusted_moving_average(my_data, lookback_volatility_short, lookback_volatility_long, 3, 4)

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 4], label = 'Volatility-Adjusted Moving Average')
plt.legend()