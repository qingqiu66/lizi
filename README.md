# 赛博粒子 (Cyber Particle) 🌌

一个基于 **Three.js** 和 **MediaPipe** 的高性能粒子可视化交互系统。通过摄像头捕捉手势，实现与数万个粒子的实时互动，支持自定义文字和图像生成。

---

## ✨ 核心特性

- **🚀 高性能渲染**：利用 WebGL 和 Three.js 渲染超过 50,000 个粒子，保持流畅的帧率。
- **🖐 手势交互**：集成 MediaPipe Hands，支持通过手势控制粒子形态：
  - **张手 (Open Hand)**：粒子爆发散开。
  - **握拳 (Fist)**：粒子聚合形成目标形状。
- **🎨 自定义内容**：
  - 支持输入任意文字生成粒子阵列。
  - 支持上传本地图片，将其轮廓转化为动态粒子。
- **🖥 控制台管理**：内置基于 Python Webview 的 GUI 控制台，集成：
  - 本地 HTTP 服务一键启停。
  - 实时系统日志查看。
  - 在线代码编辑器（Ace Editor），可直接修改前端逻辑。
- **🌈 视觉特效**：内置 UnrealBloom 高级发光滤镜，营造赛博朋克视觉氛围。

---

## 🛠 技术栈

- **前端**：
  - [Three.js](https://threejs.org/) - 3D 粒子引擎
  - [MediaPipe](https://google.github.io/mediapipe/) - 实时手势识别
  - [MDUI 2](https://www.mdui.org/) - 响应式控制台界面
  - [Ace Editor](https://ace.c9.io/) - 内置代码编辑器
- **后端**：
  - [Python 3.11.9](https://www.python.org/) - 逻辑控制与服务分发
  - [PyWebView](https://pywebview.flowrl.com/) - 跨平台桌面窗口容器
  - [HTTP Server](https://docs.python.org/3/library/http.server.html) - 本地静态资源托管

---

## 🚀 快速开始

### 方式一：源码运行
1. **安装依赖**：
   ```bash
   pip install pywebview
   ```
2. **启动应用**：
   ```bash
   python run.py
   ```
3. **访问页面**：
   - 应用启动后会自动打开控制台窗口。
   - 点击控制台中的“启动服务”按钮。
   - 点击“浏览器打开”或手动访问 `http://localhost:8001`。

### 方式二：自行打包 (PyInstaller)
如果你想自行打包成 `.exe` 文件：
1. **安装 PyInstaller**：
   ```bash
   pip install pyinstaller
   ```
2. **执行打包命令**：
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon "app.ico" --add-data "dash.html;." --add-data "index.html;." "run.py"
   ```
   - `--onefile`: 打包成单个可执行文件。
   - `--windowed`: 运行时不显示控制台窗口。
   - `--add-data`: 将 HTML 资源文件打包进可执行程序。

3. **运行可执行文件**：
   - 在 `dist` 目录下找到生成的可执行文件，双击运行即可。
   - 应用启动后会自动打开控制台窗口，并启动本地服务。

---

## 🎨 界面预览
---

## 📖 使用指南

1. **初始化**：在启动弹窗中输入你想要显示的文字，或上传一张对比度明显的图片。
2. **授权摄像头**：浏览器会请求摄像头权限，请点击“允许”以启用手势识别。
3. **交互**：
   - 将手置于摄像头前，左上角预览框会显示识别状态。
   - 尝试**握拳**和**张手**，观察粒子的聚合与爆发。
4. **自定义**：通过控制台的“代码编辑”功能，你可以实时修改 `index.html` 中的粒子颜色、密度或动画逻辑。

---

## 📂 项目结构

```text
.              # 编译后的可执行文件
├── run.py              # Python 后端主程序
├── index.html          # 粒子交互前端主页面
├── dash.html           # GUI 控制台页面
├── app.ico             # 应用图标
└── README.md           # 项目说明文档
```

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源。