# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 100

def lwma(Data, lookback, what):
    
    weighted = []
    for i in range(len(Data)):
            try:
                total = np.arange(1, lookback + 1, 1)
                
                matrix = Data[i - lookback + 1: i + 1, what:what + 1]
                matrix = np.ndarray.flatten(matrix)
                matrix = total * matrix
                wma = (matrix.sum()) / (total.sum())
                weighted = np.append(weighted, wma)

            except ValueError:
                pass
    
    Data = Data[lookback - 1:, ]
    weighted = np.reshape(weighted, (-1, 1)) 
    Data = np.concatenate((Data, weighted), axis = 1)   
    
    return Data

my_data = lwma(my_data, lookback, 3)

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 4], label = '100-period Linear-Weighted Moving Average')
plt.legend()

