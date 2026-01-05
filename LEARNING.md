# Claude Agent SDK 学習記録

## 学習開始日
2026年1月5日

---

## 1. Claude Agent SDKとは

Anthropic公式のSDKで、Claude AIを使った**自律的なエージェント**を開発できるツール。
Claude Code CLIと同じ機能をプログラムから利用できる。

### 主な特徴

| 機能 | 説明 |
|------|------|
| 組み込みツール | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch |
| サブエージェント | 専門タスク用の子エージェントを作成可能 |
| Hooks | エージェントのライフサイクルに介入可能 |
| MCP統合 | 外部システム（DB、API等）との連携 |
| セッション管理 | 複数のやり取りでコンテキスト保持 |

### 対応言語

- **Python** 3.10以上
  ```bash
  pip install claude-agent-sdk
  ```
- **TypeScript/Node.js** 18以上
  ```bash
  npm install @anthropic-ai/claude-agent-sdk
  ```

---

## 2. 基本的なアーキテクチャ

### 2つのアプローチ

#### `query()` - ワンショット実行
- 各呼び出しで新しいセッションを作成
- 1回限りのタスク向け
- シンプルで使いやすい

#### `ClaudeSDKClient` - 継続的会話
- 同一セッション内で複数のやり取りが可能
- 会話履歴やコンテキストを保持
- 対話型アプリケーション向け

---

## 3. 組み込みツール一覧

| ツール名 | 機能 |
|----------|------|
| Read | ファイル読み取り |
| Write | 新規ファイル作成 |
| Edit | 既存ファイルの編集 |
| Bash | ターミナルコマンド実行 |
| Glob | ファイルパターンマッチング |
| Grep | ファイル内容の正規表現検索 |
| WebSearch | ウェブ検索 |
| WebFetch | ウェブページのフェッチとパース |

---

## 4. パーミッションモード

| モード | 動作 | 用途 |
|--------|------|------|
| `default` | カスタム承認ロジック用 | 細かい制御が必要な場合 |
| `acceptEdits` | ファイル編集を自動承認 | 信頼できる開発ワークフロー |
| `bypassPermissions` | プロンプトなしで実行 | CI/CD、自動化 |

---

## 5. インストール手順

### 前提条件
Claude Codeのインストールと認証が必要

```bash
# macOS/Linux/WSL
curl -fsSL https://claude.ai/install.sh | bash

# または Homebrew
brew install --cask claude-code

# 認証
claude
```

### SDKインストール

**Python:**
```bash
pip install claude-agent-sdk
```

**TypeScript:**
```bash
npm install @anthropic-ai/claude-agent-sdk
```

---

## 6. サンプルコード

### Python - 基本的な使い方

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits"
        )
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

### TypeScript - 基本的な使い方

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review utils.py for bugs. Fix any issues you find.",
  options: {
    allowedTools: ["Read", "Edit", "Glob"],
    permissionMode: "acceptEdits"
  }
})) {
  if (message.type === "assistant" && message.message?.content) {
    for (const block of message.message.content) {
      if ("text" in block) {
        console.log(block.text);
      } else if ("name" in block) {
        console.log(`Tool: ${block.name}`);
      }
    }
  } else if (message.type === "result") {
    console.log(`Done: ${message.subtype}`);
  }
}
```

---

## 7. 学習の進捗

- [x] SDKの概要理解
- [x] 環境構築（2026/01/05完了）
- [x] 基本サンプルの作成と実行（2026/01/05完了）
- [ ] 応用サンプルの作成

---

## 8. 実習記録

### 実習1: 環境構築（2026/01/05）

#### 実施内容
1. Python仮想環境の作成
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. SDKのインストール
   ```bash
   pip install claude-agent-sdk
   ```

3. インストールされたバージョン: `claude-agent-sdk 0.1.18`

#### 学んだこと
- SDKはClaude Codeランタイムを内部で使用している
- Python 3.10以上が必要（今回は3.13.3を使用）

---

### 実習2: 基本サンプルの作成と実行（2026/01/05）

#### 作成ファイル
`01_basic_query.py`

#### コードの要点

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async for message in query(
    prompt="プロンプト文字列",
    options=ClaudeAgentOptions(
        allowed_tools=["Bash", "Read", "Glob"],  # 許可するツール
        permission_mode="default",                # パーミッションモード
    ),
):
    # メッセージ処理
```

#### 実行結果の観察

1. **ツール使用の流れ**
   - エージェントは自律的にツールを選択して実行
   - `Bash` → `Read` → `Read` → `Bash` → `Read` → `Read` の順で実行

2. **メッセージの種類**
   - `AssistantMessage`: Claudeからの応答（テキストまたはツール使用）
   - `ResultMessage`: 最終結果（`subtype`で成功/失敗を確認）

3. **ストリーミング**
   - `async for`でリアルタイムにメッセージを受け取れる
   - ツール実行中も進捗を確認可能

#### 学んだこと
- `query()`はシンプルで使いやすい
- エージェントは与えられたツールを組み合わせてタスクを達成する
- `allowed_tools`でセキュリティを制御できる

---

### 実習3: 認証の仕組みの理解（2026/01/05）

#### 疑問
「APIキーの設定なしでClaudeのサービスを使えるのか？」

#### 回答
Claude Agent SDKは**Claude Code CLIのランタイム**を内部で使用している。

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────┐
│  Pythonコード    │ ──→ │  Claude Code    │ ──→ │  Claude API │
│  (Agent SDK)    │      │  (ランタイム)    │      │             │
└─────────────────┘      └─────────────────┘      └─────────────┘
                              ↑
                         認証情報はここで管理
```

#### ポイント
| 項目 | 説明 |
|------|------|
| APIキー | コードに書く必要なし |
| 前提条件 | Claude Code CLIがインストール・認証済みであること |
| 確認方法 | `claude --version` が動けばOK |

#### 確認結果
```bash
$ claude --version
2.0.76 (Claude Code)
```
→ 認証済みであることを確認

#### 学んだこと
- 通常のClaude API（`anthropic`ライブラリ）とは認証方式が異なる
- Agent SDKはClaude Codeの認証セッションを共有する
- セキュリティ面でAPIキーをコードに埋め込まなくて良いのは利点

---

### 実習4: 基本サンプルの実行と観察（2026/01/05）

#### 実行コマンド
```bash
source .venv/bin/activate && python 01_basic_query.py
```

#### 実行結果
```
==================================================
Claude Agent SDK - 基本サンプル
==================================================

プロンプト: 現在のディレクトリにあるファイルを一覧表示して、簡単に説明してください。
--------------------------------------------------

[Tool] Bash を使用中...
[Claude] 現在のディレクトリにあるファイルとフォルダの一覧です：

| 名前 | 種類 | サイズ | 説明 |
|------|------|--------|------|
| `.venv` | フォルダ | - | Python仮想環境ディレクトリ |
| `01_basic_query.py` | ファイル | 2.2 KB | 基本的なクエリ処理のサンプル |
| `CLAUDE.md` | ファイル | 1.4 KB | プロジェクト設定 |
| `LEARNING.md` | ファイル | 7.8 KB | 学習内容のまとめ |

--------------------------------------------------
[結果] 完了: success
```

#### 処理の流れ
```
1. プロンプト送信
   ↓
2. エージェントがツールを自動選択（Bash）
   ↓
3. ツール実行結果を整形して回答
   ↓
4. ResultMessage で完了通知
```

#### コードと実行結果の対応

| コード部分 | 出力 |
|-----------|------|
| `hasattr(block, "name")` → ツール使用検出 | `[Tool] Bash を使用中...` |
| `hasattr(block, "text")` → テキスト検出 | `[Claude] 現在のディレクトリに...` |
| `message.subtype` → 結果タイプ | `[結果] 完了: success` |

#### 学んだこと
- **エージェントの自律性**: どのツールを使うかはエージェントが自分で判断する
- **ストリーミング応答**: `async for`でリアルタイムに進捗を受け取れる
- **メッセージの種類**: `AssistantMessage`（応答）と`ResultMessage`（完了通知）がある
- **ツール使用の透明性**: どのツールが使われたか分かる仕組みになっている

---

### 実習5: ファイル操作エージェント（2026/01/05）

#### 作成ファイル
`02_file_agent.py`

#### 基本サンプルとの違い

| 項目 | 01_basic_query.py | 02_file_agent.py |
|------|-------------------|------------------|
| 許可ツール | Bash, Read, Glob | Write, Edit, Read, Bash, Glob |
| パーミッション | `default` | `acceptEdits` |
| タスク | 単純な一覧表示 | 複数ステップ（作成→確認→編集） |

#### 重要な設定: permission_mode

```python
permission_mode="acceptEdits",  # ファイル編集を自動承認
```

| モード | 動作 |
|--------|------|
| `default` | ファイル変更時に確認が必要 |
| `acceptEdits` | ファイル変更を自動承認 |
| `bypassPermissions` | すべての操作を自動承認 |

#### エージェントの動作フロー

```
1. Bash  → ディレクトリ確認/作成
2. Write → hello.py 作成（最初は間違ったパス）
3. Bash  → 作業ディレクトリ確認
4. Write → 正しいパスで再作成 ← 自己修正！
5. Read  → 内容確認
6. Edit  → ユーザー入力機能を追加
7. Read  → 最終確認
```

#### 作成されたファイル

```python
# sample_output/hello.py
name = input("あなたの名前を入力してください: ")
print(f"こんにちは、{name}さん！")
```

#### ツール入力の取得方法

```python
if hasattr(block, "input"):
    input_data = block.input
    if tool_name == "Write" and "file_path" in input_data:
        print(f"ファイル作成: {input_data.get('file_path')}")
```

`block.input` でツールに渡された引数を取得できる。

#### 学んだこと
- **Write/Edit/Read の連携**: ファイル作成→確認→編集の流れ
- **acceptEdits の重要性**: これがないと毎回確認が必要
- **エージェントの自己修正能力**: パスミスを自分で検出・修正した
- **ツール入力の観察**: `block.input` で詳細な動作を追跡可能
- **複雑なタスクの分解**: エージェントは複数ステップを自律的に実行

---

### 実習6: 会話型エージェント（2026/01/05）

#### 作成ファイル
`03_conversation_agent.py`

#### query() vs ClaudeSDKClient

| 特徴 | `query()` | `ClaudeSDKClient` |
|------|-----------|-------------------|
| セッション | 毎回新規 | 同じセッションを継続 |
| 会話履歴 | 保持しない | 保持する |
| 用途 | ワンショット | 対話型 |

#### コードの基本構造

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async with ClaudeSDKClient(options=options) as client:
    # ターン1
    await client.query("最初の質問")
    async for message in client.receive_response():
        # 応答処理

    # ターン2（前のターンを覚えている）
    await client.query("その続きの質問")
    async for message in client.receive_response():
        # 応答処理
```

#### 実行結果の観察

| ターン | 質問 | 参照 | 結果 |
|--------|------|------|------|
| 1 | 「Pythonファイルを教えて」 | - | 3ファイルを一覧表示 |
| 2 | 「**その中で**一番シンプル？」 | ターン1 | 01_basic_query.py |
| 3 | 「**それの**行数は？」 | ターン2 | 59行 |

#### コンテキスト保持の証明

- ターン2: 「その中で」→ ターン1のファイル一覧を参照
- ターン3: 「それの」→ ターン2で言及したファイルを参照
- ターン3はツールを使わず回答 → 既に情報を持っていた

#### 学んだこと
- **ClaudeSDKClient**: `async with`で自動接続/切断
- **query() + receive_response()**: メッセージ送信と応答受信のペア
- **コンテキスト保持**: 指示語（その、それ）が正しく解釈される
- **効率性**: 過去に取得した情報は再取得不要

#### 復習: ClaudeSDKClientの本質とワークフローツールとの比較

##### コンテキスト保持が本質

```
ターン1: 「ファイルを教えて」     → [A, B, C]を回答
ターン2: 「その中で〜」          → 「その」= [A, B, C] と理解
ターン3: 「それの〜」            → 「それ」= 前の回答 と理解
```

前の会話を「覚えている」ことで、自然言語の指示語が機能する。
これにより、簡易的な「ワークフロー」を自然言語で構築できる。

##### Dify（ノードベースワークフロー）との比較

| 観点 | Dify (ノードベース) | ClaudeSDKClient |
|------|---------------------|-----------------|
| フロー定義 | 明示的（ノードと矢印） | 暗黙的（自然言語） |
| 分岐条件 | 厳格（if/else） | 柔軟（AIが判断） |
| ステップ | 事前に固定 | 動的に変化可能 |
| 再現性 | 高い（同じフロー） | 低い（毎回異なる可能性） |
| 柔軟性 | 低い | 高い |

##### 図解

```
【Dify】
  [入力] → [処理A] → [条件分岐] → [処理B] → [出力]
                         ↓
                     [処理C]
  ※ フローが事前に決まっている

【ClaudeSDKClient】
  [入力] → [AI判断] → [必要な処理を自律的に選択] → [出力]
              ↓
         前のターンの情報を参照
  ※ フローはAIが状況に応じて決める
```

##### ClaudeSDKClientの特徴まとめ

| 特徴 | 説明 |
|------|------|
| **柔軟性** | 途中で方針変更も可能（「やっぱり別の方法で」） |
| **自律性** | 各ステップでAIが最適な行動を判断 |
| **曖昧さへの対応** | 「それ」「あれ」でも文脈から理解 |
| **トレードオフ** | 再現性・予測可能性は低くなる |

---

### 実習7: カスタムツール定義（2026/01/05）

#### 作成ファイル
`04_custom_tool.py`

#### カスタムツールの作成手順

```
1. @toolデコレータでツール関数を定義
   ↓
2. create_sdk_mcp_serverでMCPサーバーを作成
   ↓
3. ClaudeAgentOptionsでmcp_serversを指定
   ↓
4. ClaudeSDKClientでエージェントを実行
```

#### 重要: query() vs ClaudeSDKClient

| 機能 | `query()` | `ClaudeSDKClient` |
|------|-----------|-------------------|
| カスタムツール | ❌ 未対応 | ✅ 対応 |

**カスタムツールを使う場合は必ず `ClaudeSDKClient` を使用する。**

#### コードの構造

```python
# 1. ツール定義
@tool(
    "add",                      # ツール名
    "2つの数値を足し算します",    # 説明（AIが参照）
    {"a": float, "b": float}    # パラメータスキーマ
)
async def add_numbers(args: dict[str, Any]) -> dict[str, Any]:
    result = args["a"] + args["b"]
    return {
        "content": [{
            "type": "text",
            "text": f"{args['a']} + {args['b']} = {result}"
        }]
    }

# 2. MCPサーバー作成
calculator_server = create_sdk_mcp_server(
    name="calculator",
    version="1.0.0",
    tools=[add_numbers, ...]
)

# 3. オプション設定
options = ClaudeAgentOptions(
    mcp_servers={"calculator": calculator_server},
    allowed_tools=["mcp__calculator__add", ...]
)

# 4. 実行（ClaudeSDKClientを使用）
async with ClaudeSDKClient(options=options) as client:
    await client.query("計算して")
```

#### ツール名の命名規則

```
mcp__{server_name}__{tool_name}

例：
- mcp__calculator__add
- mcp__calculator__multiply
- mcp__calculator__celsius_to_fahrenheit
```

#### 実行結果の観察

```
[Tool] mcp__calculator__add
[Tool] mcp__calculator__multiply
[Tool] mcp__calculator__celsius_to_fahrenheit
       [実行] add(123, 456) = 579
       [実行] multiply(7, 8) = 56
       [実行] celsius_to_fahrenheit(25) = 77.0
[Claude] 計算結果は以下の通りです：
1. 123 + 456 = 579
2. 7 × 8 = 56
3. 25°C = 77.0°F
```

- 3つのツールが**並列実行**された
- カスタムPython関数が実行され、結果がエージェントに返された

#### 学んだこと
- **@toolデコレータ**: ツール名、説明、スキーマを指定
- **create_sdk_mcp_server**: ツールをMCPサーバーにまとめる
- **戻り値形式**: `{"content": [{"type": "text", "text": "..."}]}`
- **query()の制限**: カスタムツールには`ClaudeSDKClient`が必須
- **並列実行**: 複数のカスタムツールを同時に呼び出せる

---

## 次のステップ

応用サンプルの候補：
1. ~~ファイル操作エージェント（Write/Edit使用）~~ ✅ 完了
2. ~~会話型エージェント（ClaudeSDKClient使用）~~ ✅ 完了
3. ~~カスタムツール定義~~ ✅ 完了
4. Hooks（ライフサイクル介入）
