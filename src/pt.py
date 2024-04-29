import pyecharts.options as opts
from pyecharts.charts import Line
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("2024-04-17接口调用频率.csv")

# 将时间列转换为 datetime 类型，明确指定时间格式
df['时间'] = pd.to_datetime(df['时间'], format='%Y-%m-%d %H%M')
df = df[df['应用'] == '平台后台']
# 设置需要保留的接口列表
# target_interfaces = [
#     "/PT/business/chats/groupUsercx$m=query.service", "/PT/business/messages/xxflsl$m=execute.service", "/PT/business/settings/sfydspyh$m=query.service"
# ]
target_interfaces = df["接口"].unique().tolist()
# 过滤数据，只保留指定接口的数据
df = df[df['接口'].isin(target_interfaces)]
# 提取数据
interfaces = df["接口"].unique().tolist()

# 创建折线图对象
line = Line()

# 添加 x 轴数据，一天中每分钟的时间
x_data = pd.date_range(start='2024-04-17 00:00',
                       end='2024-04-17 23:59', freq='T')
x_data = x_data.strftime('%Y-%m-%d %H:%M')
line.add_xaxis(xaxis_data=x_data)

# 添加各个接口的 y 轴数据
for interface in interfaces:
    y_data = []
    interface_data = df[df['接口'] == interface][['时间', '调用频率']]
    interface_data.set_index('时间', inplace=True)
    # 将特定时间点的数据与 x 轴上的时间点对应起来

    for time in x_data:
        if time in interface_data.index:
            y_data.append(int(interface_data.loc[time, '调用频率']))
            # print(time)
            # # print(interface_data.loc[time, '调用频率'])
            # print(interface_data.get(time+":00"))
        else:
            y_data.append(None)  # 若该时间点无数据，则填充为 None

    line.add_yaxis(
        series_name=interface,
        y_axis=y_data,
        label_opts=opts.LabelOpts(is_show=False),
        is_smooth=True,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
        is_connect_nones=True
    )

# 设置全局选项
line.set_global_opts(
    title_opts=opts.TitleOpts(title="接口调用频率"),
    init_opts=opts.InitOpts(width="1200px", height="600px")
    tooltip_opts=opts.TooltipOpts(trigger="axis"),
    xaxis_opts=opts.AxisOpts(
        type_="category",
        boundary_gap=False,
        axisline_opts=opts.AxisLineOpts(is_on_zero=True),
    ),
    legend_opts=opts.LegendOpts(pos_left="left"),
    toolbox_opts=opts.ToolboxOpts(is_show=True),
)

# 保存为 HTML 文件
line.render("接口调用频率.html")
