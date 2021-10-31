# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, high, low, close, psychological_signal, ma_col, buy, sell):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i, psychological_signal] == 1 and \
           Data[i, high] > Data[i, ma_col] and \
           Data[i - 1, close] > Data[i, close]:
               
               Data[i, buy] = 1

        if Data[i, psychological_signal] == 1 and \
           Data[i, low] < Data[i, ma_col] and \
           Data[i - 1, close] < Data[i, close]:
               
               Data[i, sell] = -1
               
    return Data

lookback = 100

def psychological_levels_scanner(Data, close, where):
    
    # Adding buy and sell columns
    Data = adder(Data, 10)
    
    # Rounding for ease of use
    Data = rounding(Data, 4)
    
    # Threshold
    level     = 0
    
    # Scanning for Psychological Levels
    for i in range(len(Data)):
        
        for i in range(len(Data)):
            
            if Data[i, close] == level:
                    
                Data[i, where] = 1
                
        level = round(level + 0.01, 2)
        if level > 5:
            break
    
    return Data

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

my_data = psychological_levels_scanner(my_data, 3, 4)
my_data = ma(my_data, lookback, 3, 5)
my_data = signal(my_data, 1, 2, 3, 4, 5, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 1000)
# plt.plot(my_data[-1000:, 5], label = '100-period Simple Moving Average')
# plt.legend()

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)


