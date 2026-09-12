# 高等数学可视化教学工具集

一组面向课堂的高等数学可视化工具：4 个可直接在浏览器打开的交互网页，3 个 Python 交互程序。全部围绕"把抽象定义画出来"这一个目标——极限过程、微元、向量运算、曲线积分，学生看得见就更容易讲清楚。

所有页面与程序均为中文界面，可直接用于课堂演示。`materials/` 里还记录了这些页面是怎么用 AI 一轮轮改出来的。

## 在线演示

**<https://signfff.github.io/visual-calculus/>** — 网页部分是纯前端，点开即用，无需安装。

| 页面 | 内容 |
| --- | --- |
| [映射与函数](https://signfff.github.io/visual-calculus/mapping-and-function.html) | 并排对比一般映射、单射、满射、双射，动画演示逆映射存在的条件 |
| [格林公式](https://signfff.github.io/visual-calculus/greens-theorem.html) | 曲线积分与二重积分的实时数值对照，解释两者为何相等 |
| [对坐标的曲线积分](https://signfff.github.io/visual-calculus/line-integral.html) | 参数曲线上的几何图像与控制面板，观察 ∫P dx + Q dy 的累加过程 |
| [心形曲面](https://signfff.github.io/visual-calculus/heart-surface.html) | 参数方程 x = cos u·(2cos v − cos 2v) 的心形曲面海报 |

页面源码在 `docs/`，克隆后双击任意 `.html` 也能本地打开；格林公式与映射两页通过 CDN 加载 MathJax，需要联网才能正确渲染公式。

## Python 交互程序

| 程序 | 说明 | 技术栈 |
| --- | --- | --- |
| [`apps/derivative-definition`](apps/derivative-definition/derivative_visualizer.py) | 输入任意函数，拖动 `a` 与 `h` 观察割线趋向切线，附带局部放大视图和 h→0 动画 | matplotlib + sympy |
| [`apps/definite-integral`](apps/definite-integral/integral_visualizer.py) | 定积分元素法：矩形微元、黎曼和与真实积分值对照，支持分割过程动画 | PyQt5 + matplotlib |
| [`apps/vector-basics`](apps/vector-basics/app.py) | 向量概念、线性运算、空间直角坐标系、向量投影四个标签页 | Dash + Plotly |

### 运行

建议 Python 3.10 - 3.12（3.13 下 PyQt5 的预编译包可能尚不可用）。

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # Linux / macOS: source .venv/bin/activate
pip install -r requirements.txt
```

```powershell
python apps/derivative-definition/derivative_visualizer.py   # 桌面窗口
python apps/definite-integral/integral_visualizer.py         # 桌面窗口
python apps/vector-basics/app.py                             # 浏览器打开 http://127.0.0.1:8050
```

只跑其中一个程序时，可按 `requirements.txt` 里的注释分组只安装需要的依赖。

中文标签依赖系统里的 `SimHei` / `Microsoft YaHei` 字体；非 Windows 系统若出现方块乱码，安装任一中文字体后修改对应源码顶部的 `font.sans-serif` 即可。

### 打包成 exe

两个桌面程序可以打包成单文件 exe，方便在没装 Python 的教室电脑上运行：

```powershell
pip install pyinstaller
./scripts/build.ps1
```

产物在 `dist/` 下（`derivative_visualizer.exe`、`integral_visualizer.exe`，各 60 - 90 MB，因为把 matplotlib / Qt 一并打进去了）。`dist/` 已被 `.gitignore` 排除，不随仓库分发——需要的人从源码自行打包即可。

## 教学材料

可以仿照教程进行AI辅助开发，过程记录在 `materials/`：

| 文档 | 内容 |
| --- | --- |
| [AI+前端可视化高数知识点制作流程](materials/教程.pdf) | 8 页。以格林公式页面为例复盘全过程：从初始提示词到第六轮修改，怎么用 F12 定位要删的冗余盒子、怎么把"对齐""不要滚动""公式别写成 a/b"这类要求讲清楚、以及改多了之后 AI 会犯哪些低级错误 |
| [曲线积分可视化 · 课堂展示版设计说明](materials/课堂展示版设计说明.pdf) | 2 页。`line-integral.html` 的设计取舍与完整提示词，附提示词拆解建议：明确使用场景、保留项、删除项、视觉目标 |

## 目录结构

```
.
├── apps/                  Python 交互程序
│   ├── derivative-definition/
│   ├── definite-integral/
│   └── vector-basics/
├── docs/                  可视化网页（GitHub Pages 目录）
│   └── index.html         页面索引
├── materials/             教学文档（PDF）
│   ├── 教程.pdf
│   └── 课堂展示版设计说明.pdf
├── scripts/build.ps1      打包脚本
└── requirements.txt
```

## License

代码与文档以 MIT 许可发布，详见 [LICENSE](LICENSE)。用于教学、二次修改均无需额外授权。
