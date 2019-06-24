# -*- coding: utf-8 -*-
#!/usr/bin/python3

import pandas as pd
import numpy as np

data = pd.read_excel('timespan.xlsx', index_col=None, header=None, usecols=1)

data['start'] = data[0].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
data['end'] = data[1].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

data['before'] = data[0].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
data['before'] = data['before'] - pd.Timedelta(5, unit='day')

data['after'] = data[1].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
data['after'] = data['after'] + pd.Timedelta(5, unit='day')


# data['start-str'] = data['start'].dt.strftime('%m/%d').apply(lambda x: 'new Date(\"'+x+'\"),')
# data['end-str'] = data['end'].dt.strftime('%m/%d').apply(lambda x: 'new Date(\"'+x+'\"),')
# y_axis = pd.Series(np.array(range(1961,2017,1)))   
# y_axis = y_axis.apply(lambda x: str(x))
y_axis = data['start'].dt.strftime('%Y')  #.apply(lambda x: x+'年')


# print('   ---------- year start ---------- ')
# data['start'].dt.strftime('%Y/%m/%d').apply(lambda x: print(x))
# print('   ---------- year end ---------- ')
# data['end'].dt.strftime('%Y/%m/%d').apply(lambda x: print(x))

# print('   ---------- y axis ---------- ')
# print(list(y_axis))
# print('   ---------- month start ---------- ')
# data['start'].dt.strftime('%m').apply(lambda x: print(x))
# print('   ---------- month end ---------- ')
# data['end'].dt.strftime('%m').apply(lambda x: print(x))
# print('   ---------- day start ---------- ')
# data['start'].dt.strftime('%d').apply(lambda x: print(x))
# print('   ---------- day end ---------- ')
# data['end'].dt.strftime('%d').apply(lambda x: print(x))

print('   ---------- day before ---------- ')
print(list(data['before'].dt.strftime('%Y%m%d')))
print('   ---------- day after ---------- ')
print(list(data['after'].dt.strftime('%Y%m%d')))