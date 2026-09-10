import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import math

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "向量概念可视化系统"

# 颜色方案
COLORS = {
    'background': '#1E1E1E',
    'paper_bgcolor': '#1E1E1E',
    'plot_bgcolor': '#1E1E1E',
    'text': '#FFFFFF',
    'vector_a': '#FF6B6B',
    'vector_b': '#4D96FF', 
    'vector_sum': '#6BCB77',
    'vector_scaled': '#FFD93D',
    'grid': '#444444'
}

# ======== 布局定义 ========
app.layout = dbc.Container([
    # 标题
    dbc.Row([
        dbc.Col([
            html.H1("向量概念可视化系统", 
                   className="text-center mb-4",
                   style={'color': '#FFD700', 'fontWeight': 'bold'})
        ])
    ]),
    
    # 标签页导航
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="main-tabs", value='tab-1', children=[
                dcc.Tab(label='1. 向量的概念', value='tab-1',
                       style={'backgroundColor': '#2E2E2E', 'color': 'white'},
                       selected_style={'backgroundColor': '#4D96FF', 'color': 'white'}),
                dcc.Tab(label='2. 向量的线性运算', value='tab-2',
                       style={'backgroundColor': '#2E2E2E', 'color': 'white'},
                       selected_style={'backgroundColor': '#4D96FF', 'color': 'white'}),
                dcc.Tab(label='3. 空间直角坐标系', value='tab-3',
                       style={'backgroundColor': '#2E2E2E', 'color': 'white'},
                       selected_style={'backgroundColor': '#4D96FF', 'color': 'white'}),
                dcc.Tab(label='4. 向量的投影', value='tab-4',
                       style={'backgroundColor': '#2E2E2E', 'color': 'white'},
                       selected_style={'backgroundColor': '#4D96FF', 'color': 'white'}),
            ])
        ])
    ], className="mb-4"),
    
    # 标签页内容
    html.Div(id='tab-content')
], fluid=True, style={'backgroundColor': COLORS['background']})

# ======== 1. 向量的概念 ========
def create_vector_concept_tab():
    return dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='vector-concept-plot',
                figure=create_vector_concept_figure(),
                config={'displayModeBar': True}
            )
        ], width=8),
        dbc.Col([
            html.Div([
                html.H4("向量的基本概念", style={'color': '#FFD700'}),
                html.Hr(style={'borderColor': '#444444'}),
                html.P("向量是既有大小又有方向的量，在数学和物理学中有着广泛的应用。", 
                      style={'color': 'white'}),
                html.Ul([
                    html.Li("大小：向量的长度（模）", style={'color': '#FF6B6B'}),
                    html.Li("方向：箭头指示的方向", style={'color': '#4D96FF'}),
                    html.Li("起点：向量的起始位置", style={'color': '#6BCB77'}),
                    html.Li("终点：向量的结束位置", style={'color': '#FFD93D'})
                ], style={'color': 'white'}),
                html.P("向量可以用坐标表示，如：", style={'color': 'white'}),
                html.P("a = (3, 2)", style={
                    'color': '#FF6B6B', 
                    'fontSize': '20px', 
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                })
            ], style={
                'backgroundColor': '#2E2E2E',
                'padding': '20px',
                'borderRadius': '10px',
                'height': '100%'
            })
        ], width=4)
    ])

def create_vector_concept_figure():
    fig = go.Figure()
    
    # 添加坐标轴
    fig.add_shape(type="line", x0=-5, y0=0, x1=5, y1=0, line=dict(color="white", width=2))
    fig.add_shape(type="line", x0=0, y0=-1, x1=0, y1=4, line=dict(color="white", width=2))
    
    # 添加网格
    for i in range(-5, 6):
        fig.add_shape(type="line", x0=i, y0=-1, x1=i, y1=4, line=dict(color=COLORS['grid'], width=1, dash='dot'))
    for i in range(-1, 5):
        fig.add_shape(type="line", x0=-5, y0=i, x1=5, y1=i, line=dict(color=COLORS['grid'], width=1, dash='dot'))
    
    # 添加向量
    vector = [3, 2]
    fig.add_annotation(
        x=vector[0], y=vector[1],
        ax=0, ay=0,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=3,
        arrowcolor=COLORS['vector_a']
    )
    
    # 添加文本标注 - 使用斜体表示向量
    fig.add_annotation(x=vector[0]/2, y=vector[1]/2, text="<i>a</i>", showarrow=False, 
                      font=dict(size=20, color=COLORS['vector_a']))
    fig.add_annotation(x=vector[0]*0.9, y=vector[1]*1.05, text=f"终点: ({vector[0]}, {vector[1]})", 
                      showarrow=False, font=dict(size=12, color="white"))
    fig.add_annotation(x=0.05, y=0.05, text="起点: (0,0)", 
                      showarrow=False, font=dict(size=12, color="white"))
    
    # 设置图形属性
    fig.update_layout(
        title="向量的概念：有大小和方向的量",
        xaxis=dict(range=[-5, 5], title="X轴", gridcolor=COLORS['grid']),
        yaxis=dict(range=[-1, 4], title="Y轴", gridcolor=COLORS['grid']),
        plot_bgcolor=COLORS['plot_bgcolor'],
        paper_bgcolor=COLORS['paper_bgcolor'],
        font=dict(color=COLORS['text']),
        showlegend=False,
        height=600
    )
    
    return fig

# ======== 2. 向量的线性运算 ========
def create_vector_operations_tab():
    return dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='vector-operations-plot',
                figure=create_vector_operations_figure(2, 1, 1, 3, 2.0),
                config={'displayModeBar': True}
            )
        ], width=8),
        dbc.Col([
            html.Div([
                html.H4("向量线性运算控制", style={'color': '#FFD700'}),
                html.Hr(style={'borderColor': '#444444'}),
                
                html.H5("向量 a 坐标", style={'color': COLORS['vector_a'], 'marginTop': '20px'}),
                html.P("X坐标:", style={'color': 'white', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='a-x-slider',
                    min=-5, max=5, step=0.1, value=2,
                    marks={i: str(i) for i in range(-5, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.P("Y坐标:", style={'color': 'white', 'marginBottom': '5px', 'marginTop': '20px'}),
                dcc.Slider(
                    id='a-y-slider',
                    min=-2, max=6, step=0.1, value=1,
                    marks={i: str(i) for i in range(-2, 7)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.H5("向量 b 坐标", style={'color': COLORS['vector_b'], 'marginTop': '30px'}),
                html.P("X坐标:", style={'color': 'white', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='b-x-slider',
                    min=-5, max=5, step=0.1, value=1,
                    marks={i: str(i) for i in range(-5, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.P("Y坐标:", style={'color': 'white', 'marginBottom': '5px', 'marginTop': '20px'}),
                dcc.Slider(
                    id='b-y-slider',
                    min=-2, max=6, step=0.1, value=3,
                    marks={i: str(i) for i in range(-2, 7)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.H5("标量 k", style={'color': COLORS['vector_scaled'], 'marginTop': '30px'}),
                dcc.Slider(
                    id='k-slider',
                    min=0, max=3, step=0.1, value=2.0,
                    marks={i: str(i) for i in [0, 1, 2, 3]},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.Div(id='vector-calculations', style={'marginTop': '30px', 'color': 'white'})
                
            ], style={
                'backgroundColor': '#2E2E2E',
                'padding': '20px',
                'borderRadius': '10px',
                'height': '100%'
            })
        ], width=4)
    ])

def create_vector_operations_figure(a_x, a_y, b_x, b_y, k):
    fig = go.Figure()
    
    a = np.array([a_x, a_y])
    b = np.array([b_x, b_y])
    vector_sum = a + b
    scaled_a = k * a
    
    # 添加坐标轴
    fig.add_shape(type="line", x0=-8, y0=0, x1=8, y1=0, line=dict(color="white", width=2))
    fig.add_shape(type="line", x0=0, y0=-3, x1=0, y1=7, line=dict(color="white", width=2))
    
    # 添加网格
    for i in range(-8, 9):
        fig.add_shape(type="line", x0=i, y0=-3, x1=i, y1=7, line=dict(color=COLORS['grid'], width=1, dash='dot'))
    for i in range(-3, 8):
        fig.add_shape(type="line", x0=-8, y0=i, x1=8, y1=i, line=dict(color=COLORS['grid'], width=1, dash='dot'))
    
    # 添加向量 a - 使用斜体表示
    fig.add_annotation(
        x=a[0], y=a[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_a']
    )
    fig.add_trace(go.Scatter(x=[a[0]/2], y=[a[1]/2], mode="text", text=["<i>a</i>"],
                           textfont=dict(size=16, color=COLORS['vector_a']), showlegend=False))
    
    # 添加向量 b
    fig.add_annotation(
        x=b[0], y=b[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_b']
    )
    fig.add_trace(go.Scatter(x=[b[0]/2], y=[b[1]/2], mode="text", text=["<i>b</i>"],
                           textfont=dict(size=16, color=COLORS['vector_b']), showlegend=False))
    
    # 添加向量和
    fig.add_annotation(
        x=vector_sum[0], y=vector_sum[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_sum']
    )
    fig.add_trace(go.Scatter(x=[vector_sum[0]/2], y=[vector_sum[1]/2], mode="text", 
                           text=["<i>a</i> + <i>b</i>"], textfont=dict(size=16, color=COLORS['vector_sum']), showlegend=False))
    
    # 添加标量乘法结果
    fig.add_annotation(
        x=scaled_a[0], y=scaled_a[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_scaled']
    )
    fig.add_trace(go.Scatter(x=[scaled_a[0]/2], y=[scaled_a[1]/2], mode="text", 
                           text=[f"k·<i>a</i> (k={k})"], textfont=dict(size=16, color=COLORS['vector_scaled']), showlegend=False))
    
    # 添加虚线表示向量加法
    fig.add_shape(type="line", x0=a[0], y0=a[1], x1=vector_sum[0], y1=vector_sum[1],
                 line=dict(color=COLORS['vector_b'], width=2, dash="dash"))
    
    # 设置图形属性
    fig.update_layout(
        title="向量的线性运算",
        xaxis=dict(range=[-8, 8], title="X轴", gridcolor=COLORS['grid']),
        yaxis=dict(range=[-3, 7], title="Y轴", gridcolor=COLORS['grid']),
        plot_bgcolor=COLORS['plot_bgcolor'],
        paper_bgcolor=COLORS['paper_bgcolor'],
        font=dict(color=COLORS['text']),
        showlegend=False,
        height=600
    )
    
    return fig

# ======== 3. 空间直角坐标系（右手系） ========
def create_3d_coordinate_tab():
    return dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='3d-coordinate-plot',
                figure=create_3d_coordinate_figure(),
                config={'displayModeBar': True}
            )
        ], width=8),
        dbc.Col([
            html.Div([
                html.H4("空间直角坐标系（右手系）", style={'color': '#FFD700'}),
                html.Hr(style={'borderColor': '#444444'}),
                html.P("右手系坐标系：", style={'color': 'white'}),
                html.Ul([
                    html.Li("X轴（红色）- 右手拇指方向", style={'color': '#FF6B6B'}),
                    html.Li("Y轴（绿色）- 右手食指方向", style={'color': '#6BCB77'}),
                    html.Li("Z轴（蓝色）- 右手中指方向", style={'color': '#4D96FF'})
                ], style={'color': 'white'}),
                html.P("三个坐标平面将空间分为八个卦限：", style={'color': 'white', 'marginTop': '20px'}),
                html.Table([
                    html.Tr([html.Td("I卦限"), html.Td("(+,+,+)", style={'color': '#FF6B6B'})]),
                    html.Tr([html.Td("II卦限"), html.Td("(-,+,+)", style={'color': '#4D96FF'})]),
                    html.Tr([html.Td("III卦限"), html.Td("(-,-,+)", style={'color': '#6BCB77'})]),
                    html.Tr([html.Td("IV卦限"), html.Td("(+,-,+)", style={'color': '#FFD93D'})]),
                    html.Tr([html.Td("V卦限"), html.Td("(+,+,-)", style={'color': '#FF9AA2'})]),
                    html.Tr([html.Td("VI卦限"), html.Td("(-,+,-)", style={'color': '#A0E7E5'})]),
                    html.Tr([html.Td("VII卦限"), html.Td("(-,-,-)", style={'color': '#B5EAD7'})]),
                    html.Tr([html.Td("VIII卦限"), html.Td("(+,-,-)", style={'color': '#C7CEEA'})]),
                ], style={'width': '100%', 'color': 'white', 'marginTop': '10px'}),
                html.P("使用鼠标可以旋转、缩放和移动3D视图", style={'color': '#CCCCCC', 'marginTop': '20px', 'fontStyle': 'italic'}),
                html.P("右手定则：", style={'color': 'white', 'marginTop': '20px', 'fontWeight': 'bold'}),
                html.P("拇指指向X轴正方向，食指指向Y轴正方向，中指指向Z轴正方向", 
                      style={'color': '#FFD700', 'fontStyle': 'italic'})
            ], style={
                'backgroundColor': '#2E2E2E',
                'padding': '20px',
                'borderRadius': '10px',
                'height': '100%'
            })
        ], width=4)
    ])

def create_3d_coordinate_figure():
    fig = go.Figure()
    
    # 添加坐标轴 - 右手系
    # X轴：红色，从-5到5，水平向右
    fig.add_trace(go.Scatter3d(x=[-5, 5], y=[0, 0], z=[0, 0], 
                              mode='lines', line=dict(color='red', width=6), name='X轴'))
    # Y轴：绿色，从-5到5，水平向前（远离观察者）
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[-5, 5], z=[0, 0], 
                              mode='lines', line=dict(color='green', width=6), name='Y轴'))
    # Z轴：蓝色，从-5到5，垂直向上
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[-5, 5], 
                              mode='lines', line=dict(color='blue', width=6), name='Z轴'))
    
    # 添加坐标平面
    # XY平面 (z=0)
    xx, yy = np.meshgrid(np.linspace(-4, 4, 10), np.linspace(-4, 4, 10))
    zz = np.zeros_like(xx)
    fig.add_trace(go.Surface(x=xx, y=yy, z=zz, opacity=0.3, colorscale='Blues', showscale=False, name='XY平面'))
    
    # YZ平面 (x=0)
    yy, zz = np.meshgrid(np.linspace(-4, 4, 10), np.linspace(-4, 4, 10))
    xx = np.zeros_like(yy)
    fig.add_trace(go.Surface(x=xx, y=yy, z=zz, opacity=0.3, colorscale='Reds', showscale=False, name='YZ平面'))
    
    # XZ平面 (y=0)
    xx, zz = np.meshgrid(np.linspace(-4, 4, 10), np.linspace(-4, 4, 10))
    yy = np.zeros_like(xx)
    fig.add_trace(go.Surface(x=xx, y=yy, z=zz, opacity=0.3, colorscale='Greens', showscale=False, name='XZ平面'))
    
    # 添加卦限标记 - 右手系坐标
    quadrants = [
        (3, 3, 3, 'I', '#FF6B6B'), (-3, 3, 3, 'II', '#4D96FF'),
        (-3, -3, 3, 'III', '#6BCB77'), (3, -3, 3, 'IV', '#FFD93D'),
        (3, 3, -3, 'V', '#FF9AA2'), (-3, 3, -3, 'VI', '#A0E7E5'),
        (-3, -3, -3, 'VII', '#B5EAD7'), (3, -3, -3, 'VIII', '#C7CEEA')
    ]
    
    for x, y, z, label, color in quadrants:
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], 
                                 mode='text', text=[label],
                                 textfont=dict(size=16, color=color),
                                 showlegend=False))
    
    # 设置图形属性 - 调整视角以显示右手系
    fig.update_layout(
        title="空间直角坐标系与卦限（右手系）",
        scene=dict(
            xaxis=dict(title='X轴', gridcolor=COLORS['grid'], backgroundcolor=COLORS['plot_bgcolor']),
            yaxis=dict(title='Y轴', gridcolor=COLORS['grid'], backgroundcolor=COLORS['plot_bgcolor']),
            zaxis=dict(title='Z轴', gridcolor=COLORS['grid'], backgroundcolor=COLORS['plot_bgcolor']),
            bgcolor=COLORS['plot_bgcolor'],
            aspectmode='cube',
            # 设置相机位置以更好地显示右手系
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        paper_bgcolor=COLORS['paper_bgcolor'],
        font=dict(color=COLORS['text']),
        height=600
    )
    
    return fig

# ======== 4. 向量的投影 ========
def create_vector_projection_tab():
    return dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='vector-projection-plot',
                figure=create_vector_projection_figure(3, 2, 4, 1),
                config={'displayModeBar': True}
            )
        ], width=8),
        dbc.Col([
            html.Div([
                html.H4("向量投影控制", style={'color': '#FFD700'}),
                html.Hr(style={'borderColor': '#444444'}),
                
                html.H5("向量 AB 坐标", style={'color': COLORS['vector_a'], 'marginTop': '20px'}),
                html.P("X坐标:", style={'color': 'white', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='ab-x-slider',
                    min=-5, max=5, step=0.1, value=3,
                    marks={i: str(i) for i in range(-5, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.P("Y坐标:", style={'color': 'white', 'marginBottom': '5px', 'marginTop': '20px'}),
                dcc.Slider(
                    id='ab-y-slider',
                    min=-5, max=5, step=0.1, value=2,
                    marks={i: str(i) for i in range(-5, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.H5("投影方向向量 u", style={'color': COLORS['vector_b'], 'marginTop': '30px'}),
                html.P("X坐标:", style={'color': 'white', 'marginBottom': '5px'}),
                dcc.Slider(
                    id='u-x-slider',
                    min=-5, max=5, step=0.1, value=4,
                    marks={i: str(i) for i in range(-5, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.P("Y坐标:", style={'color': 'white', 'marginBottom': '5px', 'marginTop': '20px'}),
                dcc.Slider(
                    id='u-y-slider',
                    min=-5, max=5, step=0.1, value=1,
                    marks={i: str(i) for i in range(-5, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.Div(id='projection-calculations', style={'marginTop': '30px', 'color': 'white'})
                
            ], style={
                'backgroundColor': '#2E2E2E',
                'padding': '20px',
                'borderRadius': '10px',
                'height': '100%'
            })
        ], width=4)
    ])

def create_vector_projection_figure(ab_x, ab_y, u_x, u_y):
    fig = go.Figure()
    
    AB = np.array([ab_x, ab_y])
    u = np.array([u_x, u_y])
    
    # 计算投影
    dot_product = np.dot(AB, u)
    norm_u_squared = np.dot(u, u)
    
    if norm_u_squared < 1e-10:
        projection = np.zeros(2)
    else:
        scalar_proj = dot_product / norm_u_squared
        projection = scalar_proj * u
    
    # 添加坐标轴
    fig.add_shape(type="line", x0=-5, y0=0, x1=5, y1=0, line=dict(color="white", width=2))
    fig.add_shape(type="line", x0=0, y0=-5, x1=0, y1=5, line=dict(color="white", width=2))
    
    # 添加网格
    for i in range(-5, 6):
        fig.add_shape(type="line", x0=i, y0=-5, x1=i, y1=5, line=dict(color=COLORS['grid'], width=1, dash='dot'))
    for i in range(-5, 6):
        fig.add_shape(type="line", x0=-5, y0=i, x1=5, y1=i, line=dict(color=COLORS['grid'], width=1, dash='dot'))
    
    # 添加投影方向向量 u - 使用斜体表示
    fig.add_annotation(
        x=u[0], y=u[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_b']
    )
    fig.add_trace(go.Scatter(x=[u[0]/2], y=[u[1]/2], mode="text", text=["<i>u</i>"],
                           textfont=dict(size=16, color=COLORS['vector_b']), showlegend=False))
    
    # 添加向量 AB - 使用斜体表示
    fig.add_annotation(
        x=AB[0], y=AB[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_a']
    )
    fig.add_trace(go.Scatter(x=[AB[0]/2], y=[AB[1]/2], mode="text", text=["<i>AB</i>"],
                           textfont=dict(size=16, color=COLORS['vector_a']), showlegend=False))
    
    # 添加投影向量 - 使用斜体表示
    fig.add_annotation(
        x=projection[0], y=projection[1], ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3,
        arrowcolor=COLORS['vector_sum']
    )
    fig.add_trace(go.Scatter(x=[projection[0]/2], y=[projection[1]/2], mode="text", 
                           text=["Prj<sub><i>u</i></sub><i>AB</i>"], textfont=dict(size=16, color=COLORS['vector_sum']), showlegend=False))
    
    # 添加投影垂线
    fig.add_shape(type="line", x0=AB[0], y0=AB[1], x1=projection[0], y1=projection[1],
                 line=dict(color="white", width=2, dash="dash"))
    
    # 设置图形属性
    fig.update_layout(
        title="向量的投影",
        xaxis=dict(range=[-5, 5], title="X轴", gridcolor=COLORS['grid']),
        yaxis=dict(range=[-5, 5], title="Y轴", gridcolor=COLORS['grid']),
        plot_bgcolor=COLORS['plot_bgcolor'],
        paper_bgcolor=COLORS['paper_bgcolor'],
        font=dict(color=COLORS['text']),
        showlegend=False,
        height=600
    )
    
    return fig

# ======== 回调函数 ========
@app.callback(
    Output('tab-content', 'children'),
    Input('main-tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return create_vector_concept_tab()
    elif tab == 'tab-2':
        return create_vector_operations_tab()
    elif tab == 'tab-3':
        return create_3d_coordinate_tab()
    elif tab == 'tab-4':
        return create_vector_projection_tab()

@app.callback(
    [Output('vector-operations-plot', 'figure'),
     Output('vector-calculations', 'children')],
    [Input('a-x-slider', 'value'),
     Input('a-y-slider', 'value'),
     Input('b-x-slider', 'value'),
     Input('b-y-slider', 'value'),
     Input('k-slider', 'value')]
)
def update_vector_operations(a_x, a_y, b_x, b_y, k):
    fig = create_vector_operations_figure(a_x, a_y, b_x, b_y, k)
    
    a = np.array([a_x, a_y])
    b = np.array([b_x, b_y])
    vector_sum = a + b
    scaled_a = k * a
    
    calculations = [
        html.H5("计算结果", style={'color': '#FFD700'}),
        html.P(f"向量 a = ({a[0]:.1f}, {a[1]:.1f})", style={'color': COLORS['vector_a']}),
        html.P(f"向量 b = ({b[0]:.1f}, {b[1]:.1f})", style={'color': COLORS['vector_b']}),
        html.P(f"向量和 a + b = ({vector_sum[0]:.1f}, {vector_sum[1]:.1f})", style={'color': COLORS['vector_sum']}),
        html.P(f"数乘 k·a = ({scaled_a[0]:.1f}, {scaled_a[1]:.1f})", style={'color': COLORS['vector_scaled']}),
        html.P(f"标量 k = {k:.1f}", style={'color': COLORS['vector_scaled']})
    ]
    
    return fig, calculations

@app.callback(
    [Output('vector-projection-plot', 'figure'),
     Output('projection-calculations', 'children')],
    [Input('ab-x-slider', 'value'),
     Input('ab-y-slider', 'value'),
     Input('u-x-slider', 'value'),
     Input('u-y-slider', 'value')]
)
def update_vector_projection(ab_x, ab_y, u_x, u_y):
    fig = create_vector_projection_figure(ab_x, ab_y, u_x, u_y)
    
    AB = np.array([ab_x, ab_y])
    u = np.array([u_x, u_y])
    
    # 计算投影
    dot_product = np.dot(AB, u)
    norm_u_squared = np.dot(u, u)
    
    if norm_u_squared < 1e-10:
        scalar_proj = 0
        projection = np.zeros(2)
    else:
        scalar_proj = dot_product / norm_u_squared
        projection = scalar_proj * u
    
    calculations = [
        html.H5("投影计算结果", style={'color': '#FFD700'}),
        html.P(f"向量 AB = ({AB[0]:.1f}, {AB[1]:.1f})", style={'color': COLORS['vector_a']}),
        html.P(f"投影方向 u = ({u[0]:.1f}, {u[1]:.1f})", style={'color': COLORS['vector_b']}),
        html.P(f"投影标量: (AB·u)/|u|² = {scalar_proj:.2f}", style={'color': 'white'}),
        html.P(f"投影向量: ({projection[0]:.2f}, {projection[1]:.2f})", style={'color': COLORS['vector_sum']}),
        html.Hr(style={'borderColor': '#444444'}),
        html.P("投影公式:", style={'color': 'white', 'fontWeight': 'bold'}),
        html.P("Prj<sub>u</sub>AB = (AB·u)/|u|² · u", style={'color': '#FFD700', 'fontStyle': 'italic'})
    ]
    
    return fig, calculations

    # ======== 运行应用 ========
if __name__ == '__main__':
    app.run(debug=True, port=8050)