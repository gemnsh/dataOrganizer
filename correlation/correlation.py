import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.ticker import FuncFormatter

a='■'
df = pd.read_csv('./소비자.csv', sep=',',encoding='cp949')
df2 = pd.read_csv('./기사.csv', sep=',',encoding='cp949')
df3 = pd.read_csv('./가게.csv', sep=',',encoding='cp949')

font_path = 'C:/Windows/Fonts/KoPubDotumBold.ttf'
fontprop = fm.FontProperties(fname=font_path, size=18)
fontprop2 = fm.FontProperties(fname=font_path, size=10)

df['날짜'] = pd.to_datetime(df['날짜'])
df2['날짜'] = pd.to_datetime(df2['날짜'])
df3['날짜'] = pd.to_datetime(df3['날짜'])

fig, ax1 = plt.subplots(figsize=(15, 5))
ax2=ax1.twinx()
ax3=ax1.twinx()
ax1.plot(df['날짜'], df['Android+IOS 사용자 수'],linewidth=0.4,label='소비자',color='#0000ff')
ax2.plot(df2['날짜'], df2['Android+IOS 사용자 수'],linewidth=0.4,label='기사', color='#00ff00')
ax3.plot(df3['날짜'], df3['Android+IOS 사용자 수'],linewidth=0.4,label='가게' ,color='#ff0000')
ax1.tick_params(axis='y', labelcolor='r')
ax2.tick_params(axis='y', labelcolor='b')
ax3.tick_params(axis='y', labelcolor='g')
ax3.spines['right'].set_position(('outward', 70))

def scientific_formatter(x, pos):
    return f'{x:.1e}'

ax1.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))
ax2.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))
ax3.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))

ax1.legend(prop=fontprop2,loc=(0.17,0.10),frameon=False)
ax2.legend(prop=fontprop2,loc=(0.17,0.06),frameon=False)
ax3.legend(prop=fontprop2,loc=(0.17,0.02),frameon=False)
ax2.yaxis.label.set_size(12)
ax3.yaxis.label.set_size(12)

correlation = df['Android+IOS 사용자 수'].corr(df2['Android+IOS 사용자 수'])
correlation2 = df2['Android+IOS 사용자 수'].corr(df3['Android+IOS 사용자 수'])
correlation3 = df['Android+IOS 사용자 수'].corr(df3['Android+IOS 사용자 수'])

plt.figtext(0.06, 0.21, f'소비자 vs 기사 상관 계수: {correlation:.2f}', ha='left', va='top', fontproperties=fontprop2, fontsize=10,bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))
plt.figtext(0.06, 0.17, f'기사 vs 가게 상관 계수: {correlation2:.2f}', ha='left', va='top', fontproperties=fontprop2, fontsize=10,bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))
plt.figtext(0.06, 0.13, f'소비자 vs 가게 상관 계수: {correlation3:.2f}', ha='left', va='top', fontproperties=fontprop2, fontsize=10,bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))
plt.title(a+' 관련 어플 사용자 수',fontproperties=fontprop)
plt.tight_layout()
plt.subplots_adjust()
plt.show()


