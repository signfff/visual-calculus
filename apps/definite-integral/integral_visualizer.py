import sys
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QGroupBox, QRadioButton,
    QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# 解决中文乱码问题
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class IntegrationVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("定积分元素法可视化工具")
        self.setGeometry(100, 100, 1000, 800)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QGroupBox {
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 1ex;
                color: #ecf0f1;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #3498db;
            }
            QLabel { color: #ecf0f1; }
            QLineEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1c6ea4; }
            QRadioButton { color: #ecf0f1; }
        """)
        
        # 创建主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题
        title_label = QLabel("定积分元素法可视化工具")
        title_label.setFont(QFont("SimHei", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #3498db; padding: 10px;")
        main_layout.addWidget(title_label)
        
        # 输入部分
        input_group = QGroupBox("积分参数设置")
        input_layout = QFormLayout()
        input_layout.setSpacing(10)
        
        # 函数输入
        self.function_input = QLineEdit("x**2")
        self.function_input.setPlaceholderText("输入函数表达式，例如：x**2, sin(x), exp(x)")
        input_layout.addRow(QLabel("函数 f(x):"), self.function_input)
        
        # 积分区间
        interval_layout = QHBoxLayout()
        self.lower_bound_input = QLineEdit("0")
        self.lower_bound_input.setFixedWidth(80)
        self.upper_bound_input = QLineEdit("1")
        self.upper_bound_input.setFixedWidth(80)
        interval_layout.addWidget(self.lower_bound_input)
        interval_layout.addWidget(QLabel("到"))
        interval_layout.addWidget(self.upper_bound_input)
        interval_layout.addStretch()
        input_layout.addRow(QLabel("积分区间:"), interval_layout)
        
        # 分割数
        self.partitions_input = QLineEdit("10")
        self.partitions_input.setFixedWidth(80)
        input_layout.addRow(QLabel("分割数:"), self.partitions_input)
        
        # 可视化选项
        self.static_radio = QRadioButton("静态图")
        self.static_radio.setChecked(True)
        self.animation_radio = QRadioButton("动态图")
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.static_radio)
        options_layout.addWidget(self.animation_radio)
        input_layout.addRow(QLabel("可视化选项:"), options_layout)
        
        # 按钮
        self.plot_button = QPushButton("绘制积分图")
        self.plot_button.clicked.connect(self.plot_integration)
        input_layout.addRow(self.plot_button)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # 绘图区域
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_facecolor('#f0f0f0')
        self.figure.tight_layout(pad=3.0)
        main_layout.addWidget(self.canvas, 1)
        
        # 状态栏
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("background-color: #34495e; color: #ecf0f1;")
        self.status_bar.showMessage("就绪 - 输入参数后点击'绘制积分图'按钮")
        
        # 初始化变量
        self.animation = None
        self.true_integral = 0

    def plot_integration(self):
        # 清除之前的动画
        if self.animation:
            self.animation.event_source.stop()
            self.animation = None
        
        try:
            # 获取用户输入
            func_expr = self.function_input.text()
            lower_bound = float(self.lower_bound_input.text())
            upper_bound = float(self.upper_bound_input.text())
            partitions = int(self.partitions_input.text())
            
            if lower_bound >= upper_bound:
                raise ValueError("积分区间下限必须小于上限")
            
            if partitions <= 0:
                raise ValueError("分割数必须大于0")
            
            # 定义函数
            def f(x):
                return eval(func_expr, {"__builtins__": None}, 
                           {"x": x, "sin": np.sin, "cos": np.cos, 
                            "tan": np.tan, "exp": np.exp, "log": np.log, 
                            "sqrt": np.sqrt, "pi": np.pi})
            
            # 生成x值
            x = np.linspace(lower_bound - 0.2, upper_bound + 0.2, 1000)
            y = f(x)
            
            # 清除之前的绘图
            self.ax.clear()
            
            # 绘制函数曲线
            self.ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {func_expr}')
            
            # 设置坐标轴范围
            self.ax.set_xlim([lower_bound - 0.2, upper_bound + 0.2])
            y_min, y_max = min(y), max(y)
            self.ax.set_ylim([min(0, y_min) - 0.1, max(0, y_max) + 0.1])
            
            # 绘制坐标轴
            self.ax.axhline(0, color='black', linewidth=0.8)
            self.ax.axvline(0, color='black', linewidth=0.8)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # 绘制积分区域
            integral_x = np.linspace(lower_bound, upper_bound, 100)
            self.ax.fill_between(integral_x, f(integral_x), color='skyblue', alpha=0.3, label='积分区域')
            
            # 计算真实积分值
            self.true_integral = np.trapz(f(integral_x), integral_x)
            
            # 根据选择的模式绘制
            if self.static_radio.isChecked():
                # 静态图模式
                self.draw_static_integration(f, lower_bound, upper_bound, partitions)
                self.ax.set_title(f'定积分元素法可视化 (分割数: {partitions})', fontsize=16)
            else:
                # 动态图模式
                self.ax.set_title('分割过程演示 (n = 分割数)', fontsize=16)
                
                # 创建动画
                self.animation = FuncAnimation(
                    self.figure, 
                    lambda frame: self.update_animation(frame, f, lower_bound, upper_bound, partitions),
                    frames=range(1, partitions + 1),
                    interval=500, 
                    repeat=False
                )
            
            # 添加图例和标签
            self.ax.legend(loc='upper left')
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            
            # 刷新画布
            self.canvas.draw()
            
            # 更新状态栏
            self.status_bar.showMessage(f"绘图完成 - 积分区间: [{lower_bound}, {upper_bound}], 分割数: {partitions}, 真实积分值: {self.true_integral:.4f}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"输入错误: {str(e)}")
            self.status_bar.showMessage(f"错误: {str(e)}")
    
    def draw_static_integration(self, f, lower_bound, upper_bound, partitions):
        """绘制静态积分图"""
        # 绘制积分元素
        xi = (lower_bound + upper_bound) / 2
        dx = (upper_bound - lower_bound) / 10
        dy = f(xi)
        
        # 添加矩形微元
        rect = Rectangle((xi, 0), dx, dy, fill=False, edgecolor='red', linewidth=2, hatch='//')
        self.ax.add_patch(rect)
        
        # 添加标注
        self.ax.annotate('微元面积 $dA = f(x)dx$', 
                        xy=(xi + dx/2, dy/2), 
                        xytext=(xi + 0.3, dy/2 - 0.1),
                        arrowprops=dict(arrowstyle="->", color='red'),
                        fontsize=12, color='red')
        
        self.ax.annotate(r'$dx$', xy=(xi + dx/2, 0), 
                        xytext=(xi + dx/2, -0.05), 
                        ha='center', fontsize=12)
        
        self.ax.annotate(r'$dy = f(x)$', xy=(xi + dx, dy/2), 
                        xytext=(xi + dx + 0.05, dy/2), 
                        va='center', fontsize=12)
        
        # 显示积分表达式
        self.ax.text(0.05, 0.95, 
                    f'矩形面积和: {self.calculate_riemann_sum(f, lower_bound, upper_bound, partitions):.4f}\n'
                    f'真实积分值: {self.true_integral:.4f}', 
                    transform=self.ax.transAxes, fontsize=12, 
                    bbox=dict(facecolor='white', alpha=0.8))
    
    def update_animation(self, frame, f, lower_bound, upper_bound, max_partitions):
        """动画更新函数（用于动态图）"""
        # 清除当前矩形
        for patch in self.ax.patches:
            if isinstance(patch, Rectangle):
                patch.remove()
        
        # 清除文本
        for text in self.ax.texts:
            if text.get_text().startswith('矩形面积和') or text.get_text().startswith('分割过程'):
                text.remove()
        
        # 更新标题
        self.ax.set_title(f'分割过程演示 (n = {frame})', fontsize=16)
        
        # 绘制矩形微元
        dx = (upper_bound - lower_bound) / frame
        total_area = 0
        
        for i in range(frame):
            x_left = lower_bound + i * dx
            height = f(x_left + dx)  # 右端点高度
            rect = Rectangle((x_left, 0), dx, height, 
                            fill=True, alpha=0.3, edgecolor='r', facecolor='orange')
            self.ax.add_patch(rect)
            total_area += dx * height
        
        # 显示当前积分近似值
        self.ax.text(0.05, 0.95, 
                    f'矩形面积和: {total_area:.4f}\n'
                    f'真实积分值: {self.true_integral:.4f}', 
                    transform=self.ax.transAxes, fontsize=12, 
                    bbox=dict(facecolor='white', alpha=0.8))
    
    def calculate_riemann_sum(self, f, lower_bound, upper_bound, partitions):
        """计算黎曼和（右端点法）"""
        dx = (upper_bound - lower_bound) / partitions
        total = 0
        for i in range(partitions):
            x = lower_bound + (i + 1) * dx  # 右端点
            total += f(x) * dx
        return total

    def closeEvent(self, event):
        # 关闭时停止动画
        if self.animation:
            self.animation.event_source.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegrationVisualizer()
    window.show()
    sys.exit(app.exec_())