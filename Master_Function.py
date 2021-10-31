import datetime
import pytz
import pandas                    as pd
import MetaTrader5               as mt5
import matplotlib.pyplot         as plt
import numpy                     as np
import statistics                as stats

frame_MIN1 = mt5.TIMEFRAME_M1
frame_M5   = mt5.TIMEFRAME_M5
frame_M10  = mt5.TIMEFRAME_M10
frame_M15  = mt5.TIMEFRAME_M15
frame_M20  = mt5.TIMEFRAME_M20
frame_M30  = mt5.TIMEFRAME_M30
frame_H1   = mt5.TIMEFRAME_H1
frame_H2   = mt5.TIMEFRAME_H2
frame_H3   = mt5.TIMEFRAME_H3
frame_H4   = mt5.TIMEFRAME_H4
frame_D1   = mt5.TIMEFRAME_D1
frame_W1   = mt5.TIMEFRAME_W1
frame_M1   = mt5.TIMEFRAME_MN1

now = datetime.datetime.now()

def asset_list(asset_set):
   
    if asset_set == 'FX':
        
        assets = ['EURUSD', 'USDCHF', 'GBPUSD', 'AUDUSD', 'NZDUSD',
                  'USDCAD', 'EURCAD', 'EURGBP', 'EURCHF', 'AUDCAD',
                  'USDJPY', 'NZDCHF', 'NZDCAD', 'EURAUD','AUDNZD',
                  'GBPCAD', 'AUDCHF', 'GBPAUD', 'GBPCHF', 'GBPNZD']
       
    elif asset_set == 'CRYPTO':
        
        assets = ['BTCUSD', 'ETHUSD', 'XRPUSD', 'LTCUSD']
       
    elif asset_set == 'COMMODITIES':
        
        assets = ['XAUUSD', 'XAGUSD', 'XPTUSD', 'XPDUSD']    
       
    return assets

def mass_import(asset, horizon):
    
    if horizon == 'MN1':
        data = get_quotes(frame_MIN1, 2021, 8, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)    
    
    if horizon == 'M5':
        data = get_quotes(frame_M5, 2021, 6, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)

    if horizon == 'M10':
        data = get_quotes(frame_M10, 2021, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)
        
    if horizon == 'M15':
        data = get_quotes(frame_M15, 2021, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)
        
    if horizon == 'M30':
        data = get_quotes(frame_M30, 2016, 8, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)   
        
    if horizon == 'M20':
        data = get_quotes(frame_M20, 2018, 8, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)           
        
    if horizon == 'H1':
        data = get_quotes(frame_H1, 2011, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
        
    if horizon == 'H2':
        data = get_quotes(frame_H2, 2010, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
        
    if horizon == 'H3':
        data = get_quotes(frame_H3, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
        
    if horizon == 'H4':
        data = get_quotes(frame_H4, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
        
    if horizon == 'H6':
        data = get_quotes(frame_H6, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)            
        
    if horizon == 'D1':
        data = get_quotes(frame_D1, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
           
    if horizon == 'W1':
        data = get_quotes(frame_W1, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        
         
    if horizon == 'M1':
        data = get_quotes(frame_M1, 2000, 1, 1, asset = assets[asset])
        data = data.iloc[:, 1:5].values
        data = data.round(decimals = 5)        

    return data 

def get_quotes(time_frame, year = 2005, month = 1, day = 1, asset = "EURUSD"):
        
    # Establish connection to MetaTrader 5 
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    
    timezone = pytz.timezone("Europe/Paris")
    
    utc_from = datetime.datetime(year, month, day, tzinfo = timezone)
    utc_to = datetime.datetime(now.year, now.month, now.day, tzinfo = timezone)
    
    rates = mt5.copy_rates_range(asset, time_frame, utc_from, utc_to)
    
    rates_frame = pd.DataFrame(rates)

    return rates_frame

def adder(Data, times):
    
    for i in range(1, times + 1):
    
        new = np.zeros((len(Data), 1), dtype = float)
        Data = np.append(Data, new, axis = 1)

    return Data

def deleter(Data, index, times):
    
    for i in range(1, times + 1):
    
        Data = np.delete(Data, index, axis = 1)

    return Data
   
def jump(Data, jump):
    
    Data = Data[jump:, ]
    
    return Data

def rounding(Data, how_far):
    
    Data = Data.round(decimals = how_far)
    
    return Data

def volatility(Data, lookback, what, where):
    
    # Adding an extra column
    Data = adder(Data, 1)
    
    for i in range(len(Data)):
        
        try:
            Data[i, where] = (Data[i - lookback + 1:i + 1, what].std())
    
        except IndexError:
            pass
     
    # Cleaning
    Data = jump(Data, lookback)    
     
    return Data

def ohlc_plot_bars(Data, window):
     
    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
        plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)
        
        if Chosen[i, 3] > Chosen[i, 0]:
            plt.vlines(x = i, ymin = Chosen[i, 0], ymax = Chosen[i, 3], color = 'black', linewidth = 1.00)  

        if Chosen[i, 3] < Chosen[i, 0]:
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'black', linewidth = 1.00)  
            
        if Chosen[i, 3] == Chosen[i, 0]:
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'black', linewidth = 1.00)  
            
    plt.grid() 
    
def ohlc_plot_candles(Data, window):
      
    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        plt.vlines(x = i, ymin = Chosen[i, 2], ymax = Chosen[i, 1], color = 'black', linewidth = 1)  
        
        if Chosen[i, 3] > Chosen[i, 0]:
            plt.vlines(x = i, ymin = Chosen[i, 0], ymax = Chosen[i, 3], color = 'green', linewidth = 3)  

        if Chosen[i, 3] < Chosen[i, 0]:
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0], color = 'red', linewidth = 3)  
            
        if Chosen[i, 3] == Chosen[i, 0]:
            plt.vlines(x = i, ymin = Chosen[i, 3], ymax = Chosen[i, 0] + 0.00001, color = 'black', linewidth = 6)  
            
    plt.grid()

def signal_chart(Data, close, what_bull, what_bear, window = 500):   
     
    Plottable = Data[-window:, ]
    
    fig, ax = plt.subplots(figsize = (10, 5))
    
    ohlc_plot_candles(Data, window)    

    for i in range(len(Plottable)):
        
        if Plottable[i, what_bull] == 1:
            
            x = i
            y = Plottable[i, close]
        
            ax.annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = 11, headwidth = 11, facecolor = 'green', color = 'green'))
        
        elif Plottable[i, what_bear] == -1:
            
            x = i
            y = Plottable[i, close]
        
            ax.annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = -11, headwidth = -11, facecolor = 'red', color = 'red'))

def indicator_plot_double(Data, opening, high, low, close, second_panel, window = 250):

    fig, ax = plt.subplots(2, figsize = (10, 5))

    Chosen = Data[-window:, ]
    
    for i in range(len(Chosen)):
        
        ax[0].vlines(x = i, ymin = Chosen[i, low], ymax = Chosen[i, high], color = 'black', linewidth = 1)  
        
        if Chosen[i, close] > Chosen[i, opening]:
            color_chosen = 'green'
            ax[0].vlines(x = i, ymin = Chosen[i, opening], ymax = Chosen[i, close], color = color_chosen, linewidth = 2)  

        if Chosen[i, close] < Chosen[i, opening]:
            color_chosen = 'red'
            ax[0].vlines(x = i, ymin = Chosen[i, close], ymax = Chosen[i, opening], color = color_chosen, linewidth = 2)  
            
        if Chosen[i, close] == Chosen[i, opening]:
            color_chosen = 'black'
            ax[0].vlines(x = i, ymin = Chosen[i, close], ymax = Chosen[i, opening], color = color_chosen, linewidth = 2)  
   
    ax[0].grid() 
     
    ax[1].plot(Data[-window:, second_panel], color = 'royalblue', linewidth = 1)
    ax[1].grid()
    
def performance_variable_period(Data, close, buy, sell, long_result_col, short_result_col, total_result_col):
    
    # Adding a few columns
    Data = adder(Data, 10)
    
    # Variable Holding Period
    for i in range(len(Data)):
        
        try:
            
            if Data[i, buy] == 1:
                
                for a in range(i + 1, i + 1000):
                    
                    if Data[a, buy] == 1 or Data[a, sell] == -1:
                        
                        Data[a, long_result_col] = Data[a, close] - Data[i, close]
                        
                        break
                    
                    else:
                        
                        continue                
                    
            else:
                
                continue
            
        except IndexError:
            
            pass
                    
    for i in range(len(Data)):
        
        try:
            
            if Data[i, sell] == -1:
                
                for a in range(i + 1, i + 1000):
                                        
                    if Data[a, buy] == 1 or Data[a, sell] == -1:
                        
                        Data[a, short_result_col] = Data[i, close] - Data[a, close]
                        
                        break   
                     
                    else:
                        
                        continue
                    
            else:
                continue
            
        except IndexError:
            
            pass   
        
    # Aggregating the Long & Short Results Into One Column
    Data[:, total_result_col] = Data[:, long_result_col] + Data[:, short_result_col]  
    
    # Profit Factor    
    total_net_profits = Data[Data[:, total_result_col] > 0, total_result_col]
    total_net_losses  = Data[Data[:, total_result_col] < 0, total_result_col] 
    total_net_losses  = abs(total_net_losses)
    profit_factor     = round(np.sum(total_net_profits) / np.sum(total_net_losses), 2)

    # Hit Ratio    
    hit_ratio         = len(total_net_profits) / (len(total_net_losses) + len(total_net_profits))
    hit_ratio         = round(hit_ratio, 2) * 100
    
    # Risk Reward Ratio
    average_gain            = total_net_profits.mean()
    average_loss            = total_net_losses.mean()
    realized_risk_reward    = average_gain / average_loss
        
    # Expectancy
    expectancy    = (average_gain * (hit_ratio / 100)) - ((1 - (hit_ratio / 100)) * average_loss)
    expectancy    = round(expectancy, 4)
        
    # Number of Trades
    trades = len(total_net_losses) + len(total_net_profits)
        
    print('Hit Ratio         = ', hit_ratio)
    print('Average Gain      = ', average_gain * 100000)
    print('Average Loss      = ', average_loss * 100000)    
    print('Expectancy        = ', expectancy * 100000)
    print('Profit factor     = ', profit_factor) 
    print('Realized RR       = ', round(realized_risk_reward, 3))
    print('Number of Trades  = ', trades)    
   
    return Data

def performance_fixed_period(Data, close, buy, sell, period, long_result_col, short_result_col, total_result_col):
    
    # Adding a few columns
    Data = adder(Data, 10)
    
    # Fixed Period Holding
    for i in range(len(Data)):
        
        try: 
            
            if Data[i, buy] == 1:
                
                Data[i + period, long_result_col] = Data[i + period, close] - Data[i, close]
    
            elif Data[i, sell] == -1:
                
                Data[i + period, short_result_col] = Data[i, close] - Data[i + period, close]  
                
        except IndexError:
            
            pass   
        
    # Aggregating the Long & Short Results Into One Column
    Data[:, total_result_col] = Data[:, long_result_col] + Data[:, short_result_col]  
    
    # Profit Factor    
    total_net_profits = Data[Data[:, total_result_col] > 0, total_result_col]
    total_net_losses  = Data[Data[:, total_result_col] < 0, total_result_col] 
    total_net_losses  = abs(total_net_losses)
    profit_factor     = round(np.sum(total_net_profits) / np.sum(total_net_losses), 2)

    # Hit Ratio    
    hit_ratio         = len(total_net_profits) / (len(total_net_losses) + len(total_net_profits))
    hit_ratio         = round(hit_ratio, 2) * 100
    
    # Risk Reward Ratio
    average_gain            = total_net_profits.mean()
    average_loss            = total_net_losses.mean()
    realized_risk_reward    = average_gain / average_loss
        
    # Expectancy
    expectancy    = (average_gain * (hit_ratio / 100)) - ((1 - (hit_ratio / 100)) * average_loss)
    expectancy    = round(expectancy, 4)
        
    # Number of Trades
    trades = len(total_net_losses) + len(total_net_profits)
        
    print('Hit Ratio         = ', hit_ratio)
    print('Average Gain      = ', average_gain * 100000)
    print('Average Loss      = ', average_loss * 100000)    
    print('Expectancy        = ', expectancy * 100000)
    print('Profit factor     = ', profit_factor) 
    print('Realized RR       = ', round(realized_risk_reward, 3))
    print('Number of Trades  = ', trades)    
   
    return Data

def signal_chart_bars(Data, close, what_bull, what_bear, window = 500):   
     
    Plottable = Data[-window:, ]
    
    fig, ax = plt.subplots(figsize = (10, 5))
    
    ohlc_plot_bars(Data, window)    

    for i in range(len(Plottable)):
        
        if Plottable[i, what_bull] == 1:
            
            x = i
            y = Plottable[i, close]
        
            ax.annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = 11, headwidth = 11, facecolor = 'green', color = 'green'))
        
        elif Plottable[i, what_bear] == -1:
            
            x = i
            y = Plottable[i, close]
        
            ax.annotate(' ', xy = (x, y), 
                        arrowprops = dict(width = 9, headlength = -11, headwidth = -11, facecolor = 'red', color = 'red'))  
