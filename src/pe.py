from pyecharts import options as opts
from pyecharts.charts import Line
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("2024-04-17接口调用频率.csv")

# 将时间列转换为 datetime 类型，明确指定时间格式
df['时间'] = pd.to_datetime(df['时间'], format='%Y-%m-%d %H%M')
df = df[df['应用'] == '平台后台']
# 设置需要保留的接口列表
target_interfaces = [
    "/PT/business/chats/groupUsercx$m=query.service",
    "/PT/business/chats/groupListcx$m=query.service"   
]

# 过滤数据，只保留指定接口的数据
df = df[df['接口'].isin(target_interfaces)]
# 提取数据
interfaces = df["接口"].unique().tolist()

# 创建折线图对象
line = Line()

# 添加 x 轴数据
line.add_xaxis(xaxis_data=df['时间'].tolist())
print(len(df['时间'].tolist()))

# 添加各个接口的 y 轴数据
for interface in interfaces:
    interface_data = df[df['接口'] == interface]['调用频率'].tolist()
    print(len(interface_data))
    line.add_yaxis(
        series_name=interface,
        y_axis=interface_data,
        label_opts=opts.LabelOpts(is_show=False),
        is_smooth=True
    )

# 设置全局选项
line.set_global_opts(
    title_opts=opts.TitleOpts(title="接口调用频率"),
    tooltip_opts=opts.TooltipOpts(trigger="axis"),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        axistick_opts=opts.AxisTickOpts(is_show=True),
        splitline_opts=opts.SplitLineOpts(is_show=True),
    ),
    xaxis_opts=opts.AxisOpts(
        type_="time", boundary_gap=False),  # 将 x 轴类型设置为时间型
)

# 保存为 HTML 文件
line.render("接口调用频率.html")
