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

def hull_moving_average(Data, what, lookback, where):
    
    Data = lwma(Data, lookback, what)
    
    second_lookback = round((lookback / 2), 1)
    second_lookback = int(second_lookback) 
    
    Data = lwma(Data, second_lookback, what)
    
    Data = adder(Data, 1)
    Data[:, where + 2] = ((2 * Data[:, where + 1]) - Data[:, where])

    third_lookback = round(np.sqrt(lookback), 1)
    third_lookback = int(third_lookback) 

    Data = lwma(Data, third_lookback, where + 2)
    Data = deleter(Data, where, 3)

    return Data

my_data = hull_moving_average(my_data, 3, lookback, 4)

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 4], label = '100-period Hull Moving Average')
plt.legend()