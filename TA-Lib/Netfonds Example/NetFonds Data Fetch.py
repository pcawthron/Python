# Some sample code to test getting intrady prices from www.netfonds.no
# 
# Prices are available for appriximately the last 15 days (to be confirmed)
#
# Note that AAPL.O denotes NASDAQ where
#    NASDAQ: O
#    NYSE: N
#    AMEX: A
#

from pylab import *
from pandas import *
from urllib import urlretrieve
import talib

url='http://hopey.netfonds.no/posdump.php?date=20121130&paper=%s.O&csv_format=csv'

urlretrieve(url % 'AAPL', 'AAPL.csv')
urlretrieve(url % 'GOOG', 'GOOG.csv')

AAPL = read_csv('AAPL.csv')
GOOG = read_csv('GOOG.csv')

AAPL = AAPL.drop_duplicates(cols='time')
GOOG = GOOG.drop_duplicates(cols='time')

for i in AAPL.index:
    AAPL['time'][i]=datetime.strptime(AAPL['time'][i],'%Y%m%dT%H%M%S')
AAPL.index=AAPL['time']; del AAPL['time']

for i in GOOG.index:
    GOOG['time'][i]=datetime.strptime(GOOG['time'][i],'%Y%m%dT%H%M%S')
GOOG.index=GOOG['time']; del GOOG['time']
 
DATA = DataFrame({'AAPL':AAPL['bid'],'GOOG':GOOG['bid']}) 

DATA = DATA[DATA.index > datetime(2012, 11, 30, 9, 59, 0)]

DATA['AAPL'] = (DATA['AAPL'].fillna(method='ffill')).fillna(method='backfill')
DATA['GOOG'] = (DATA['GOOG'].fillna(method='ffill')).fillna(method='backfill')

DATA['GOOG_SMA'] = talib.SMA(DATA['GOOG'],500)
DATA['GOOG_FMA'] = talib.SMA(DATA['GOOG'],200)
 
print DATA.ix[:20].to_string()
DATA.plot(subplots=True)

plt.show() 
 
 
print "Done."