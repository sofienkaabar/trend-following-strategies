# Base Parameters
assets           = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

def signal(Data, close, psar_col, ma_col, buy, sell):
    
    Data = adder(Data, 10)
        
    for i in range(len(Data)):
            
        if Data[i, close] > Data[i, psar_col] and \
           Data[i, close] > Data[i, ma_col] and \
           Data[i - 1, close] < Data[i - 1, psar_col]:
               
               Data[i, buy] = 1

        if Data[i, close] < Data[i, psar_col] and \
           Data[i, close] < Data[i, ma_col] and \
           Data[i - 1, close] > Data[i - 1, psar_col]:
               
               Data[i, sell] = -1
               
    return Data

lookback = 50

def sar(s, af = 0.02, amax = 0.2):
    
    high, low = s.high, s.low

    # Starting values
    sig0, xpt0, af0 = True, high[0], af
    sar = [low[0] - (high - low).std()]

    for i in range(1, len(s)):
        sig1, xpt1, af1 = sig0, xpt0, af0

        lmin = min(low[i - 1], low[i])
        lmax = max(high[i - 1], high[i])

        if sig1:
            sig0 = low[i] > sar[-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high[i] >= sar[-1]
            xpt0 = min(lmin, xpt1)

        if sig0 == sig1:
            sari = sar[-1] + (xpt1 - sar[-1])*af1
            af0 = min(amax, af1 + af)

            if sig0:
                af0 = af0 if xpt0 > xpt1 else af1
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 < xpt1 else af1
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0

        sar.append(sari)

    return sar

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

my_data = pd.DataFrame(my_data)
my_data.columns = ['open','high','low','close']
Parabolic = sar(my_data, 0.02, 0.2)
Parabolic = np.array(Parabolic)
Parabolic = np.reshape(Parabolic, (-1, 1))
my_data = np.concatenate((my_data, Parabolic), axis = 1)
my_data = ma(my_data, lookback, 3, 5)
my_data = signal(my_data, 3, 4, 5, 6, 7)

# signal_chart_bars(my_data, 3, 6, 7, window = 500)
# plt.plot(my_data[-500:, 4], label = 'Parabolic SAR', linestyle = 'dashed')
# plt.plot(my_data[-500:, 5], label = '50-period Simple Moving Average')
# plt.legend()

# Variable Period Strategy
my_data = performance_variable_period(my_data, 3, 6, 7, 8, 9, 10)

# Fixed Period Strategy - Must Not be Used Directly After the Previous Performance Function
my_data = performance_fixed_period(my_data, 3, 6, 7, 15, 8, 9, 10)




