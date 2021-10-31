# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def ichimoku(Data, close, high, low, kijun_lookback, 
             tenkan_lookback,
             chikou_lookback,
             senkou_span_projection,
             senkou_span_b_lookback,
             where):
    
    Data = adder(Data, 3)
    
    # Kijun-sen
    for i in range(len(Data)):
        try:
            Data[i, where] = max(Data[i - kijun_lookback:i + 1, high]) + min(Data[i - kijun_lookback:i + 1, low])
    
        except ValueError:
            pass
        
    Data[:, where] = Data[:, where] / 2
    
    # Tenkan-sen
    for i in range(len(Data)):
        try:
            Data[i, where + 1] = max(Data[i - tenkan_lookback:i + 1, high]) + min(Data[i - tenkan_lookback:i + 1, low])
    
        except ValueError:
            pass
        
    Data[:, where + 1] = Data[:, where + 1] / 2

    # Senkou-span A
    senkou_span_a = (Data[:, where] + Data[:, where + 1]) / 2
    senkou_span_a = np.reshape(senkou_span_a, (-1, 1))

    # Senkou-span B
    for i in range(len(Data)):
        try:
            Data[i, where + 2] = max(Data[i - senkou_span_b_lookback:i + 1, high]) + min(Data[i - senkou_span_b_lookback:i + 1, low])
    
        except ValueError:
            pass
    
    Data[:, where + 2] = Data[:, where + 2] / 2  
    senkou_span_b = Data[:, where + 2]
    senkou_span_b = np.reshape(senkou_span_b, (-1, 1))
    kumo = np.concatenate((senkou_span_a, senkou_span_b), axis = 1)
    
    Data = deleter(Data, where + 2, 1)
    
    # Creating the Cloud
    Data = np.concatenate((Data, kumo), axis = 1)
    Data = Data[senkou_span_b_lookback:, ]

    for i in range (1, 7):
        
        new_array = shift(Data[:, 0], -senkou_span_projection, cval = 0)
        new_array = np.reshape(new_array, (-1, 1))
        Data = np.concatenate((Data, new_array), axis = 1)
        Data = deleter(Data, 0, 1)

    kumo = Data[:, 0:2]
    Data = deleter(Data, 0, 2)
    Data = np.concatenate((Data, kumo), axis = 1)
    
    Data = adder(Data, 1)   
    
    for i in range(len(Data)):  
        try:   
            Data[i, 8] = Data[i + chikou_lookback, 3]
        except IndexError:
            pass
    
    Data[-senkou_span_projection:, 0] = Data[-senkou_span_projection:, 0] / 0
    Data[-senkou_span_projection:, 1] = Data[-senkou_span_projection:, 1] / 0
    Data[-senkou_span_projection:, 2] = Data[-senkou_span_projection:, 2] / 0
    Data[-senkou_span_projection:, 3] = Data[-senkou_span_projection:, 3] / 0
    Data[-senkou_span_projection:, 4] = Data[-senkou_span_projection:, 4] / 0
    Data[-senkou_span_projection:, 5] = Data[-senkou_span_projection:, 5] / 0
    Data[-52:, 8] = Data[-52:, 8] / 0
    
    return Data

my_data = ichimoku(my_data, 3, 1, 2, 26, 
             9,
             26,
             26,
             52,
             4)

ohlc_plot_bars(my_data, 250)
plt.plot(my_data[-250:, 4], label = 'Kijun-Sen', color = 'blue')
plt.plot(my_data[-250:, 5], label = 'Tenkan-Sen', color = 'red')
plt.plot(my_data[-250:, 6], label = 'Senkou-span A', color = 'purple')
plt.plot(my_data[-250:, 7], label = 'Senkou-span B', color = 'cornflowerblue')
plt.plot(my_data[-250:, 8], label = 'Chikou-span', color = 'green')
plt.legend()
