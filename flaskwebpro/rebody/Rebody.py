'''
Author: your name
Date: 2021-01-22 16:35:35
LastEditTime: 2021-01-23 16:45:54
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \zhihu\zhihuRebody.py
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

#读入CSV文件

df = pd.read_csv('imdb_data.csv')
#这两句作用为防止中文乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

"""
df.shape
df_sum = sum(df.duplicated())
print(df_sum)
print(df.columns)
# 查看更多的列信息和每列数据类型
print(df.info())
print(df.describe())
"""


x = np.array([1, 2, 3, 4])
y = x * 2

# 一个图形中包含多个图表
# plt.subplot(nrows, ncols, plot_number)
"""
Scatteplot是用于研究两个变量之间关系的经典和基本图。如果数据中有多个组，则可能需要以不同颜色可视化每个组。
"""
ax_1 = plt.subplot(2, 2, 1)
total_bill = df['rating'].values
tip = df['metascore'].values
plt.scatter(x=total_bill,y=tip,marker='o',s=20,alpha=0.5,edgecolors='black',linewidths=1)
plt.xlabel('rating')
plt.ylabel('metascore')
plt.title('关于rating与metascore评分得散点图分析')

#带边界的气泡图（Bubble plot with Encircling）
ax_2 = plt.subplot(2, 2, 2)
total_bill = df['rating'].values
tip = df['cumulative_worldwide_gross'].values
plt.scatter(x=total_bill,y=tip,marker='o',s=20,alpha=0.5,edgecolors='black',linewidths=1)
plt.xlabel('rating')
plt.ylabel('全球总票房')
plt.title('关于rating与全球总票房评分得散点图分析')

ax_3 = plt.subplot(2, 2, 3)
#计算每年的电影产量
movie_year = df.groupby('release_date')['title'].count() #计算每年的电影产量
#print(movie_year.index.tolist())
#print(movie_year.values.tolist())

total_bill = (movie_year.index.tolist()) #把index索引值拿出来作为x轴，也就是年份，以列表形式输出。
tip = (movie_year.values.tolist())#把values值作为y轴，也就是每年的电影量的和。
plt.xlabel('时间') #设置x轴标签
plt.ylabel('电影量')#设置y轴标签
plt.title('电影产量年份图')#设置标题名称
plt.plot(total_bill, tip)
plt.bar(total_bill, tip)

ax_4 = plt.subplot(2, 2, 4)

mpl.rcParams['legend.fontsize'] = 10
 
fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
axis_x = df['rating'].values
axis_y = df['metascore'].values
axis_z = df['cumulative_worldwide_gross'].values

ax.set_xlabel('rating评分')
ax.set_ylabel('metascore评分')
ax.set_zlabel('全球总票房')

col =np.where(axis_x>8.0,'g',np.where(axis_y>80,'r',np.where(axis_z>500000000,'c','y')))
ax.scatter(axis_x, axis_y, axis_z,c =col,label='关于rating、metascore及评分得散点图分析')
ax.legend()


# 设置图表
# plt.tight_layout()
plt.subplots_adjust(top=0.969, bottom=0.081, left=0.052, right=0.977, hspace=0.2, wspace=0.12)

plt.show()