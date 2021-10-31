# Base Parameters
assets = asset_list('FX') 

# Trading Parameters   
horizon = 'H1'
pair    = 0

# Mass Imports 
my_data = mass_import(pair, horizon)

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

# If you have an array
my_data = pd.DataFrame(my_data)

# Renaming the columns to fit the function
my_data.columns = ['open','high','low','close']

# Calculating the Parabolic SAR
Parabolic = sar(my_data, 0.02, 0.2)

# Converting the Parabolic values back to an array
Parabolic = np.array(Parabolic)

# Reshaping
Parabolic = np.reshape(Parabolic, (-1, 1))

# Concatenating with the OHLC Data
my_data = np.concatenate((my_data, Parabolic), axis = 1)

ohlc_plot_candles(my_data, 100)
plt.plot(my_data[-100:, 4], linestyle = 'dashed')
