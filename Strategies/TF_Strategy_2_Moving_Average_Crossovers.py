# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, close, ma_short, ma_long, buy, sell):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i, ma_short] > Data[i, ma_long] and \
           Data[i - 1, ma_short] < Data[i - 1, ma_long]: 
               
               Data[i, buy] = 1

        if Data[i, ma_short] < Data[i, ma_long] and \
           Data[i - 1, ma_short] > Data[i - 1, ma_long]:
               
               Data[i, sell] = -1
               
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

lookback_short = 50
lookback_long  = 100

my_data = ma(my_data, lookback_short, 3, 4)
my_data = ma(my_data, lookback_long, 3, 5)
my_data = signal(my_data, 3, 4, 5, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 1000)
# plt.plot(my_data[-1000:, 4])
# plt.plot(my_data[-1000:, 5])

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)
