# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def hidden_divergence(Data, indicator, lower_barrier, upper_barrier, width):
    
    Data = adder(Data, 10)
    
    for i in range(len(Data)):
        
        try:
            if Data[i, indicator] < lower_barrier and Data[i - 1, indicator] > lower_barrier:
                
                for a in range(i + 1, i + width):
                    
                    # First trough
                    if Data[a, indicator] > lower_barrier:
                        
                        for r in range(a + 1, a + width):
                            
                            if Data[r, indicator] < lower_barrier and \
                            Data[r, indicator] < Data[i, indicator] and Data[r, 3] > Data[i, 3]:
                                
                                for s in range(r + 1, r + width):
                                    
                                    # Second trough
                                    if Data[s, indicator] > lower_barrier:
                                        Data[s, 6] = 1
                                        break
                                    
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
                    
        except IndexError:
            pass
        
    for i in range(len(Data)):
        
        try:
            if Data[i, indicator] > upper_barrier  and Data[i - 1, indicator] < upper_barrier:
                
                for a in range(i + 1, i + width):
                    
                    # First trough
                    if Data[a, indicator] < upper_barrier:
                        for r in range(a + 1, a + width):
                            if Data[r, indicator] > upper_barrier and \
                            Data[r, indicator] > Data[i, indicator] and Data[r, 3] < Data[i, 3]:
                                for s in range(r + 1, r + width):
                                    
                                    # Second trough
                                    if Data[s, indicator] < upper_barrier:
                                        Data[s, 7] = -1
                                        break
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
        except IndexError:
            pass 
        
    return Data

lookback = 14

def stochastic(Data, lookback, high, low, close, where, genre = 'High-Low'):
        
    # Adding a column
    Data = adder(Data, 1)
    
    if genre == 'High-Low':
        
        for i in range(len(Data)):
            
            try:
                Data[i, where] = (Data[i, close] - min(Data[i - lookback + 1:i + 1, low])) / (max(Data[i - lookback + 1:i + 1, high]) - min(Data[i - lookback + 1:i + 1, low]))
            
            except ValueError:
                pass
            
    if genre == 'Normalization':
        
        for i in range(len(Data)):
            
            try:
                Data[i, where] = (Data[i, close] - min(Data[i - lookback + 1:i + 1, close])) / (max(Data[i - lookback + 1:i + 1, close]) - min(Data[i - lookback + 1:i + 1, close]))
            
            except ValueError:
                pass
            
    Data[:, where] = Data[:, where] * 100  
    Data = jump(Data, lookback)

    return Data 

my_data = stochastic(my_data, lookback, 1, 2, 3, 4)
my_data = hidden_divergence(my_data, 4, 20, 70, 30)

# indicator_plot_double(my_data, 0, 1, 2, 3, 4, window = 300)
# signal_chart_bars(my_data, 3, 6, 7, window = 300)

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)

