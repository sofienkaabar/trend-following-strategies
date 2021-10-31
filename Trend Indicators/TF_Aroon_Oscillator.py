
# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 8

# Mass Imports 
my_data = mass_import(pair, horizon)

# Indicator Parameters
lookback = 25

def aroon(Data, period, close, where):
    
    # Adding Columns
    Data = adder(Data, 10)

    # Max Highs
    for i in range(len(Data)):
        
        try:
        
            Data[i, where] = max(Data[i - period + 1:i + 1, 1])
        
        except ValueError:
            
            pass
    # Max Lows
    for i in range(len(Data)):
        
        try:
       
            Data[i, where + 1] = min(Data[i - period + 1:i + 1, 2]) 
        
        except ValueError:
            
            pass
        
    # Where the High Equals the Highest High in the period
    for i in range(len(Data)):
       
        if Data[i, 1] == Data[i, where]:
            
            Data[i, where + 2] = 1
        
    # Where the Low Equals the Lowest Low in the period
    for i in range(len(Data)):
       
        if Data[i, 2] == Data[i, where + 1]:
            
            Data[i, where + 3] = 1

    # Jumping Rows
    Data = jump(Data, period)

    # Calculating Aroon Up
    for i in range(len(Data)):
        
        try:
        
            try:
                
                x = max(Data[i - period:i, 1])
                y = np.where(Data[i - period:i, 1] == x)
                y = np.array(y)
                distance = period - y
            
                Data[i - 1, where + 4] = 100 *((period - distance) / period)


            except ValueError:
                
                pass
            
        except IndexError:
            
            pass


    # Calculating Aroon Down
    for i in range(len(Data)):
        
        try:
        
            try:
                
                x = min(Data[i - period:i, 2])
                y = np.where(Data[i - period:i, 2] == x)
                y = np.array(y)
                distance = period - y
            
                Data[i - 1, where + 5] = 100 *((period - distance) / period)


            except ValueError:
                
                pass
            
        except IndexError:
            
            pass
    
    # Cleaning
    Data = deleter(Data, 4, 4)
    
    return Data    
    
my_data = aroon(my_data, lookback, 3, 4)

indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 500)
plt.plot(my_data[-500:, 5], color = 'orange', linewidth = 1)
