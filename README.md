# 🐳 Dockerfile生成器

一个功能强大、界面美观、小白友好的Dockerfile生成工具。

## ✨ 特性

- 🎨 **现代化界面**：采用深色主题设计，美观大方
- 🚀 **10+预设模板**：涵盖Python、Node.js、Java、Go、PHP等主流技术栈
- 📝 **实时预览**：配置更改即时生成Dockerfile
- 🎯 **智能提示**：根据选择自动配置最佳参数
- 📋 **一键复制**：快速复制生成的Dockerfile
- 🔒 **.dockerignore生成**：自动生成常用的.dockerignore文件
- 💡 **使用技巧**：提供Dockerfile编写最佳实践

## 🛠️ 技术栈

- **后端**：Flask (Python)
- **前端**：HTML5 + CSS3 + Vanilla JavaScript
- **代码高亮**：Highlight.js
- **无数据库**：轻量级设计

## 📦 安装

### 方式一：直接运行（推荐）

1. 确保已安装Python 3.8+

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python app.py
```

4. 打开浏览器访问：`http://127.0.0.1:5000`

### 方式二：使用Docker运行

1. 构建镜像：
```bash
docker build -t dockerfile-generator .
```

2. 运行容器：
```bash
docker run -p 5000:5000 dockerfile-generator
```

3. 打开浏览器访问：`http://localhost:5000`

## 🎯 快速开始

### 使用预设模板

1. 在首页选择一个技术栈预设（如Python Flask）
2. 点击卡片自动填充配置
3. 点击"生成 Dockerfile"按钮
4. 点击"下载"或"复制"获取结果

### 自定义配置

1. 选择基础镜像
2. 设置工作目录和端口
3. 选择包管理器
4. 添加环境变量（如需要）
5. 点击"生成 Dockerfile"

## 📖 功能说明

### 预设模板

| 模板 | 描述 | 基础镜像 |
|------|------|---------|
| 🐍 Python Flask | Flask Web应用 | Python 3.11 |
| 🐍 Python Django | Django Web应用 | Python 3.11 |
| 🟢 Node.js Express | Express后端API | Node.js 18 |
| 🟢 Node.js Next.js | Next.js全栈应用 | Node.js 18 |
| ☕ Java Spring | Spring Boot应用 | OpenJDK 17 |
| 🔷 Go Gin | Gin Web框架 | Go 1.21 |
| 🐘 PHP Laravel | Laravel应用 | PHP 8.2 |
| 🌐 Nginx静态网站 | 静态HTML/CSS/JS | Nginx Alpine |
| ⚛️ React + Vite | React前端应用 | Node.js 18 |
| 💚 Vue + Vite | Vue前端应用 | Node.js 18 |

### 配置选项

#### 基础配置
- **维护者**：Dockerfile的MAINTAINER信息
- **基础镜像**：应用运行的操作系统和语言环境
- **工作目录**：应用代码存放位置
- **暴露端口**：容器对外开放的端口

#### 依赖管理
- **pip**：Python项目（需要requirements.txt）
- **npm**：Node.js项目（需要package.json）
- **Composer**：PHP项目（需要composer.json）
- **Maven**：Java项目（需要pom.xml）
- **Go Modules**：Go项目

#### 环境变量
- 添加键值对形式的环境变量
- 支持多个变量

#### 高级选项
- **系统依赖**：额外的系统包安装
- **应用代码目录**：源代码位置
- **健康检查**：容器健康检查命令
- **启动命令**：容器启动命令
- **框架类型**：自动设置最佳启动命令

## 🎨 界面预览

### 深色主题设计
采用GitHub Dark主题风格，保护眼睛，适合长时间使用。

### 响应式布局
支持桌面、平板、手机等设备访问。

### 代码高亮
使用Highlight.js实现Dockerfile语法高亮，提高可读性。

## 💡 使用技巧

### 1. 选择轻量级镜像
```
推荐：python:3.11-slim
不推荐：python:3.11
```
slim和alpine版本体积更小，安全性更高。

### 2. 使用.dockerignore
排除不需要的文件和目录：
- node_modules
- __pycache__
- .git
- *.log

### 3. 多阶段构建
对于编译型语言，使用多阶段构建可以减小最终镜像体积。

### 4. 优化层缓存
将不常变化的步骤（如依赖安装）放在前面。

## 🔧 API接口

### 生成Dockerfile
```
POST /api/generate
Content-Type: application/json

{
    "base_image": "python:3.11-slim",
    "work_dir": "/app",
    "port": "5000",
    "package_manager": "pip",
    "requirements_file": "requirements.txt"
}
```

### 获取预设列表
```
GET /api/presets
```

### 获取特定预设
```
GET /api/preset/<preset_id>
```

### 生成.dockerignore
```
POST /api/dockerignore
```

### 下载Dockerfile
```
POST /api/download
Content-Type: application/json

{
    "base_image": "...",
    ...
}
```

### 验证配置
```
POST /api/validate
Content-Type: application/json

{
    ...
}
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📝 许可证

MIT License

## 🙏 致谢

- Flask框架
- Highlight.js代码高亮
- GitHub Dark主题设计灵感

---

**Made with ❤️ by AI Assistant**
