# 🐳 Dockerfile Generator

> 🤖 **AI-Assisted Development Project** - Developed by AI programming assistant (SOLO), automatically generating complete features from natural language requirements.

## 🌐 Language Switch

[![English](https://img.shields.io/badge/English-blue?style=flat-square)](README_en.md)
[![日本語](https://img.shields.io/badge/日本語-red?style=flat-square)](README_ja.md)
[![简体中文](https://img.shields.io/badge/简体中文-green?style=flat-square)](README.md)

A powerful, beautiful, and beginner-friendly Dockerfile generation tool.

## ✨ Features

- 🎨 **Modern UI**: Dark theme design, elegant and beautiful
- 🚀 **10+ Preset Templates**: Covering Python, Node.js, Java, Go, PHP and other mainstream tech stacks
- 📝 **Real-time Preview**: Generate Dockerfile instantly as you configure
- 🎯 **Smart Hints**: Automatically configure optimal parameters based on selection
- 📋 **One-click Copy**: Quickly copy the generated Dockerfile
- 🔒 **.dockerignore Generation**: Auto-generate common .dockerignore files
- 💡 **Usage Tips**: Provide Dockerfile best practices

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Syntax Highlighting**: Highlight.js
- **No Database**: Lightweight design

## 📦 Installation

### Method 1: Direct Run (Recommended)

1. Ensure Python 3.8+ is installed

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open browser: `http://127.0.0.1:5000`

### Method 2: Using Docker

1. Build the image:
```bash
docker build -t dockerfile-generator .
```

2. Run the container:
```bash
docker run -p 5000:5000 dockerfile-generator
```

3. Open browser: `http://localhost:5000`

## 🎯 Quick Start

### Using Preset Templates

1. Select a tech stack preset on the home page (e.g., Python Flask)
2. Click the card to auto-fill the configuration
3. Click the "Generate Dockerfile" button
4. Click "Download" or "Copy" to get the result

### Custom Configuration

1. Select base image
2. Set working directory and port
3. Choose package manager
4. Add environment variables (if needed)
5. Click "Generate Dockerfile"

## 📖 Features

### Preset Templates

| Template | Description | Base Image |
|----------|-------------|------------|
| 🐍 Python Flask | Flask Web App | Python 3.11 |
| 🐍 Python Django | Django Web App | Python 3.11 |
| 🟢 Node.js Express | Express Backend API | Node.js 18 |
| 🟢 Node.js Next.js | Next.js Full-stack | Node.js 18 |
| ☕ Java Spring | Spring Boot App | OpenJDK 17 |
| 🔷 Go Gin | Gin Web Framework | Go 1.21 |
| 🐘 PHP Laravel | Laravel App | PHP 8.2 |
| 🌐 Nginx Static | Static HTML/CSS/JS | Nginx Alpine |
| ⚛️ React + Vite | React Frontend | Node.js 18 |
| 💚 Vue + Vite | Vue Frontend | Node.js 18 |

### Configuration Options

#### Basic Configuration
- **Maintainer**: Dockerfile MAINTAINER info
- **Base Image**: OS and language environment for the application
- **Working Directory**: Location for application code
- **Exposed Port**: Port exposed by the container

#### Dependency Management
- **pip**: Python projects (requires requirements.txt)
- **npm**: Node.js projects (requires package.json)
- **Composer**: PHP projects (requires composer.json)
- **Maven**: Java projects (requires pom.xml)
- **Go Modules**: Go projects

#### Environment Variables
- Add environment variables as key-value pairs
- Support multiple variables

#### Advanced Options
- **System Dependencies**: Additional system packages to install
- **Application Code Directory**: Source code location
- **Health Check**: Container health check command
- **Start Command**: Container start command
- **Framework Type**: Automatically set optimal start command

## 🎨 Interface Preview

### Dark Theme Design
GitHub Dark theme style, easy on the eyes, suitable for long-time use.

### Responsive Layout
Supports desktop, tablet, and mobile devices.

### Code Highlighting
Highlight.js for Dockerfile syntax highlighting, improving readability.

## 💡 Usage Tips

### 1. Choose Lightweight Images
```
Recommended: python:3.11-slim
Not recommended: python:3.11
```
slim and alpine versions are smaller and more secure.

### 2. Use .dockerignore
Exclude unnecessary files and directories:
- node_modules
- __pycache__
- .git
- *.log

### 3. Multi-stage Build
For compiled languages, multi-stage builds can reduce final image size.

### 4. Optimize Layer Caching
Put infrequently changing steps (like dependency installation) at the front.

## 🔧 API Endpoints

### Generate Dockerfile
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

### Get Presets List
```
GET /api/presets
```

### Get Specific Preset
```
GET /api/preset/<preset_id>
```

### Generate .dockerignore
```
POST /api/dockerignore
```

### Download Dockerfile
```
POST /api/download
Content-Type: application/json

{
    "base_image": "...",
    ...
}
```

### Validate Configuration
```
POST /api/validate
Content-Type: application/json

{
    ...
}
```

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📝 License

MIT License

## 🙏 Acknowledgments

- **SOLO** - AI Programming Assistant, driving the project's design and implementation throughout
- Flask Framework
- Highlight.js for code highlighting
- GitHub Dark theme design inspiration

---

**🤖 AI Generated & Developed by SOLO**
