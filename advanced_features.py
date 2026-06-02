"""
Dockerfile生成器 - 高级功能扩展
包含多阶段构建、Docker Compose生成等高级功能
"""

from flask import Blueprint, render_template, request, jsonify
import json

# 创建高级功能蓝图
advanced_bp = Blueprint('advanced', __name__, url_prefix='/advanced')

@advanced_bp.route('/')
def advanced_index():
    """高级功能页面"""
    return render_template('advanced.html')

@advanced_bp.route('/api/multi-stage', methods=['POST'])
def generate_multi_stage():
    """生成多阶段构建Dockerfile"""
    try:
        config = request.json
        
        lines = []
        lines.append("# ==================================================")
        lines.append("# 多阶段构建 Dockerfile")
        lines.append("# ==================================================")
        lines.append("")
        
        # 第一阶段：构建
        lines.append("# ============ 阶段1：构建 ============")
        lines.append(f"FROM {config.get('build_image', 'python:3.11-slim')} AS builder")
        lines.append("")
        
        work_dir = config.get('work_dir', '/build')
        lines.append(f"WORKDIR {work_dir}")
        lines.append("")
        
        # 复制依赖文件
        if config.get('copy_deps'):
            lines.append("# 复制依赖文件")
            lines.append(f"COPY {config.get('deps_file', 'requirements.txt')} .")
            lines.append("")
        
        # 安装构建依赖
        if config.get('install_deps'):
            lines.append("# 安装构建依赖")
            lines.append(f"RUN {config.get('install_cmd', 'pip install -r requirements.txt')}")
            lines.append("")
        
        # 复制源代码
        lines.append("# 复制源代码")
        lines.append(f"COPY {config.get('src_dir', 'src')} .")
        lines.append("")
        
        # 构建应用
        if config.get('build_cmd'):
            lines.append("# 构建应用")
            lines.append(f"RUN {config['build_cmd']}")
            lines.append("")
        
        lines.append("")
        lines.append("# ============ 阶段2：运行 ============")
        
        # 第二阶段：运行
        runtime_image = config.get('runtime_image', 'python:3.11-slim')
        lines.append(f"FROM {runtime_image} AS runtime")
        lines.append("")
        
        # 创建非root用户（安全）
        lines.append("# 创建非root用户")
        lines.append("RUN groupadd -r appgroup && useradd -r -g appgroup appuser")
        lines.append("")
        
        work_dir_run = config.get('work_dir_run', '/app')
        lines.append(f"WORKDIR {work_dir_run}")
        lines.append("")
        
        # 复制构建产物
        lines.append("# 从构建阶段复制产物")
        lines.append(f"COPY --from=builder {config.get('build_output', '/build/dist')} .")
        lines.append("")
        
        # 设置权限
        lines.append("# 设置权限")
        lines.append("RUN chown -R appuser:appgroup /app")
        lines.append("")
        
        # 切换用户
        lines.append("# 切换到非root用户")
        lines.append("USER appuser")
        lines.append("")
        
        # 暴露端口
        if config.get('port'):
            lines.append(f"EXPOSE {config['port']}")
            lines.append("")
        
        # 启动命令
        if config.get('cmd'):
            lines.append(f"CMD {config['cmd']}")
        
        return jsonify({
            'success': True,
            'dockerfile': '\n'.join(lines)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/api/docker-compose', methods=['POST'])
def generate_docker_compose():
    """生成Docker Compose配置"""
    try:
        config = request.json
        
        compose = {
            'version': '3.8',
            'services': {}
        }
        
        # 主服务配置
        service_name = config.get('service_name', 'app')
        compose['services'][service_name] = {
            'build': config.get('build_context', '.'),
            'container_name': config.get('container_name', f"{service_name}_container"),
            'ports': [f"{config.get('host_port', 8080)}:{config.get('container_port', 5000)}"],
            'environment': [],
            'restart': config.get('restart_policy', 'unless-stopped')
        }
        
        # 环境变量
        env_vars = config.get('env_vars', {})
        if env_vars:
            compose['services'][service_name]['environment'] = [
                f"{k}={v}" for k, v in env_vars.items()
            ]
        
        # 卷挂载（开发模式）
        if config.get('volumes'):
            compose['services'][service_name]['volumes'] = config['volumes']
        
        # 依赖服务
        if config.get('depends_on'):
            compose['services'][service_name]['depends_on'] = config['depends_on']
        
        # 网络
        if config.get('networks'):
            compose['services'][service_name]['networks'] = config['networks']
        
        # networks配置
        if config.get('networks'):
            compose['networks'] = {
                net: {'driver': 'bridge'} 
                for net in config['networks']
            }
        
        # 格式化输出
        compose_yaml = f"version: '{compose['version']}'\n\nservices:\n"
        
        for svc_name, svc_config in compose['services'].items():
            compose_yaml += f"  {svc_name}:\n"
            
            if 'build' in svc_config:
                compose_yaml += f"    build: {svc_config['build']}\n"
            if 'container_name' in svc_config:
                compose_yaml += f"    container_name: {svc_config['container_name']}\n"
            if 'ports' in svc_config:
                compose_yaml += f"    ports:\n"
                for port in svc_config['ports']:
                    compose_yaml += f"      - \"{port}\"\n"
            if 'environment' in svc_config and svc_config['environment']:
                compose_yaml += f"    environment:\n"
                for env in svc_config['environment']:
                    compose_yaml += f"      - {env}\n"
            if 'volumes' in svc_config:
                compose_yaml += f"    volumes:\n"
                for vol in svc_config['volumes']:
                    compose_yaml += f"      - {vol}\n"
            if 'depends_on' in svc_config:
                compose_yaml += f"    depends_on:\n"
                for dep in svc_config['depends_on']:
                    compose_yaml += f"      - {dep}\n"
            if 'restart' in svc_config:
                compose_yaml += f"    restart: {svc_config['restart']}\n"
            if 'networks' in svc_config:
                compose_yaml += f"    networks:\n"
                for net in svc_config['networks']:
                    compose_yaml += f"      - {net}\n"
            
            compose_yaml += "\n"
        
        # networks部分
        if 'networks' in compose:
            compose_yaml += "networks:\n"
            for net_name, net_config in compose['networks'].items():
                compose_yaml += f"  {net_name}:\n"
                compose_yaml += f"    driver: {net_config['driver']}\n\n"
        
        return jsonify({
            'success': True,
            'docker_compose': compose_yaml
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/api/best-practices', methods=['GET'])
def get_best_practices():
    """获取Dockerfile最佳实践"""
    practices = {
        'security': [
            {
                'title': '使用非root用户',
                'description': '创建专用用户运行应用，避免容器内root权限',
                'example': '''RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser'''
            },
            {
                'title': '定期更新基础镜像',
                'description': '及时更新镜像以修复安全漏洞',
                'example': '# 定期检查并更新 FROM python:3.11-slim'
            },
            {
                'title': '使用特定版本标签',
                'description': '避免使用latest标签，确保构建可重现',
                'example': '# ✅ 推荐：python:3.11.8-slim\n# ❌ 避免：python:slim'
            },
            {
                'title': '最小化安装',
                'description': '只安装运行所需包，减少攻击面',
                'example': 'apt-get install --no-install-recommends <package>'
            }
        ],
        'performance': [
            {
                'title': '利用层缓存',
                'description': '将不常变化的指令放前面，依赖文件先复制',
                'example': '''# ✅ 好的顺序
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ 差的顺序
COPY . .
RUN pip install -r requirements.txt'''
            },
            {
                'title': '多阶段构建',
                'description': '分离构建环境和运行环境，减小镜像体积',
                'example': '''FROM golang AS builder
RUN go build -o app

FROM alpine
COPY --from=builder /app /app
CMD ["/app"]'''
            },
            {
                'title': '合并RUN指令',
                'description': '减少镜像层数，加快构建',
                'example': '''RUN apt-get update && \\
    apt-get install -y git curl && \\
    rm -rf /var/lib/apt/lists/*'''
            },
            {
                'title': '使用合适的基础镜像',
                'description': 'slim和alpine版本体积更小',
                'example': '# ✅ python:3.11-slim (约150MB)\n# ❌ python:3.11 (约1GB)'
            }
        ],
        'maintainability': [
            {
                'title': '添加健康检查',
                'description': '帮助监控容器状态',
                'example': 'HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health || exit 1'
            },
            {
                'title': '使用.dockerignore',
                'description': '排除不需要的文件，减少构建上下文',
                'example': '''node_modules
.git
__pycache__
*.log'''
            },
            {
                'title': '添加LABEL元数据',
                'description': '记录维护者、版本等信息',
                'example': '''LABEL maintainer="your.email@example.com"
LABEL version="1.0"
LABEL description="Your application"'''
            },
            {
                'title': '使用WORKDIR而不是cd',
                'description': '更清晰，且会自动创建目录',
                'example': '# ✅ WORKDIR /app\n# ❌ RUN cd /app'
            }
        ]
    }
    
    return jsonify({
        'success': True,
        'practices': practices
    })

# 注册蓝图到主应用
def register_advanced_routes(app):
    """注册高级功能路由"""
    app.register_blueprint(advanced_bp)
