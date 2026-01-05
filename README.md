# Claude Agent SDK 学習プロジェクト

Claude Agent SDK（Python）の学習用サンプル集です。

## 前提条件

- Python 3.10以上
- Claude Code CLIがインストール・認証済みであること

```bash
# Claude Codeのインストール（未インストールの場合）
brew install --cask claude-code

# 認証
claude
```

## セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/Takashi-Matsumura/cagentsdk-sample.git
cd cagentsdk-sample

# 仮想環境を作成・有効化
python3 -m venv .venv
source .venv/bin/activate

# SDKをインストール
pip install claude-agent-sdk
```

## サンプル一覧

| # | ファイル | 内容 | 使用API |
|---|----------|------|---------|
| 1 | `01_basic_query.py` | 基本的なquery()の使い方 | `query()` |
| 2 | `02_file_agent.py` | Write/Editでファイル操作 | `query()` |
| 3 | `03_conversation_agent.py` | 継続的な会話（コンテキスト保持） | `ClaudeSDKClient` |
| 4 | `04_custom_tool.py` | @toolでカスタムツール作成 | `ClaudeSDKClient` |
| 5 | `05_hooks.py` | ライフサイクルへの介入 | `ClaudeSDKClient` |

## 実行方法

```bash
# 仮想環境を有効化
source .venv/bin/activate

# 各サンプルを実行
python 01_basic_query.py
python 02_file_agent.py
python 03_conversation_agent.py
python 04_custom_tool.py
python 05_hooks.py
```

## 学んだ主要概念

### query() vs ClaudeSDKClient

| 機能 | `query()` | `ClaudeSDKClient` |
|------|-----------|-------------------|
| 用途 | シンプルなワンショット | 継続的な会話 |
| セッション | 毎回新規 | 保持 |
| カスタムツール | ❌ 未対応 | ✅ 対応 |
| Hooks | ❌ 限定的 | ✅ 完全対応 |

### パーミッションモード

| モード | 動作 |
|--------|------|
| `default` | ファイル変更時に確認が必要 |
| `acceptEdits` | ファイル変更を自動承認 |
| `bypassPermissions` | すべての操作を自動承認 |

## ファイル構成

```
cagentsdk-sample/
├── 01_basic_query.py         # 基本サンプル
├── 02_file_agent.py          # ファイル操作
├── 03_conversation_agent.py  # 会話型エージェント
├── 04_custom_tool.py         # カスタムツール
├── 05_hooks.py               # Hooks
├── LEARNING.md               # 詳細な学習記録
├── CLAUDE.md                 # プロジェクト概要（Claude Code用）
└── README.md                 # このファイル
```

## 参考リンク

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk)
- [Claude Code](https://claude.ai/code)

## ライセンス

MIT
