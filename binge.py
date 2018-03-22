# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:39:46 2018

@author: farming567
"""
import matplotlib.dates as mdate
from matplotlib.dates import DateFormatter
import strategy as st
## 斌哥
road = 'C:\\Users\\farming567\\Desktop\\new\\'
filename = 'binge.xlsx'
zs = pd.read_excel(road+filename)       
zs = zs.loc[:,['时间','盈亏']]
zs['盈亏'] = zs['盈亏'].apply(lambda x: 0 if str(x).isspace() else x)
zs['盈亏'] = zs['盈亏'].apply(lambda x: 0 if np.isnan(x) else x)
grouped=zs['盈亏'].groupby(zs['时间'])
test = grouped.sum()

final = s['2017-05-11':'2018-01-09'].loc[:,'300etf']
data = pd.concat([final, test], axis = 1,join = 'outer')
data['盈亏'] = data['盈亏'].apply(lambda x: 0 if np.isnan(x) else x)

asset = [10000000]
for i in range(1,len(final.index)):
    if data.loc[data.index[i],'盈亏'] == 0:
        asset.append(asset[i-1])
    else:
        asset.append(asset[i-1]+data.loc[data.index[i],'盈亏'])
data.loc[:,'value'] = asset

s = data.loc[:,['300etf','value']]
s.columns =['hs300','value']    
s_return = (s-s.shift(1))/s.shift(1) #计算收益率
std_price = (1+s_return).cumprod()
std_price = std_price.dropna() # 删除空值所在的行
s_return = s_return.dropna()

st.annual_return(std_price.index, std_price.loc[:,'value']) 
st.max_drawdown(std_price.index, std_price.loc[:,'value'])
st.sharpe_ratio(std_price.index, std_price.loc[:,'value'], s_return.loc[:,'value'])
st.volatility(std_price.index,  s_return.loc[:,'value'])

# 周数据
week_data = s
week_data['weekday'] = [date.weekday() for date in week_data.index]
week_data = week_data[week_data['weekday']==4]
w_return = (week_data-week_data.shift(1))/week_data.shift(1) #计算收益率
w_price = (1+w_return).cumprod()
w_price = w_price.dropna() # 删除空值所在的行
w_return = w_return.dropna()

st.max_drawdown(w_price.index, w_price.loc[:,'value'])

'''
st.max_drawdown(std_price.index, std_price.loc[:,'n_4'])                           
# 年化收益率
st.annual_return(std_price.index, std_price.loc[:,'n_4'])
# 最大回撤
st.max_drawdown(std_price.index, std_price.loc[:,'n_4'])
# 平均涨幅
st.average_change(std_price.index,  s_return.loc[:,'n_4'])
# 上涨概率
st.prob_up(std_price.index,  s_return.loc[:,'n_4'])
# 最大连续上涨天数和最大连续下跌天数
st.max_successive_up(std_price.index,  s_return.loc[:,'n_4'])
# 最大单周期涨幅和最大单周期跌幅
max_period_return(std_price.index,  s_return.loc[:,'n_4'])
# 收益波动率
volatility(std_price.index,  s_return.loc[:,'n_4'])
# beta值
beta(std_price.index,s_return.loc[:,'n_4'], s_return.loc[:,'300etf'])
# alpha值
alpha(std_price.index, std_price.loc[:,'n_4'], std_price.loc[:,'300etf'], s_return.loc[:,'n_4'], s_return.loc[:,'n_4'])
# 夏普比率
sharpe_ratio(std_price.index, std_price.loc[:,'n_4'], s_return.loc[:,'n_4'])
# 信息比率
info_ratio(std_price.index, s_return.loc[:,'n_4'], s_return.loc[:,'n_4'])
'''                            
#可视化
fig=plt.figure(figsize=(15,7.8))
ax1=fig.add_subplot(111)
ax1.plot(std_price.loc[:,'hs300'],'y--')  #可修改
ax1.plot(std_price.loc[:,'value'])  #可修改

ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))#设置时间标签显示格式   
plt.xticks(pd.date_range('2017-05-01','2018-01-20',freq = '7D'),fontsize=10, rotation=50)
plt.yticks(np.arange(0.95,1.5,0.05),fontsize=10)

plt.grid(True, linestyle = "--", linewidth = "0.5") 
plt.legend(loc='upper left')
plt.savefig(road+"binge"+'.jpg',transparent=True, dpi = 800,bbox_inches = 'tight') 
plt.show()




