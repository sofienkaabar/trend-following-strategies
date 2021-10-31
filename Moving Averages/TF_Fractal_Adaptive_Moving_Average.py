# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 100

def fractal_dimension(Data, lookback, high, low, close, where):
    
    Data = adder(Data, 10)
    
    for i in range(len(Data)):
        
        try:
                
            # Calculating N1
            Data[i, where]     = max(Data[i - (2 * lookback):i - lookback, high])
            Data[i, where + 1] = min(Data[i - (2 * lookback):i - lookback, low])
            Data[i, where + 2] = (Data[i, where] - Data[i, where + 1]) / lookback
           
            # Calculating N2
            Data[i, where + 3] = max(Data[i - lookback:i, high])
            Data[i, where + 4] = min(Data[i - lookback:i, low])
            Data[i, where + 5] = (Data[i, where + 3] - Data[i, where + 4]) / lookback
            
            # Calculating N3
            Data[i, where + 6] = max(Data[i, where], Data[i, where + 3])
            Data[i, where + 7] = min(Data[i, where + 1], Data[i, where + 4])
            Data[i, where + 8] = (Data[i, where + 6] - Data[i, where + 7]) / (2 * lookback)
            
            # Calculating the Fractal Dimension Index
            if Data[i, where + 2] > 0 and Data[i, where + 5] > 0 and Data[i, where + 8] > 0:
                
                Data[i, where + 9] = (np.log(Data[i, where + 2] + Data[i, where + 5]) - np.log(Data[i, where + 8])) / np.log(2)
            
        except ValueError:
            pass
        
    # Cleaning
    Data = deleter(Data, where, 9) 
    Data = jump(Data, lookback * 2)
        
    return Data

# Calculating a 13-period Fractal Dimension Index
my_data = fractal_dimension(my_data, lookback, 1, 2, 3, 4)

# Adding a Few Columns
my_data = adder(my_data, 2)

# Calculating the alpha factor
for i in range(len(my_data)):
    
    my_data[i, 5] = np.exp(-4.6 * (my_data[i, 4] - 1))

# Calculating the First Value of FRAMA
my_data[1, 6] = (my_data[1, 5] * my_data[1, 3]) + ((1 - my_data[1, 5]) * my_data[0, 3])

# Calculating the Rest of FRAMA
for i in range(2, len(my_data)):
    
    try:
        my_data[i, 6] = (my_data[i, 5] * my_data[i, 3]) + ((1 - my_data[i, 5]) * my_data[i - 1, 6])
        
    except IndexError:
    
        pass

ohlc_plot_bars(my_data, 500)
plt.plot(my_data[-500:, 6], label = '100-period Fractal Adaptive Moving Average')
plt.legend()