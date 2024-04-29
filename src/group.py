import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

plt.rcParams['font.sans-serif'] = ['SimSun']
# 读取CSV文件
df = pd.read_csv('2024-04-17接口调用频率.csv')

# 将时间列转换为datetime类型，明确指定时间格式
df['时间'] = pd.to_datetime(df['时间'], format='%Y-%m-%d %H%M')

# 过滤数据，只保留应用名称为"平台后台"的数据
df = df[df['应用'] == '平台后台']

# 按应用和接口分组，计算每个组合的调用频率

grouped = df.groupby(['应用', '接口']).agg({'调用频率': 'sum'}).reset_index()

# 获取调用频率最高的前100个组合
top_100 = grouped.nlargest(10, '调用频率')

plt.figure(figsize=(10, 6))
for index, row in top_100.iterrows():
    plt.plot(df[(df['应用'] == row['应用']) & (df['接口'] == row['接口'])]['时间'],
             df[(df['应用'] == row['应用']) & (df['接口'] == row['接口'])]['调用频率'],
             label=f"{row['应用']} - {row['接口']}")

plt.xlabel('时间')
plt.ylabel('调用频率')
plt.title('Top 100 组合的调用频率折线图')
plt.legend()
plt.xticks(rotation=45)

# 自定义横坐标时间显示格式
date_formatter = DateFormatter('%d %H:%M')
plt.gca().xaxis.set_major_formatter(date_formatter)

plt.tight_layout()
plt.show()
