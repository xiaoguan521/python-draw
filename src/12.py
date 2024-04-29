import pandas as pd
import matplotlib.pyplot as plt

# 定义要读取的CSV文件列表
file_names = ['2024-04-16接口调用频率.csv', '2024-04-17接口调用频率.csv',
              '2024-04-18接口调用频率.csv', '2024-04-19接口调用频率.csv', '2024-04-20接口调用频率.csv', '2024-04-21接口调用频率.csv']

# 创建一个空的DataFrame来存储所有数据
all_data = pd.DataFrame()

# 循环读取每个CSV文件并将其合并到all_data DataFrame中
for file in file_names:
    # 读取当前文件的数据
    data = pd.read_csv(file)
    # 将当前文件的数据添加到all_data中
    all_data = pd.concat([all_data, data])

# 可以在这里对合并后的数据进行分析和处理

# 绘制折线图
plt.plot(all_data['x_column'], all_data['y_column'])
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Title')
plt.show()
