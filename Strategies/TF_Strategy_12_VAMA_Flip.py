# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, close, vama_col, distance, buy, sell):
    
    Data = adder(Data, 10)
    
    for i in range(len(Data)):
        
        if Data[i, close] > Data[i, vama_col] and Data[i - 1, close] < Data[i - 1, vama_col]:
            
            for a in range(i + 1, len(Data)):
                
                if Data[a, close] > Data[a, vama_col] + distance:
                    
                    Data[a, buy] = 1
                    
                    break
                
                elif Data[a, close] < Data[a, vama_col]:
                    
                    break
                
        elif Data[i, close] < Data[i, vama_col] and Data[i - 1, close] > Data[i - 1, vama_col]:
            
            for a in range(i + 1, len(Data)):
                
                if Data[a, close] < Data[a, vama_col] - distance:
                    
                    Data[a, sell] = -1
                    
                    break
                
                elif Data[a, close] > Data[a, vama_col]:
                    
                    break
                
    return Data

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

lookback_volatility_short = 3
lookback_volatility_long  = 233

my_data = volatility_adjusted_moving_average(my_data, lookback_volatility_short, lookback_volatility_long, 3, 4)
my_data = signal(my_data, 3, 4, 0.0020, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 1000)
# plt.plot(my_data[-1000:, 4])

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)
