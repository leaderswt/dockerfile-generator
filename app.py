"""
Dockerfile生成器 - 图形界面工具
功能强大、界面美观、小白友好的Dockerfile生成工具
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import json
import os
from datetime import datetime

# 导入高级功能
from advanced_features import register_advanced_routes

app = Flask(__name__)

# 注册高级功能路由
register_advanced_routes(app)

# 静态文件路由 - 用于i18n.js（使用/i18n路径避免与Flask默认static冲突）
@app.route('/i18n/<path:filename>')
def i18n_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'translations'), filename)

# 预设模板配置
PRESETS = {
    # Python 生态
    'python-flask': {
        'name': '🐍 Python Flask',
        'description': '适合Python Flask Web应用',
        'base_image': 'python:3.12-slim',
        'package_manager': 'pip',
        'port': '5000',
        'framework': 'flask'
    },
    'python-django': {
        'name': '🐍 Python Django',
        'description': '适合Python Django应用',
        'base_image': 'python:3.12-slim',
        'package_manager': 'pip',
        'port': '8000',
        'framework': 'django'
    },
    'python-fastapi': {
        'name': '⚡ Python FastAPI',
        'description': '高性能Python异步API框架',
        'base_image': 'python:3.12-slim',
        'package_manager': 'pip',
        'port': '8000',
        'framework': 'fastapi'
    },
    
    # Node.js 生态
    'node-express': {
        'name': '🟢 Node.js Express',
        'description': '适合Node.js Express应用',
        'base_image': 'node:22-alpine',
        'package_manager': 'npm',
        'port': '3000',
        'framework': 'express'
    },
    'node-nextjs': {
        'name': '🟢 Node.js Next.js',
        'description': '适合Next.js全栈应用',
        'base_image': 'node:22-alpine',
        'package_manager': 'npm',
        'port': '3000',
        'framework': 'nextjs'
    },
    'node-nestjs': {
        'name': '🔺 Node.js NestJS',
        'description': '企业级Node.js框架',
        'base_image': 'node:22-alpine',
        'package_manager': 'npm',
        'port': '3000',
        'framework': 'nestjs'
    },
    'react-vite': {
        'name': '⚛️ React + Vite',
        'description': 'React前端应用',
        'base_image': 'node:22-alpine',
        'package_manager': 'npm',
        'port': '5173',
        'framework': 'react'
    },
    'vue-vite': {
        'name': '💚 Vue + Vite',
        'description': 'Vue前端应用',
        'base_image': 'node:22-alpine',
        'package_manager': 'npm',
        'port': '5173',
        'framework': 'vue'
    },
    
    # Java 生态
    'java-spring': {
        'name': '☕ Java Spring Boot',
        'description': '适合Java Spring Boot应用',
        'base_image': 'eclipse-temurin:21-jdk-alpine',
        'package_manager': 'maven',
        'port': '8080',
        'framework': 'spring'
    },
    
    # Go 生态
    'go-gin': {
        'name': '🔷 Go Gin',
        'description': 'Go Web框架',
        'base_image': 'golang:1.23-alpine',
        'package_manager': 'go',
        'port': '8080',
        'framework': 'gin'
    },
    'go-fiber': {
        'name': '🔷 Go Fiber',
        'description': '高性能Go Web框架',
        'base_image': 'golang:1.23-alpine',
        'package_manager': 'go',
        'port': '3000',
        'framework': 'fiber'
    },
    
    # PHP 生态
    'php-laravel': {
        'name': '🐘 PHP Laravel',
        'description': 'PHP Laravel应用',
        'base_image': 'php:8.3-apache',
        'package_manager': 'composer',
        'port': '80',
        'framework': 'laravel'
    },
    
    # Rust 生态
    'rust-actix': {
        'name': '🦀 Rust Actix',
        'description': '高性能Rust Web框架',
        'base_image': 'rust:1.75-slim',
        'package_manager': 'cargo',
        'port': '8080',
        'framework': 'actix'
    },
    
    # .NET 生态
    'dotnet-core': {
        'name': '🎯 .NET Core',
        'description': '跨平台.NET应用',
        'base_image': 'mcr.microsoft.com/dotnet/aspnet:8.0-alpine',
        'package_manager': 'dotnet',
        'port': '8080',
        'framework': 'dotnet'
    },
    
    # Ruby 生态
    'ruby-rails': {
        'name': '🔶 Ruby on Rails',
        'description': 'Ruby Web框架',
        'base_image': 'ruby:3.3-slim',
        'package_manager': 'bundler',
        'port': '3000',
        'framework': 'rails'
    },
    
    # 静态网站
    'nginx-static': {
        'name': '🌐 Nginx静态网站',
        'description': '静态HTML/CSS/JS网站',
        'base_image': 'nginx:alpine',
        'package_manager': 'none',
        'port': '80',
        'framework': 'static'
    }
}

# Dockerfile注释多语言翻译
DOCKERFILE_COMMENTS = {
    'zh': {
        'header': '# ==================================================\n# Dockerfile 生成器创建\n# 基础镜像: {image}\n# ==================================================',
        'base_image': '# 基础镜像',
        'maintainer': '# 维护者信息',
        'work_dir': '# 设置工作目录',
        'env_vars': '# 设置环境变量',
        'sys_packages': '# 安装系统依赖',
        'copy_deps': '# 复制依赖文件',
        'install_python_deps': '# 安装Python依赖',
        'copy_package_json': '# 复制package.json',
        'install_npm_deps': '# 安装npm依赖（生产环境）',
        'copy_composer': '# 复制composer文件',
        'install_composer_deps': '# 安装composer依赖',
        'copy_pom': '# 复制pom.xml',
        'download_maven_deps': '# 下载Maven依赖',
        'copy_source': '# 复制源代码',
        'copy_cargo': '# 复制Cargo文件',
        'build_rust': '# 构建Rust应用',
        'copy_csproj': '# 复制项目文件',
        'copy_gemfile': '# 复制Gemfile',
        'install_ruby_deps': '# 安装Ruby依赖',
        'copy_app_code': '# 复制应用代码',
        'create_user': '# 创建非root用户（安全最佳实践）',
        'set_permissions': '# 设置文件权限',
        'switch_user': '# 切换到非root用户',
        'expose_port': '# 暴露端口',
        'health_check': '# 健康检查',
        'start_cmd': '# 启动命令',
        'default_cmd': 'CMD ["echo", "请配置启动命令"]',
    },
    'en': {
        'header': '# ==================================================\n# Generated by Dockerfile Generator\n# Base image: {image}\n# ==================================================',
        'base_image': '# Base image',
        'maintainer': '# Maintainer info',
        'work_dir': '# Set working directory',
        'env_vars': '# Set environment variables',
        'sys_packages': '# Install system dependencies',
        'copy_deps': '# Copy dependency file',
        'install_python_deps': '# Install Python dependencies',
        'copy_package_json': '# Copy package.json',
        'install_npm_deps': '# Install npm dependencies (production)',
        'copy_composer': '# Copy composer files',
        'install_composer_deps': '# Install composer dependencies',
        'copy_pom': '# Copy pom.xml',
        'download_maven_deps': '# Download Maven dependencies',
        'copy_source': '# Copy source code',
        'copy_cargo': '# Copy Cargo files',
        'build_rust': '# Build Rust application',
        'copy_csproj': '# Copy project files',
        'copy_gemfile': '# Copy Gemfile',
        'install_ruby_deps': '# Install Ruby dependencies',
        'copy_app_code': '# Copy application code',
        'create_user': '# Create non-root user (security best practice)',
        'set_permissions': '# Set file permissions',
        'switch_user': '# Switch to non-root user',
        'expose_port': '# Expose port',
        'health_check': '# Health check',
        'start_cmd': '# Start command',
        'default_cmd': 'CMD ["echo", "Please configure start command"]',
    },
    'ja': {
        'header': '# ==================================================\n# Dockerfile生成ツールで作成\n# ベースイメージ: {image}\n# ==================================================',
        'base_image': '# ベースイメージ',
        'maintainer': '# 作成者情報',
        'work_dir': '# 作業ディレクトリ設定',
        'env_vars': '# 環境変数設定',
        'sys_packages': '# システム依存パッケージインストール',
        'copy_deps': '# 依存ファイルコピー',
        'install_python_deps': '# Python依存インストール',
        'copy_package_json': '# package.jsonコピー',
        'install_npm_deps': '# npm依存インストール（本番環境）',
        'copy_composer': '# composerファイルコピー',
        'install_composer_deps': '# composer依存インストール',
        'copy_pom': '# pom.xmlコピー',
        'download_maven_deps': '# Maven依存ダウンロード',
        'copy_source': '# ソースコードコピー',
        'copy_cargo': '# Cargoファイルコピー',
        'build_rust': '# Rustアプリビルド',
        'copy_csproj': '# プロジェクトファイルコピー',
        'copy_gemfile': '# Gemfileコピー',
        'install_ruby_deps': '# Ruby依存インストール',
        'copy_app_code': '# アプリコードコピー',
        'create_user': '# non-rootユーザー作成（セキュリティ推奨）',
        'set_permissions': '# ファイル権限設定',
        'switch_user': '# non-rootユーザーに切り替え',
        'expose_port': '# ポート公開',
        'health_check': '# ヘルスチェック',
        'start_cmd': '# 起動コマンド',
        'default_cmd': 'CMD ["echo", "起動コマンドを設定してください"]',
    },
    'ko': {
        'header': '# ==================================================\n# Dockerfile 생성기로 작성\n# 베이스 이미지: {image}\n# ==================================================',
        'base_image': '# 베이스 이미지',
        'maintainer': '# 관리자 정보',
        'work_dir': '# 작업 디렉토리 설정',
        'env_vars': '# 환경 변수 설정',
        'sys_packages': '# 시스템 의존성 설치',
        'copy_deps': '# 의존성 파일 복사',
        'install_python_deps': '# Python 의존성 설치',
        'copy_package_json': '# package.json 복사',
        'install_npm_deps': '# npm 의존성 설치 (프로덕션)',
        'copy_composer': '# composer 파일 복사',
        'install_composer_deps': '# composer 의존성 설치',
        'copy_pom': '# pom.xml 복사',
        'download_maven_deps': '# Maven 의존성 다운로드',
        'copy_source': '# 소스 코드 복사',
        'copy_cargo': '# Cargo 파일 복사',
        'build_rust': '# Rust 앱 빌드',
        'copy_csproj': '# 프로젝트 파일 복사',
        'copy_gemfile': '# Gemfile 복사',
        'install_ruby_deps': '# Ruby 의존성 설치',
        'copy_app_code': '# 앱 코드 복사',
        'create_user': '# non-root 사용자 생성 (보안 권장)',
        'set_permissions': '# 파일 권한 설정',
        'switch_user': '# non-root 사용자로 전환',
        'expose_port': '# 포트 노출',
        'health_check': '# 헬스 체크',
        'start_cmd': '# 시작 명령',
        'default_cmd': 'CMD ["echo", "시작 명령을 설정하세요"]',
    },
    'ru': {
        'header': '# ==================================================\n# Создано генератором Dockerfile\n# Базовый образ: {image}\n# ==================================================',
        'base_image': '# Базовый образ',
        'maintainer': '# Информация об авторе',
        'work_dir': '# Установка рабочей директории',
        'env_vars': '# Установка переменных окружения',
        'sys_packages': '# Установка системных зависимостей',
        'copy_deps': '# Копирование файла зависимостей',
        'install_python_deps': '# Установка Python зависимостей',
        'copy_package_json': '# Копирование package.json',
        'install_npm_deps': '# Установка npm зависимостей (production)',
        'copy_composer': '# Копирование composer файлов',
        'install_composer_deps': '# Установка composer зависимостей',
        'copy_pom': '# Копирование pom.xml',
        'download_maven_deps': '# Загрузка Maven зависимостей',
        'copy_source': '# Копирование исходного кода',
        'copy_cargo': '# Копирование Cargo файлов',
        'build_rust': '# Сборка Rust приложения',
        'copy_csproj': '# Копирование файлов проекта',
        'copy_gemfile': '# Копирование Gemfile',
        'install_ruby_deps': '# Установка Ruby зависимостей',
        'copy_app_code': '# Копирование кода приложения',
        'create_user': '# Создание non-root пользователя (безопасность)',
        'set_permissions': '# Установка прав доступа',
        'switch_user': '# Переключение на non-root пользователя',
        'expose_port': '# Открытие порта',
        'health_check': '# Проверка здоровья',
        'start_cmd': '# Команда запуска',
        'default_cmd': 'CMD ["echo", "Настройте команду запуска"]',
    },
    'de': {
        'header': '# ==================================================\n# Erstellt vom Dockerfile Generator\n# Basis-Image: {image}\n# ==================================================',
        'base_image': '# Basis-Image',
        'maintainer': '# Betreuer-Info',
        'work_dir': '# Arbeitsverzeichnis festlegen',
        'env_vars': '# Umgebungsvariablen setzen',
        'sys_packages': '# Systemabhängigkeiten installieren',
        'copy_deps': '# Abhängigkeitsdatei kopieren',
        'install_python_deps': '# Python-Abhängigkeiten installieren',
        'copy_package_json': '# package.json kopieren',
        'install_npm_deps': '# npm-Abhängigkeiten installieren (Produktion)',
        'copy_composer': '# composer-Dateien kopieren',
        'install_composer_deps': '# composer-Abhängigkeiten installieren',
        'copy_pom': '# pom.xml kopieren',
        'download_maven_deps': '# Maven-Abhängigkeiten herunterladen',
        'copy_source': '# Quellcode kopieren',
        'copy_cargo': '# Cargo-Dateien kopieren',
        'build_rust': '# Rust-Anwendung bauen',
        'copy_csproj': '# Projektdateien kopieren',
        'copy_gemfile': '# Gemfile kopieren',
        'install_ruby_deps': '# Ruby-Abhängigkeiten installieren',
        'copy_app_code': '# Anwendungscode kopieren',
        'create_user': '# Non-root Benutzer erstellen (Sicherheit)',
        'set_permissions': '# Dateiberechtigungen setzen',
        'switch_user': '# Zu non-root Benutzer wechseln',
        'expose_port': '# Port freigeben',
        'health_check': '# Health-Check',
        'start_cmd': '# Start-Befehl',
        'default_cmd': 'CMD ["echo", "Bitte Start-Befehl konfigurieren"]',
    },
    'fr': {
        'header': '# ==================================================\n# Créé par le générateur Dockerfile\n# Image de base : {image}\n# ==================================================',
        'base_image': '# Image de base',
        'maintainer': '# Info mainteneur',
        'work_dir': '# Définir le répertoire de travail',
        'env_vars': '# Définir les variables d\'environnement',
        'sys_packages': '# Installer les dépendances système',
        'copy_deps': '# Copier le fichier de dépendances',
        'install_python_deps': '# Installer les dépendances Python',
        'copy_package_json': '# Copier package.json',
        'install_npm_deps': '# Installer les dépendances npm (production)',
        'copy_composer': '# Copier les fichiers composer',
        'install_composer_deps': '# Installer les dépendances composer',
        'copy_pom': '# Copier pom.xml',
        'download_maven_deps': '# Télécharger les dépendances Maven',
        'copy_source': '# Copier le code source',
        'copy_cargo': '# Copier les fichiers Cargo',
        'build_rust': '# Construire l\'application Rust',
        'copy_csproj': '# Copier les fichiers projet',
        'copy_gemfile': '# Copier Gemfile',
        'install_ruby_deps': '# Installer les dépendances Ruby',
        'copy_app_code': '# Copier le code de l\'application',
        'create_user': '# Créer utilisateur non-root (sécurité)',
        'set_permissions': '# Définir les permissions',
        'switch_user': '# Basculer vers utilisateur non-root',
        'expose_port': '# Exposer le port',
        'health_check': '# Health check',
        'start_cmd': '# Commande de démarrage',
        'default_cmd': 'CMD ["echo", "Veuillez configurer la commande de démarrage"]',
    },
    'ar': {
        'header': '# ==================================================\n# أنشئ بواسطة مولد Dockerfile\n# الصورة الأساسية: {image}\n# ==================================================',
        'base_image': '# الصورة الأساسية',
        'maintainer': '# معلومات المشرف',
        'work_dir': '# تعيين مجلد العمل',
        'env_vars': '# تعيين متغيرات البيئة',
        'sys_packages': '# تثبيت حزم النظام',
        'copy_deps': '# نسخ ملف التبعيات',
        'install_python_deps': '# تثبيت تبعيات Python',
        'copy_package_json': '# نسخ package.json',
        'install_npm_deps': '# تثبيت تبعيات npm (إنتاج)',
        'copy_composer': '# نسخ ملفات composer',
        'install_composer_deps': '# تثبيت تبعيات composer',
        'copy_pom': '# نسخ pom.xml',
        'download_maven_deps': '# تحميل تبعيات Maven',
        'copy_source': '# نسخ الكود المصدري',
        'copy_cargo': '# نسخ ملفات Cargo',
        'build_rust': '# بناء تطبيق Rust',
        'copy_csproj': '# نسخ ملفات المشروع',
        'copy_gemfile': '# نسخ Gemfile',
        'install_ruby_deps': '# تثبيت تبعيات Ruby',
        'copy_app_code': '# نسخ كود التطبيق',
        'create_user': '# إنشاء مستخدم non-root (أمان)',
        'set_permissions': '# تعيين صلاحيات الملفات',
        'switch_user': '# التبديل إلى مستخدم non-root',
        'expose_port': '# فتح المنفذ',
        'health_check': '# فحص الصحة',
        'start_cmd': '# أمر البدء',
        'default_cmd': 'CMD ["echo", "يرجى تكوين أمر البدء"]',
    }
}

def get_comment(lang, key, **kwargs):
    """获取指定语言的注释"""
    comments = DOCKERFILE_COMMENTS.get(lang, DOCKERFILE_COMMENTS['en'])
    text = comments.get(key, DOCKERFILE_COMMENTS['en'].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass
    return text

def generate_dockerfile(config, lang='zh'):
    """生成Dockerfile内容 - 优化版，包含安全最佳实践，支持多语言注释"""
    lines = []
    
    base_image = config.get('base_image', 'python:3.12-slim')
    
    # 文件头
    lines.append(get_comment(lang, 'header', image=base_image))
    lines.append("")
    
    # 基础镜像
    lines.append(get_comment(lang, 'base_image'))
    lines.append(f"FROM {base_image}")
    lines.append("")
    
    # 维护者信息（使用LABEL代替MAINTAINER）
    if config.get('maintainer'):
        lines.append(get_comment(lang, 'maintainer'))
        lines.append(f"LABEL maintainer=\"{config['maintainer']}\"")
        lines.append("")
    
    # 设置工作目录
    work_dir = config.get('work_dir', '/app')
    lines.append(get_comment(lang, 'work_dir'))
    lines.append(f"WORKDIR {work_dir}")
    lines.append("")
    
    # 环境变量
    if config.get('env_vars'):
        lines.append(get_comment(lang, 'env_vars'))
        for key, value in config['env_vars'].items():
            if key and value:
                lines.append(f"ENV {key}={value}")
        lines.append("")
    
    # 系统包安装（根据基础镜像类型选择包管理器）
    if config.get('system_packages'):
        packages = ' '.join(config['system_packages'].split(','))
        
        lines.append(get_comment(lang, 'sys_packages'))
        
        # 检测基础镜像类型并选择合适的包管理器
        if 'alpine' in base_image.lower():
            lines.append(f"RUN apk add --no-cache {packages}")
        elif 'debian' in base_image.lower() or 'ubuntu' in base_image.lower() or 'python' in base_image.lower() or 'openjdk' in base_image.lower():
            lines.append(f"RUN apt-get update && apt-get install -y --no-install-recommends {packages} \\")
            lines.append("    && rm -rf /var/lib/apt/lists/*")
        else:
            lines.append(f"RUN apt-get update && apt-get install -y --no-install-recommends {packages} \\")
            lines.append("    && rm -rf /var/lib/apt/lists/*")
        
        lines.append("")
    
    # 复制依赖文件
    package_manager = config.get('package_manager', 'pip')
    
    if package_manager == 'pip' and config.get('requirements_file'):
        lines.append(get_comment(lang, 'copy_deps'))
        lines.append(f"COPY {config['requirements_file']} .")
        lines.append("")
        lines.append(get_comment(lang, 'install_python_deps'))
        lines.append("RUN pip install --no-cache-dir --upgrade pip && \\")
        lines.append("    pip install --no-cache-dir -r requirements.txt")
        lines.append("")
    elif package_manager == 'npm' and config.get('package_json'):
        lines.append(get_comment(lang, 'copy_package_json'))
        lines.append("COPY package*.json ./")
        lines.append("")
        lines.append(get_comment(lang, 'install_npm_deps'))
        lines.append("RUN npm ci --only=production")
        lines.append("")
    elif package_manager == 'composer' and config.get('composer_json'):
        lines.append(get_comment(lang, 'copy_composer'))
        lines.append("COPY composer.json composer.lock ./")
        lines.append("")
        lines.append(get_comment(lang, 'install_composer_deps'))
        lines.append("RUN composer install --no-dev --optimize-autoloader --no-interaction")
        lines.append("")
    elif package_manager == 'maven':
        lines.append(get_comment(lang, 'copy_pom'))
        lines.append("COPY pom.xml .")
        lines.append("")
        lines.append(get_comment(lang, 'download_maven_deps'))
        lines.append("RUN mvn dependency:go-offline -B")
        lines.append("")
        lines.append(get_comment(lang, 'copy_source'))
        lines.append("COPY src ./src")
        lines.append("RUN mvn package -DskipTests -B")
        lines.append("")
    elif package_manager == 'cargo':
        lines.append(get_comment(lang, 'copy_cargo'))
        lines.append("COPY Cargo.toml Cargo.lock ./")
        lines.append("")
        lines.append(get_comment(lang, 'build_rust'))
        lines.append("RUN cargo build --release")
        lines.append("")
    elif package_manager == 'dotnet':
        lines.append(get_comment(lang, 'copy_csproj'))
        lines.append("COPY *.csproj ./")
        lines.append("RUN dotnet restore")
        lines.append("")
        lines.append(get_comment(lang, 'copy_source'))
        lines.append("COPY . ./")
        lines.append("RUN dotnet publish -c Release -o out")
        lines.append("")
    elif package_manager == 'bundler':
        lines.append(get_comment(lang, 'copy_gemfile'))
        lines.append("COPY Gemfile Gemfile.lock ./")
        lines.append("")
        lines.append(get_comment(lang, 'install_ruby_deps'))
        lines.append("RUN bundle install --jobs 4 --retry 3")
        lines.append("")
    
    # 复制应用代码
    if config.get('app_code_dir'):
        lines.append(get_comment(lang, 'copy_app_code'))
        lines.append(f"COPY {config['app_code_dir']} .")
        lines.append("")
    
    # 创建非root用户（安全最佳实践）
    if config.get('create_user', True):
        lines.append(get_comment(lang, 'create_user'))
        
        if 'alpine' in base_image.lower():
            lines.append("RUN addgroup -g 1000 appgroup && \\")
            lines.append("    adduser -u 1000 -G appgroup -s /bin/sh -D appuser")
        else:
            lines.append("RUN groupadd -r appgroup && \\")
            lines.append("    useradd -r -g appgroup -s /bin/bash appuser")
        
        lines.append("")
        lines.append(get_comment(lang, 'set_permissions'))
        lines.append(f"RUN chown -R appuser:appgroup {work_dir}")
        lines.append("")
        lines.append(get_comment(lang, 'switch_user'))
        lines.append("USER appuser")
        lines.append("")
    
    # 暴露端口
    if config.get('port'):
        lines.append(get_comment(lang, 'expose_port'))
        lines.append(f"EXPOSE {config['port']}")
        lines.append("")
    
    # 健康检查
    if config.get('health_check'):
        lines.append(get_comment(lang, 'health_check'))
        lines.append(f"HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\")
        lines.append(f"  CMD {config['health_check']}")
        lines.append("")
    
    # 运行命令
    lines.append(get_comment(lang, 'start_cmd'))
    
    # 根据框架调整启动命令
    framework = config.get('framework', '')
    if framework in ['flask']:
        lines.append(f'CMD ["python", "app.py"]')
    elif framework in ['fastapi']:
        port = config.get('port', '8000')
        lines.append(f'CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]')
    elif framework in ['express', 'nextjs', 'nestjs', 'react', 'vue']:
        lines.append(f'CMD ["npm", "start"]')
    elif framework in ['django']:
        port = config.get('port', '8000')
        lines.append(f'CMD ["python", "manage.py", "runserver", "0.0.0.0:{port}"]')
    elif framework in ['spring']:
        lines.append('CMD ["java", "-jar", "target/app.jar"]')
    elif framework in ['gin', 'fiber']:
        lines.append(f'CMD ["./main"]')
    elif framework in ['laravel']:
        port = config.get('port', '80')
        lines.append(f'CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port={port}"]')
    elif framework in ['actix']:
        lines.append(f'CMD ["./target/release/app"]')
    elif framework in ['dotnet']:
        lines.append(f'CMD ["dotnet", "out/app.dll"]')
    elif framework in ['rails']:
        port = config.get('port', '3000')
        lines.append(f'CMD ["rails", "server", "-b", "0.0.0.0", "-p", "{port}"]')
    elif framework in ['static']:
        lines.append('CMD ["nginx", "-g", "daemon off;"]')
    elif config.get('cmd'):
        cmd_str = config['cmd']
        if isinstance(cmd_str, list):
            cmd_str = ' '.join(cmd_str)
        lines.append(f"CMD {cmd_str}")
    else:
        lines.append(get_comment(lang, 'default_cmd'))
    
    return '\n'.join(lines)

def generate_dockerignore(framework=''):
    """生成.dockerignore文件 - 根据框架优化"""
    
    # 基础内容（所有项目通用）
    base_content = """# ==================================================
# .dockerignore 文件
# 排除不需要的文件，减小构建上下文，提高构建速度
# ==================================================

# Git
.git
.gitignore
.gitattributes

# IDE
.vscode
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/
log/

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore
.docker/

# CI/CD
.github/
.gitlab-ci.yml
.travis.yml
azure-pipelines.yml

# Documentation
README.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE
docs/
"""
    
    # 框架特定内容
    framework_content = {
        'python': """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/
.mypy_cache/
.dmypy.json
.dmmypy.json
*.pytype
.pyre/
.pytest_cache/
.ruff_cache/

# Jupyter
.ipynb_checkpoints
*.ipynb

# Environment
.env
.env.local
.env.*.local
.venv
""",
        'node': """
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
.npm
.yarn/cache
.yarn/unplugged
.yarn/build-state.yml
.yarn/install-state.gz
.pnp.*

# Build outputs
dist/
build/
.next/
.nuxt/
.cache/
.parcel-cache/
.vite/
vite.config.ts.timestamp-*

# Environment
.env
.env.local
.env.*.local
.env.development
.env.test
.env.production

# Testing
coverage/
.nyc_output/

# TypeScript
*.tsbuildinfo
""",
        'go': """
# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
go.work
go.work.sum
""",
        'rust': """
# Rust
/target/
**/*.rs.bk
Cargo.lock
!Cargo.toml
!Cargo.lock
""",
        'java': """
# Java
*.class
*.jar
*.war
*.ear
target/
.mvn/
mvnw
mvnw.cmd
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar
!**/src/main/**/build/
!**/src/test/**/build/

# IDE
*.iml
*.ipr
*.iws

# Spring Boot
.springBeans
""",
        'php': """
# PHP
/vendor/
composer.phar
composer.lock
!composer.json

# Laravel
/public/hot
/public/storage
/storage/*.key
/storage/framework/cache/data/
/storage/framework/sessions/
/storage/framework/testing/
/storage/framework/views/
/storage/logs/
/bootstrap/cache/
.env
.env.backup
.env.production
.phpunit.result.cache
Homestead.json
Homestead.yaml
auth.json

# PHPUnit
.phpunit.cache/
""",
        'ruby': """
# Ruby
*.gem
*.rbc
/.config
/coverage/
/InstalledFiles
/pkg/
/spec/reports/
/spec/examples.txt
/test/tmp/
/test/version_tmp/
/tmp/

# Bundler
/vendor/bundle
/lib/bundler/man/

# Rails
*.rbc
capybara-*.html
.rspec
/db/*.sqlite3
/db/*.sqlite3-journal
/public/assets
/public/system
/coverage/
/spec/tmp
**.orig
rerun.txt
pickle-email-*.html

# Environment
.env
.env.*
""",
        'dotnet': """
# .NET
bin/
obj/
out/
*.dll
*.exe
*.pdb
*.cache
*.ilk
*.log
*.vspscc
*.vssscc
.vs/
*.user
*.userosscache
*.suo
*.userprefs

# NuGet
*.nuget.props
*.nuget.targets
packages/

# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
[Ww][Ii][Nn]32/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/
[Ll]ogs/
"""
    }
    
    # 根据框架选择额外内容
    extra_content = ""
    
    if framework in ['flask', 'django', 'fastapi'] or 'python' in framework:
        extra_content = framework_content.get('python', '')
    elif framework in ['express', 'nextjs', 'nestjs', 'react', 'vue'] or 'node' in framework:
        extra_content = framework_content.get('node', '')
    elif framework in ['gin', 'fiber'] or 'go' in framework:
        extra_content = framework_content.get('go', '')
    elif framework in ['actix'] or 'rust' in framework:
        extra_content = framework_content.get('rust', '')
    elif framework in ['spring'] or 'java' in framework:
        extra_content = framework_content.get('java', '')
    elif framework in ['laravel'] or 'php' in framework:
        extra_content = framework_content.get('php', '')
    elif framework in ['rails'] or 'ruby' in framework:
        extra_content = framework_content.get('ruby', '')
    elif framework in ['dotnet'] or '.net' in framework.lower():
        extra_content = framework_content.get('dotnet', '')
    
    # 如果没有匹配到特定框架，添加所有通用内容
    if not extra_content:
        extra_content = """
# Python (if applicable)
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
.pytest_cache/
.coverage

# Node.js (if applicable)
node_modules/
npm-debug.log*
dist/
build/
.next/
.cache/

# Environment (all projects)
.env
.env.local
.env.*.local
"""
    
    return base_content + extra_content

@app.route('/')
def index():
    """主页"""
    return render_template('index.html', presets=PRESETS)

@app.route('/api/generate', methods=['POST'])
def generate():
    """生成Dockerfile"""
    try:
        config = request.json
        lang = config.pop('lang', 'zh')  # 提取语言参数
        dockerfile = generate_dockerfile(config, lang=lang)
        return jsonify({
            'success': True,
            'dockerfile': dockerfile
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/presets')
def get_presets():
    """获取预设列表"""
    return jsonify({
        'success': True,
        'presets': PRESETS
    })

@app.route('/api/preset/<preset_id>')
def get_preset(preset_id):
    """获取特定预设"""
    if preset_id in PRESETS:
        return jsonify({
            'success': True,
            'preset': PRESETS[preset_id]
        })
    else:
        return jsonify({
            'success': False,
            'error': '预设不存在'
        }), 404

@app.route('/api/dockerignore', methods=['POST'])
def get_dockerignore():
    """生成.dockerignore文件 - 支持框架特定优化"""
    try:
        data = request.json or {}
        framework = data.get('framework', '')
        
        return jsonify({
            'success': True,
            'content': generate_dockerignore(framework)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download', methods=['POST'])
def download():
    """下载Dockerfile文件"""
    try:
        config = request.json
        dockerfile = generate_dockerfile(config)
        
        # 保存到临时文件
        filename = f"Dockerfile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(dockerfile)
        
        return send_file(filepath, 
                        as_attachment=True, 
                        download_name='Dockerfile',
                        mimetype='text/plain')
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/validate', methods=['POST'])
def validate():
    """验证配置"""
    try:
        config = request.json
        errors = []
        
        # 基础验证
        if not config.get('base_image'):
            errors.append('请选择基础镜像')
        
        if not config.get('work_dir'):
            errors.append('请设置工作目录')
        
        # 特定框架验证
        if config.get('framework') in ['flask', 'django'] and not config.get('requirements_file'):
            errors.append('Python应用建议添加requirements.txt')
        
        if config.get('framework') in ['express', 'nextjs', 'react', 'vue'] and not config.get('package_json'):
            errors.append('Node.js应用建议添加package.json')
        
        return jsonify({
            'success': len(errors) == 0,
            'errors': errors
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================================================
# 多语言支持 API
# ==================================================

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    'zh': '简体中文',
    'en': 'English',
    'ja': '日本語',
    'ko': '한국어',
    'ru': 'Русский',
    'ar': 'العربية',
    'de': 'Deutsch',
    'fr': 'Français'
}

# 语言对应的RTL（从右到左）标记
RTL_LANGUAGES = ['ar']

def load_translation(lang):
    """加载指定语言的翻译文件"""
    translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
    lang_file = os.path.join(translations_dir, f'{lang}.json')
    
    # 如果请求的语言不存在，回退到中文
    if not os.path.exists(lang_file):
        lang_file = os.path.join(translations_dir, 'zh.json')
    
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading translation: {e}")
        return {}

@app.route('/api/languages')
def get_languages():
    """获取支持的语言列表"""
    return jsonify({
        'success': True,
        'languages': SUPPORTED_LANGUAGES,
        'default': 'zh',
        'rtl': RTL_LANGUAGES
    })

@app.route('/api/translation/<lang>')
def get_translation(lang):
    """获取指定语言的翻译"""
    translation = load_translation(lang)
    return jsonify({
        'success': True,
        'translation': translation,
        'is_rtl': lang in RTL_LANGUAGES
    })

# 配置文件上传目录
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'downloads')

if __name__ == '__main__':
    # 确保下载目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    print("=" * 60)
    print("🐳 Dockerfile生成器启动中...")
    print("=" * 60)
    print("📍 访问地址: http://127.0.0.1:5000")
    print("📖 按 Ctrl+C 停止服务")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
