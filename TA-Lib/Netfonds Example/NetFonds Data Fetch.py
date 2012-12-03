# Some sample code to test getting intra-day prices from www.netfonds.no
# 
# Prices are available for approximately the last 15 days (to be confirmed)
#
# Note that AAPL.O denotes NASDAQ where
#    NASDAQ: O
#    NYSE: N
#    AMEX: A
#

from pylab import *
from urllib import urlretrieve
import talib
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib.finance import candlestick
import pandas as pd

from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY

url='http://hopey.netfonds.no/posdump.php?date=20121130&paper=%s.O&csv_format=csv'

urlretrieve(url % 'AAPL', 'AAPL.csv')
urlretrieve(url % 'GOOG', 'GOOG.csv')

AAPL = pd.read_csv('AAPL.csv')
GOOG = pd.read_csv('GOOG.csv')

AAPL = AAPL.drop_duplicates(cols='time')
GOOG = GOOG.drop_duplicates(cols='time')




for i in AAPL.index:
    AAPL['time'][i]=pd.datetime.strptime(AAPL['time'][i],'%Y%m%dT%H%M%S')
#AAPL.index=AAPL['time']; del AAPL['time']
AAPL.index=AAPL['time']

for i in GOOG.index:
    GOOG['time'][i]=pd.datetime.strptime(GOOG['time'][i],'%Y%m%dT%H%M%S')
#GOOG.index=GOOG['time']; del GOOG['time']
GOOG.index=GOOG['time']

AAPL.time = date2num(AAPL.time)
GOOG.time = date2num(GOOG.time)
 
DATA = pd.DataFrame({'AAPL':AAPL['bid'],'GOOG':GOOG['bid']}) 

DATA = DATA[DATA.index > pd.datetime(2012, 11, 30, 9, 59, 0)]

DATA['AAPL'] = (DATA['AAPL'].fillna(method='ffill')).fillna(method='backfill')
DATA['GOOG'] = (DATA['GOOG'].fillna(method='ffill')).fillna(method='backfill')

DATA['GOOG_SMA'] = talib.SMA(DATA['GOOG'],1000)
DATA['GOOG_FMA'] = talib.SMA(DATA['GOOG'],500)

DATA['AAPL_SMA'] = talib.SMA(DATA['AAPL'],1000)
DATA['AAPL_FMA'] = talib.SMA(DATA['AAPL'],500)
 
print DATA.ix[:20].to_string()


DATA = pd.DataFrame({'AAPL':AAPL['bid'], 'GOOG':GOOG['bid']})

# Compute OHLC data with pandas from raw tick data
DATA_15MIN = pd.Panel({'AAPL':DATA.AAPL.resample('15min', how='ohlc', fill_method='backfill'),
                       'GOOG':DATA.GOOG.resample('15min', how='ohlc', fill_method='backfill')})

DATA_15MIN.GOOG['time']=DATA_15MIN.GOOG.index
DATA_15MIN.AAPL['time']=DATA_15MIN.AAPL.index
  
DATA_15MIN.GOOG = DATA_15MIN.GOOG.reindex(columns= ('time','open', 'close', 'high', 'low'))
DATA_15MIN.AAPL = DATA_15MIN.AAPL.reindex(columns= ('time','open', 'close', 'high', 'low'))

DATA_15MIN.GOOG['time'] = date2num(DATA_15MIN.GOOG['time'])
DATA_15MIN.AAPL['time'] = date2num(DATA_15MIN.AAPL['time'])
                       
# Technical Analysis
DATA_15MIN.GOOG['SMA'] = talib.MA(DATA_15MIN.GOOG.close, 15)
DATA_15MIN.GOOG['FMA'] = talib.MA(DATA_15MIN.GOOG.close, 9)

DATA_15MIN.AAPL['SMA'] = talib.MA(DATA_15MIN.AAPL.close, 15)
DATA_15MIN.AAPL['FMA'] = talib.MA(DATA_15MIN.AAPL.close, 9)

#mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
#alldays    = DayLocator()               # minor ticks on the days
#weekFormatter = DateFormatter('%b %d')  # Eg, Jan 12
#dayFormatter = DateFormatter('%d')

fig = figure()
fig.subplots_adjust(bottom=0.2)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
#ax.xaxis.set_major_locator(mondays)
#ax.xaxis.set_minor_locator(alldays)
#ax.xaxis.set_major_formatter(weekFormatter)
#ax1.xaxis.set_minor_formatter(dayFormatter)
#ax2.xaxis.set_minor_formatter(dayFormatter)

# Plot

candlestick(ax1, np.array(DATA_15MIN.AAPL), width=(1/48), colorup='g', colordown='r')
candlestick(ax2, np.array(DATA_15MIN.GOOG), width=(1/48), colorup='g', colordown='r')

#fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)

ax1.set_ylabel('AAPL', size=20)
ax2.set_ylabel('GOOG', size=20)

#DATA_15MIN.AAPL.close.plot(ax=ax1, lw=2)
DATA_15MIN.AAPL.SMA.plot(ax=ax1, c = 'g', label='SMA')
DATA_15MIN.AAPL.FMA.plot(ax=ax1, c = 'r', label='FMA')
ax1.legend(loc='upper left')

#DATA_15MIN.GOOG.close.plot(ax=ax2, lw=2)
DATA_15MIN.GOOG.SMA.plot(ax=ax2, c = 'g')
DATA_15MIN.GOOG.FMA.plot(ax=ax2, c = 'r')
ax2.legend(loc='upper left')


plt.show()
print "Done."