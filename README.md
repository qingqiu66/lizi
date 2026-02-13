# 🌌 Cyber Particles (赛博粒子交互系统)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Three.js](https://img.shields.io/badge/Three.js-r160-00f3ff)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-ff0055)

一个基于 WebGL 和 AI 手势识别的赛博朋克风格交互式粒子系统。用户可以通过手势实时控制数万个粒子的爆发与聚合。

---
## 🎮 演示 / Demo
[点击这里查看在线演示](https://github.com/qingqiu66/lizi)

## ✨ 核心特性 / Features

* **动态粒子变换 (Morphing)**：支持将自定义文字或上传的图片实时转化为 3D 粒子点云。
* **AI 手势视觉控制**：集成 Google MediaPipe 机器学习模型，通过摄像头实现无接触交互：
    * 🖐 **张开手掌**：粒子受力场影响爆发散开。
    * ✊ **紧握拳头**：粒子受到引力吸引，精准还原目标形状。
* **极致视觉美学**：
    * **后处理辉光**：使用 UnrealBloomPass 实现霓虹灯般的溢光效果。
    * **自定义 Shader**：底层通过 GLSL 编写顶点/片元着色器，保证 50,000+ 粒子稳定 60帧运行。
* **赛博朋克 UI**：基于毛玻璃材质（Glassmorphism）的系统启动界面。

---

## 🛠 技术栈 / Technical Stack

### 1. 图形渲染层 (Graphics)
* **Three.js (r160)**：负责 3D 场景管理、相机系统及渲染管线。
* **GLSL Shaders**：自定义着色器实现粒子平滑插值算法：
    * `mix(aRandom, aTarget, uProgress)`：在混沌状态与目标形状间进行线性插值。
    * **粒子呼吸效果**：在顶点着色器中加入 $sin(uTime)$ 函数实现粒子的微弱浮动。
* **后处理 (Post-Processing)**：使用 `EffectComposer` 叠加 `UnrealBloomPass`，通过降低阈值（Threshold）获取更纯净的黑背景发光感。

### 2. 计算机视觉层 (Computer Vision)
* **MediaPipe Hands**：实时追踪手部 21 个骨骼关键点。
* **手势算法逻辑**：
    * 通过计算 **中指尖 (Landmark 12)** 到 **腕部 (Landmark 0)** 的欧式距离，对比 **掌心宽度** 的比例值，实现抗干扰的手势识别。
    * 引入 **数值平滑滤波器**，公式为：$Current = Current + (Target - Current) \times 0.08$，确保粒子变换不随手部抖动而闪烁。

### 3. 数据处理层 (Data Processing)
* **Canvas 采样**：利用离屏 Canvas 绘制文字或图片，通过 `getImageData` 获取像素矩阵，将 2D 坐标映射为 3D 空间坐标点。

---

## 🚀 快速开始 / Quick Start

1.  **克隆项目**
    ```bash
    git clone [https://github.com/qingqiu66/lizi.git](https://github.com/qingqiu66/lizi.git)
    ```
2.  **本地运行**
    由于项目采用 ES Modules 并需要摄像头权限，请在本地服务器环境下打开（如使用 VSCode Live Server 插件）。
    或者使用 Python：
    ```bash
    python -m http.server 8000
    ```
3.  **使用提示**：
    * 启动时可输入任意文字。
    * 上传带有透明通道的 PNG 图片效果更佳。

---

## 📁 目录结构 / Project Structure

* `index.html` - 核心逻辑、样式与渲染引擎集成。
* `README.md` - 项目说明文档。

---

## 📄 开源协议 / License

本项目采用 [MIT License](LICENSE)。
