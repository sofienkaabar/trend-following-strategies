# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, ma_slope_col, buy, sell):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i, ma_slope_col] > 0 and Data[i - 1, ma_slope_col] < 0:
               
               Data[i, buy] = 1
            
        elif Data[i, ma_slope_col] < 0 and Data[i - 1, ma_slope_col] > 0:
                              
               Data[i, sell] = -1
                
    return Data

lookback = 20

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

def slope_indicator(Data, lookback, what, where):
        
    Data = adder(Data, 1)
    
    for i in range(len(Data)):
        Data[i, where] = (Data[i, what] - Data[i - lookback, what]) / lookback
        
    Data = jump(Data, lookback)
    
    return Data 

my_data = ma(my_data, lookback, 3, 4)
my_data = slope_indicator(my_data, lookback, 4, 5)
my_data = signal(my_data, 5, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 500)
# plt.plot(my_data[-500:, 4])

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)
