import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import sympy as sp
import matplotlib as mpl

# 设置中文字体支持
mpl.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei'] 
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['mathtext.fontset'] = 'cm'  # 优化数学符号显示

class DerivativeVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.35)
        self._setup_controls()
        self._update_function('x**2')
    
    def _parse_function(self, expr):
        """解析函数并确定定义域"""
        if not expr.strip(): return None
        
        try:
            x = sp.symbols('x')
            f_expr = sp.sympify(expr)
            f = sp.lambdify(x, f_expr, 'numpy')
            f_prime = sp.lambdify(x, f_expr.diff(x), 'numpy')
            
            # 智能定义域检测
            domain = (-5, 5)
            expr_lower = expr.lower()
            if 'log' in expr_lower or 'ln' in expr_lower: domain = (0.1, 5)
            elif 'sqrt' in expr_lower: domain = (0, 5)
            elif 'tan' in expr_lower: domain = (-1.4, 1.4)
            elif 'asin' in expr_lower or 'acos' in expr_lower: domain = (-1, 1)
            elif '1/x' in expr_lower or '/x' in expr_lower: 
                domain = (0.1, 5) if '-x' not in expr else (-5, -0.1)
            
            return {
                'f': f, 'f_prime': f_prime, 'domain': domain,
                'title': f"$f(x) = {sp.latex(f_expr)}$",
                'derivative': f"$f'(x) = {sp.latex(f_expr.diff(x))}$",
                'raw_expr': expr
            }
        except:
            return None

    def _setup_controls(self):
        """设置交互控件"""
        # 函数输入框
        self.func_input = TextBox(plt.axes([0.25, 0.2, 0.6, 0.05]), 
                                 '输入函数:', initial='x**2')
        self.func_input.on_submit(self._update_function)
        
        # 参数滑块
        self.a_slider = Slider(plt.axes([0.25, 0.15, 0.6, 0.03]), 
                              '点 a', -5, 5, valinit=0)
        self.h_slider = Slider(plt.axes([0.25, 0.1, 0.6, 0.03]), 
                              '距离 h', -1, 1, valinit=0.5)
        
        self.a_slider.on_changed(self._update_plot)
        self.h_slider.on_changed(self._update_plot)
        
        # 功能按钮，调整尺寸：[左, 下, 宽, 高] ，这里缩小了宽度和高度
        self.example_btn = Button(plt.axes([0.05, 0.25, 0.12, 0.04]), '示例函数')  
        self.example_btn.on_clicked(self._load_example)
        
        self.animate_btn = Button(plt.axes([0.05, 0.18, 0.12, 0.04]), 'h→0动画') 
        self.animate_btn.on_clicked(self._animate_h)

    def _load_example(self, event=None):
        """加载随机示例函数"""
        examples = [
            "sin(x)", "cos(x)", "exp(x)", "log(x)", "sqrt(x)", "1/x",
            "x**2", "x**3", "tan(x)", "1/(1+x**2)", "exp(-x**2)"
        ]
        self.func_input.set_val(np.random.choice(examples))
        self._update_function(self.func_input.text)

    def _animate_h(self, event=None):
        """演示h趋近于0的动画（减慢速度）"""
        if not hasattr(self, 'custom_func'): return
            
        h_vals = np.concatenate([
            np.linspace(self.h_slider.val, np.sign(self.h_slider.val)*0.1, 15),
            np.linspace(np.sign(self.h_slider.val)*0.1, 0.001, 10)
        ])
        
        for h in h_vals:
            self.h_slider.set_val(h)
            plt.pause(0.15)  # 延长暂停时间，减慢动画速度

    def _update_function(self, expr):
        """更新函数并刷新视图"""
        self.custom_func = self._parse_function(expr)
        if self.custom_func:
            xmin, xmax = self.custom_func['domain']
            self.a_slider.valmin, self.a_slider.valmax = xmin, xmax
            self.a_slider.set_val((xmin + xmax)/2)
            self._update_plot()
        else:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "函数解析错误", 
                         ha='center', va='center', color='red', fontsize=14)
            self.fig.canvas.draw_idle()

    def _update_plot(self, event=None):
        """更新主绘图（优化注释显示，去掉左上角函数名）"""
        if not hasattr(self, 'custom_func') or not self.custom_func: return
            
        self.ax.clear()
        a, h = self.a_slider.val, self.h_slider.val
        f, f_prime = self.custom_func['f'], self.custom_func['f_prime']
        xmin, xmax = self.custom_func['domain']
        
        # 绘制函数曲线
        x = np.linspace(xmin, xmax, 500)
        self.ax.plot(x, f(x), 'b-', lw=2, label=self.custom_func['title'])
        
        # 计算关键点
        xA, xB = a, a + h
        yA, yB = f(xA), f(xB)
        slope_secant = (yB - yA)/(h or 1e-10)  # 避免除零错误
        slope_tangent = f_prime(a)
        
        # 绘制割线和切线（长度相同）
        tangent_x = np.linspace(a - 1, a + 1, 50)
        
        # 割线（使用与切线相同的x范围）
        self.ax.plot(tangent_x, yA + slope_secant * (tangent_x - a), 
                     'r--', label='割线')
        self.ax.scatter([xA, xB], [yA, yB], c='red', zorder=5)
        
        # 切线
        self.ax.plot(tangent_x, yA + slope_tangent * (tangent_x - a), 
                     'g-', label='切线')
        
        # 添加点坐标标注
        self.ax.text(xA, yA, f'({xA:.2f}, {yA:.2f})', fontsize=9, 
                     ha='right', va='top' if yA < yB else 'bottom',
                     bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8))
        
        self.ax.text(xB, yB, f'({xB:.2f}, {yB:.2f})', fontsize=9, 
                     ha='left', va='bottom' if yA < yB else 'top',
                     bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8))
        
        # 左上角信息框（去掉函数名，仅保留关键信息）
        info_text = (f"导函数: {self.custom_func['derivative']}\n"
                     f"在 x={a:.2f} 处的导数: $\\mathbf{{{slope_tangent:.4f}}}$，定义式: $\\lim_{{h \\to 0}} \\frac{{f(a+h)-f(a)}}{{h}}$")
        
        self.ax.text(0.05, 0.95, info_text, transform=self.ax.transAxes,
                     fontsize=8.5, va='top', bbox=dict(boxstyle='round', fc='wheat', alpha=0.8))
        
        # 右下角斜率信息（增加切线斜率并加粗显示）
        if abs(h) > 1e-5:
            frac = f"$\\frac{{{yB:.2f}-{yA:.2f}}}{{{h:.2f}}}$"
            self.ax.text(0.95, 0.05, 
                         f"割线斜率: $\\mathbf{{{slope_secant:.4f}}}$ ({frac})，"
                         f"切线斜率: $\\mathbf{{{slope_tangent:.4f}}}$", 
                         transform=self.ax.transAxes, fontsize=10, ha='right',
                         bbox=dict(boxstyle='round', fc='lightyellow', alpha=0.7))
        
        # 添加局部放大视图
        ax_inset = self.ax.inset_axes([0.65, 0.65, 0.3, 0.25])
        ax_inset.plot(x, f(x), 'b-', lw=1.5)
        
        # 在局部放大视图中绘制割线和切线（使用相同的范围）
        ax_inset.plot(tangent_x, yA + slope_secant * (tangent_x - a), 'r--')
        ax_inset.plot(tangent_x, yA + slope_tangent * (tangent_x - a), 'g-')
        ax_inset.scatter([xA, xB], [yA, yB], c='red', s=30)
        
        margin = max(0.5, abs(h) * 3)
        ax_inset.set_xlim(a - margin, a + margin)
        ax_inset.set_ylim(yA - margin, yA + margin)
        ax_inset.grid(True, ls='--', alpha=0.5)
        ax_inset.set_title('局部放大', fontsize=8)
        
        # 设置图形属性
        self.ax.set(xlim=(xmin, xmax), title='导数可视化工具')
        self.ax.legend(loc='upper right', fontsize=9)
        self.ax.grid(True)
        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    dv = DerivativeVisualizer()
    plt.show()