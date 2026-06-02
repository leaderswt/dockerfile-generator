#!/bin/bash

# 🐳 Dockerfile生成器启动脚本

echo "============================================================"
echo "           🐳 Dockerfile生成器启动脚本"
echo "============================================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未检测到Python3，请先安装Python 3.8+"
    echo "   下载地址：https://www.python.org/downloads/"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖..."
if ! pip show flask &> /dev/null; then
    echo "📥 正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

echo "✅ 依赖检查完成"
echo ""
echo "🚀 正在启动Dockerfile生成器..."
echo ""
echo "📍 访问地址: http://127.0.0.1:5000"
echo "📖 按 Ctrl+C 停止服务"
echo "============================================================"
echo ""

python3 app.py
