# Claude Agent SDK 学習プロジェクト

## プロジェクト概要
ユーザーがClaude Agent SDKを学習するためのサンプルプロジェクト。
学習過程は `LEARNING.md` に記録している。

## 現在の状況（2026/01/05時点）

### 完了済み
- [x] SDKの概要理解
- [x] Python環境構築（.venv、claude-agent-sdk 0.1.18）
- [x] 基本サンプル作成・実行（`01_basic_query.py`）
- [x] 認証の仕組みの理解（Claude Code CLIを使用）
- [x] ファイル操作エージェント（`02_file_agent.py`）

### 次のステップ（ユーザーに選択してもらう）
応用サンプルの作成。以下の候補がある：
1. ~~ファイル操作エージェント（Write/Edit使用）~~ ✅
2. 会話型エージェント（ClaudeSDKClient使用）
3. カスタムツール定義
4. Hooks（ライフサイクル介入）

## ファイル構成
```
cagentsdk-sample/
├── .venv/                 # Python仮想環境（セットアップ済み）
├── 01_basic_query.py      # 基本サンプル（query()の使い方）
├── 02_file_agent.py       # ファイル操作エージェント（Write/Edit）
├── sample_output/         # エージェントが作成したファイル
│   └── hello.py
├── LEARNING.md            # 詳細な学習記録
└── CLAUDE.md              # このファイル（再開用）
```

## 実行方法
```bash
source .venv/bin/activate
python 01_basic_query.py
```

## 再開時の指示
- ユーザーは日本語で対応
- 学習記録は `LEARNING.md` に追記していく
- サンプルファイルは番号付きで作成（02_xxx.py, 03_xxx.py...）
- 実行結果の観察と学んだことを記録する
