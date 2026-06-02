# 🐳 Dockerfile生成ツール

> 🤖 **AI支援開発プロジェクト** - AIプログラミングアシスタント（SOLO）が驱动し，自然言語からの要求で完全な機能を自动生成。

## 🌐 言語切り替え

[![English](https://img.shields.io/badge/English-blue?style=flat-square)](README_en.md)
[![日本語](https://img.shields.io/badge/日本語-red?style=flat-square)](README_ja.md)
[![简体中文](https://img.shields.io/badge/简体中文-green?style=flat-square)](README.md)

強力で美しく、初心者にも優しいDockerfile生成ツールです。

## ✨ 機能

- 🎨 **モダンなUI**：ダークテーマデザイン、美しく洗練された外观
- 🚀 **10+のプリセットテンプレート**：Python、Node.js、Java、Go、PHPなどの主流技术スタックをカバー
- 📝 **リアルタイムプレビュー**：设定変更即时にDockerfileを生成
- 🎯 **インテリジェントなヒント**：選択に基づいて自动的に最適なパラメータを設定
- 📋 **ワンクリックのコピー**：生成されたDockerfileを素早くコピー
- 🔒 **.dockerignore生成**：一般的な.dockerignoreファイルを自动生成
- 💡 **ヒント**：Dockerfile作成のベストプラクティスを提供

## 🛠️ 技術スタック

- **バックエンド**：Flask (Python)
- **フロントエンド**：HTML5 + CSS3 + Vanilla JavaScript
- **コードハイライト**：Highlight.js
- **データベースなし**：軽量設計

## 📦 インストール

### 方法1：直接実行（推奨）

1. Python 3.8+がインストールされていることを確認

2. 依存関係をインストール：
```bash
pip install -r requirements.txt
```

3. アプリケーションを実行：
```bash
python app.py
```

4. ブラウザで開く：`http://127.0.0.1:5000`

### 方法2：Dockerを使用

1. イメージをビルド：
```bash
docker build -t dockerfile-generator .
```

2. コンテナを実行：
```bash
docker run -p 5000:5000 dockerfile-generator
```

3. ブラウザで開く：`http://localhost:5000`

## 🎯 クイックスタート

### プリセットテンプレートを使用

1. 首页で技术スタックのプリセットを選択（例：Python Flask）
2. カードをクリックして設定を自动入力
3. 「Generate Dockerfile」ボタンをクリック
4. 「Download」または「Copy」をクリックして结果を取得

### カスタム設定

1. ベースイメージを選択
2. 作業ディレクトリとポートを設定
3. パッケージマネージャーを選択
4. 環境変数を追加（必要に応じて）
5. 「Generate Dockerfile」をクリック

## 📖 機能説明

### プリセットテンプレート

| テンプレート | 説明 | ベースイメージ |
|------------|------|--------------|
| 🐍 Python Flask | Flask Webアプリ | Python 3.11 |
| 🐍 Python Django | Django Webアプリ | Python 3.11 |
| 🟢 Node.js Express | Express バックエンドAPI | Node.js 18 |
| 🟢 Node.js Next.js | Next.js フルスタック | Node.js 18 |
| ☕ Java Spring | Spring Bootアプリ | OpenJDK 17 |
| 🔷 Go Gin | Gin Webフレームワーク | Go 1.21 |
| 🐘 PHP Laravel | Laravelアプリ | PHP 8.2 |
| 🌐 Nginx静的サイト | 静的HTML/CSS/JS | Nginx Alpine |
| ⚛️ React + Vite | React フロントエンド | Node.js 18 |
| 💚 Vue + Vite | Vue フロントエンド | Node.js 18 |

### 設定オプション

#### 基本設定
- **メンテナー**：DockerfileのMAINTAINER情報
- **ベースイメージ**：アプリケーション実行のOSと言語環境
- **作業ディレクトリ**：アプリケーションコードの配置場所
- **公開ポート**：コンテナが外部に公開するポート

#### 依存関係管理
- **pip**：Pythonプロジェクト（requirements.txtが必要）
- **npm**：Node.jsプロジェクト（package.jsonが必要）
- **Composer**：PHPプロジェクト（composer.jsonが必要）
- **Maven**：Javaプロジェクト（pom.xmlが必要）
- **Go Modules**：Goプロジェクト

#### 環境変数
- キーと値のペア形式で環境変数を追加
- 複数の変数をサポート

#### 詳細オプション
- **システムパッケージ**：追加のシステムパッケージインストール
- **アプリコードディレクトリ**：ソースコードの場所
- **ヘルスチェック**：コンテナヘルスチェックコマンド
- **起動コマンド**：コンテナ起動コマンド
- **フレームワークタイプ**：最適な起動コマンドを自动設定

## 🎨 インターフェースプレビュー

### ダークテーマデザイン
GitHub Darkテーマスタイル、目への负荷を軽減、長时间の使用に适しています。

### レスポンシブレイアウト
デスクトップ、タブレット、モバイルデバイスなどをサポート。

### コードハイライト
Highlight.jsによるDockerfile構文ハイライト、読みやすさを向上。

## 💡 ヒント

### 1. 軽量イメージを選択
```
推奨：python:3.11-slim
非推奨：python:3.11
```
slimとalpineバージョンはサイズが小さく、安全性が高くなります。

### 2. .dockerignoreを使用
不必要的文件和ディレクトリを除外：
- node_modules
- __pycache__
- .git
- *.log

### 3. マルチステージビルド
コンパイル言語には、マルチステージビルドで最终イメージのサイズを削减できます。

### 4. レイヤーキャッシュの最適化
変化が少ないステップ（依存関係のインストールなど）を前もって配置。

## 🔧 APIエンドポイント

### Dockerfileを生成
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

### プリセットリストを取得
```
GET /api/presets
```

### 特定のプリセットを取得
```
GET /api/preset/<preset_id>
```

### .dockerignoreを生成
```
POST /api/dockerignore
```

### Dockerfileをダウンロード
```
POST /api/download
Content-Type: application/json

{
    "base_image": "...",
    ...
}
```

### 設定を検証
```
POST /api/validate
Content-Type: application/json

{
    ...
}
```

## 🤝 貢献

IssueとPull Request大歓迎！

## 📝 ライセンス

MIT License

## 🙏 謝辞

- **SOLO** - AIプログラミングアシスタント、プロジェクト全程の设计与実装を驱动
- Flaskフレームワーク
- Highlight.jsコードハイライト
- GitHub Darkテーマデザインの灵感

---

**🤖 AI Generated & Developed by SOLO**
