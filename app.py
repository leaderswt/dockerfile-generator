"""
Dockerfile生成器 - 图形界面工具
功能强大、界面美观、小白友好的Dockerfile生成工具
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime

# 导入高级功能
from advanced_features import register_advanced_routes

app = Flask(__name__)

# 注册高级功能路由
register_advanced_routes(app)

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

def generate_dockerfile(config):
    """生成Dockerfile内容 - 优化版，包含安全最佳实践"""
    lines = []
    
    base_image = config.get('base_image', 'python:3.12-slim')
    
    # 文件头
    lines.append("# ==================================================")
    lines.append("# Dockerfile 生成器创建")
    lines.append("# 基础镜像: " + base_image)
    lines.append("# ==================================================")
    lines.append("")
    
    # 基础镜像
    lines.append("# 基础镜像")
    lines.append(f"FROM {base_image}")
    lines.append("")
    
    # 维护者信息（使用LABEL代替MAINTAINER）
    if config.get('maintainer'):
        lines.append("# 维护者信息")
        lines.append(f"LABEL maintainer=\"{config['maintainer']}\"")
        lines.append("")
    
    # 设置工作目录
    work_dir = config.get('work_dir', '/app')
    lines.append("# 设置工作目录")
    lines.append(f"WORKDIR {work_dir}")
    lines.append("")
    
    # 环境变量
    if config.get('env_vars'):
        lines.append("# 设置环境变量")
        for key, value in config['env_vars'].items():
            if key and value:
                lines.append(f"ENV {key}={value}")
        lines.append("")
    
    # 系统包安装（根据基础镜像类型选择包管理器）
    if config.get('system_packages'):
        packages = ' '.join(config['system_packages'].split(','))
        
        lines.append("# 安装系统依赖")
        
        # 检测基础镜像类型并选择合适的包管理器
        if 'alpine' in base_image.lower():
            # Alpine Linux 使用 apk
            lines.append(f"RUN apk add --no-cache {packages}")
        elif 'debian' in base_image.lower() or 'ubuntu' in base_image.lower() or 'python' in base_image.lower() or 'openjdk' in base_image.lower():
            # Debian/Ubuntu 使用 apt-get
            lines.append(f"RUN apt-get update && apt-get install -y --no-install-recommends {packages} \\")
            lines.append("    && rm -rf /var/lib/apt/lists/*")
        else:
            # 默认使用 apt-get
            lines.append(f"RUN apt-get update && apt-get install -y --no-install-recommends {packages} \\")
            lines.append("    && rm -rf /var/lib/apt/lists/*")
        
        lines.append("")
    
    # 复制依赖文件
    package_manager = config.get('package_manager', 'pip')
    
    if package_manager == 'pip' and config.get('requirements_file'):
        lines.append("# 复制依赖文件")
        lines.append(f"COPY {config['requirements_file']} .")
        lines.append("")
        lines.append("# 安装Python依赖")
        lines.append("RUN pip install --no-cache-dir --upgrade pip && \\")
        lines.append("    pip install --no-cache-dir -r requirements.txt")
        lines.append("")
    elif package_manager == 'npm' and config.get('package_json'):
        lines.append("# 复制package.json")
        lines.append("COPY package*.json ./")
        lines.append("")
        lines.append("# 安装npm依赖（生产环境）")
        lines.append("RUN npm ci --only=production")
        lines.append("")
    elif package_manager == 'composer' and config.get('composer_json'):
        lines.append("# 复制composer文件")
        lines.append("COPY composer.json composer.lock ./")
        lines.append("")
        lines.append("# 安装composer依赖")
        lines.append("RUN composer install --no-dev --optimize-autoloader --no-interaction")
        lines.append("")
    elif package_manager == 'maven':
        lines.append("# 复制pom.xml")
        lines.append("COPY pom.xml .")
        lines.append("")
        lines.append("# 下载Maven依赖")
        lines.append("RUN mvn dependency:go-offline -B")
        lines.append("")
        lines.append("# 复制源代码")
        lines.append("COPY src ./src")
        lines.append("RUN mvn package -DskipTests -B")
        lines.append("")
    elif package_manager == 'cargo':
        lines.append("# 复制Cargo文件")
        lines.append("COPY Cargo.toml Cargo.lock ./")
        lines.append("")
        lines.append("# 构建Rust应用")
        lines.append("RUN cargo build --release")
        lines.append("")
    elif package_manager == 'dotnet':
        lines.append("# 复制项目文件")
        lines.append("COPY *.csproj ./")
        lines.append("RUN dotnet restore")
        lines.append("")
        lines.append("# 复制源代码")
        lines.append("COPY . ./")
        lines.append("RUN dotnet publish -c Release -o out")
        lines.append("")
    elif package_manager == 'bundler':
        lines.append("# 复制Gemfile")
        lines.append("COPY Gemfile Gemfile.lock ./")
        lines.append("")
        lines.append("# 安装Ruby依赖")
        lines.append("RUN bundle install --jobs 4 --retry 3")
        lines.append("")
    
    # 复制应用代码
    if config.get('app_code_dir'):
        lines.append("# 复制应用代码")
        lines.append(f"COPY {config['app_code_dir']} .")
        lines.append("")
    
    # 创建非root用户（安全最佳实践）
    if config.get('create_user', True):
        lines.append("# 创建非root用户（安全最佳实践）")
        
        if 'alpine' in base_image.lower():
            lines.append("RUN addgroup -g 1000 appgroup && \\")
            lines.append("    adduser -u 1000 -G appgroup -s /bin/sh -D appuser")
        else:
            lines.append("RUN groupadd -r appgroup && \\")
            lines.append("    useradd -r -g appgroup -s /bin/bash appuser")
        
        lines.append("")
        lines.append("# 设置文件权限")
        lines.append(f"RUN chown -R appuser:appgroup {work_dir}")
        lines.append("")
        lines.append("# 切换到非root用户")
        lines.append("USER appuser")
        lines.append("")
    
    # 暴露端口
    if config.get('port'):
        lines.append(f"# 暴露端口")
        lines.append(f"EXPOSE {config['port']}")
        lines.append("")
    
    # 健康检查
    if config.get('health_check'):
        lines.append("# 健康检查")
        lines.append(f"HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\")
        lines.append(f"  CMD {config['health_check']}")
        lines.append("")
    
    # 运行命令
    lines.append("# 启动命令")
    
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
        # 默认命令
        lines.append(f'CMD ["echo", "请配置启动命令"]')
    
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
        dockerfile = generate_dockerfile(config)
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
