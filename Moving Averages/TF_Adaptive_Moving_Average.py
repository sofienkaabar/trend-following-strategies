# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 100

def kama(Data, what, where, lookback):
    
    Data = adder(Data, 10)
    
    # lookback from previous period
    for i in range(len(Data)):
        Data[i, where] = abs(Data[i, what] - Data[i - 1, what])
    
    Data[0, where] = 0
    
    # Sum of lookbacks
    for i in range(len(Data)):
        Data[i, where + 1] = (Data[i - lookback + 1:i + 1, where].sum())   
        
    # Volatility    
    for i in range(len(Data)):
        Data[i, where + 2] = abs(Data[i, what] - Data[i - lookback, what])
        
    Data = Data[lookback + 1:, ]
    
    # Efficiency Ratio
    Data[:, where + 3] = Data[:, where + 2] / Data[:, where + 1]
    
    for i in range(len(Data)):
        Data[i, where + 4] = np.square(Data[i, where + 3] * 0.6666666666666666667)
        
    for i in range(len(Data)):
        Data[i, where + 5] = Data[i - 1, where + 5] + (Data[i, where + 4] * (Data[i, what] - Data[i - 1, where + 5]))
        Data[11, where + 5] = 0
        
    Data = deleter(Data, where, 5)
    Data = jump(Data, lookback * 2)
    
    return Data

my_data = kama(my_data, 3, 4, lookback)

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 4], label = '100-period Adaptive Moving Average')
plt.legend()
