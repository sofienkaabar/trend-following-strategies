# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, close, tii_col, ma_col, buy, sell):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i, tii_col] > 60 and \
           Data[i - 1, tii_col] < 60 and \
           Data[i, close] > Data[i, ma_col]:
               
               Data[i, buy] = 1

        if Data[i, tii_col] < 40 and \
           Data[i - 1, tii_col] > 40 and \
           Data[i, close] < Data[i, ma_col]:
               
               Data[i, sell] = -1
               
    return Data

lookback_ma  = 100
lookback_tii = 14

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

def trend_intensity_indicator(Data, lookback, what, where):

    Data = adder(Data, 5)
    
    # Calculating the Moving Average
    Data = ma(Data, lookback, what, where)

    # Deviations
    for i in range(len(Data)):
        
        if Data[i, what] > Data[i, where]:
            Data[i, where + 1] = Data[i, what] - Data[i, where]
        
        if Data[i, what] < Data[i, where]:
            Data[i, where + 2] = Data[i, where] - Data[i, what]
            
        
    # Trend Intensity Index
    for i in range(len(Data)):
            
        Data[i, where + 3] = np.count_nonzero(Data[i - lookback + 1:i + 1, where + 1])
            
    for i in range(len(Data)):
            
        Data[i, where + 4] = np.count_nonzero(Data[i - lookback + 1:i + 1, where + 2])
        
    for i in range(len(Data)):
        
        Data[i, where + 5] = ((Data[i, where + 3]) / (Data[i, where + 3] + Data[i, where + 4])) * 100
        
    Data = deleter(Data, where, 5)
     
    return Data

my_data = trend_intensity_indicator(my_data, lookback_tii, 3, 4)
my_data = ma(my_data, lookback_ma, 3, 5)
my_data = signal(my_data, 3, 4, 5, 6, 7)

# indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 250)
# signal_chart_bars(my_data, 3, 6, 7, window = 1000)
# plt.plot(my_data[-1000:, 5], label = '100-period Simple Moving Average')
# plt.legend()

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)

