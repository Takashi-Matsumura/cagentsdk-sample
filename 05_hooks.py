"""
Claude Agent SDK - Hooks（ライフサイクル介入）
=============================================
エージェントの動作に介入する仕組み

このサンプルでは:
- PreToolUse: ツール実行前に介入（ブロック、入力変換）
- PostToolUse: ツール実行後に介入（監査ログ）
- HookMatcherでツールを指定
を学びます。

【重要】
- query()ではHooksが限定的 → ClaudeSDKClientを使う
- カスタムツールと同じパターン

【Hooksの種類】
- PreToolUse: ツール実行前（ブロック/変換が可能）
- PostToolUse: ツール実行後（ログ記録など）
- UserPromptSubmit: プロンプト送信時
- Stop: セッション終了時
"""

import asyncio
from datetime import datetime
from typing import Any

from claude_agent_sdk import (
    ClaudeSDKClient,  # query()ではなくClaudeSDKClientを使用
    ClaudeAgentOptions,
    HookMatcher,
    AssistantMessage,
    ResultMessage,
)


# ============================================================
# 1. PreToolUse フック: 危険な操作をブロック
# ============================================================

async def security_check(input_data: dict, tool_use_id: str, context: Any) -> dict:
    """
    ツール実行前のセキュリティチェック

    - .env ファイルへのアクセスをブロック
    - 危険なBashコマンドをブロック
    """
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    print(f"\n  🔍 [PreToolUse] セキュリティチェック: {tool_name}")

    # ファイル操作のチェック（Write, Edit, Read）
    if tool_name in ["Write", "Edit", "Read"]:
        file_path = tool_input.get("file_path", "")
        print(f"     → ファイル: {file_path}")

        # .env ファイルへのアクセスをブロック
        if ".env" in file_path:
            print(f"  🚫 [BLOCKED] .envファイルへのアクセスは禁止!")
            return {
                "permissionDecision": "deny",
                "permissionDecisionReason": ".envファイルには機密情報が含まれるためアクセス禁止",
            }

    # Bashコマンドのチェック
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        print(f"     → コマンド: {command[:50]}...")

        # 危険なコマンドをブロック
        dangerous_patterns = ["rm -rf /", ":(){ :|:& };:", "> /dev/sda"]
        for pattern in dangerous_patterns:
            if pattern in command:
                print(f"  🚫 [BLOCKED] 危険なコマンド検出: {pattern}")
                return {
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"危険なコマンドパターン検出: {pattern}",
                }

    # 問題なければ許可
    print(f"  ✅ [ALLOWED]")
    return {}


# ============================================================
# 2. PostToolUse フック: 監査ログ
# ============================================================

async def audit_log(input_data: dict, tool_use_id: str, context: Any) -> dict:
    """
    ツール実行後の監査ログ

    すべてのツール使用を記録（実際はファイルやDBに保存）
    """
    tool_name = input_data.get("tool_name", "Unknown")
    tool_input = input_data.get("tool_input", {})
    timestamp = datetime.now().strftime("%H:%M:%S")

    # ログ出力（実際はファイルやDBに保存）
    print(f"\n  📝 [PostToolUse AUDIT {timestamp}] {tool_name} 実行完了")

    return {}


# ============================================================
# 3. メイン処理（ClaudeSDKClientを使用）
# ============================================================

async def main():
    print("=" * 60)
    print("Claude Agent SDK - Hooks（ライフサイクル介入）")
    print("=" * 60)
    print()
    print("【登録したフック】")
    print("  - PreToolUse: security_check（.envブロック、危険コマンドブロック）")
    print("  - PostToolUse: audit_log（全ツールの監査ログ）")
    print()

    # Hooksの設定
    options = ClaudeAgentOptions(
        allowed_tools=["Write", "Edit", "Read", "Bash", "Glob"],
        permission_mode="acceptEdits",
        hooks={
            # PreToolUse: ツール実行前
            "PreToolUse": [
                HookMatcher(
                    hooks=[security_check],
                ),
            ],
            # PostToolUse: ツール実行後
            "PostToolUse": [
                HookMatcher(
                    hooks=[audit_log],
                ),
            ],
        },
    )

    # ClaudeSDKClientを使用（query()ではHooksが動作しない）
    async with ClaudeSDKClient(options=options) as client:

        # テスト1: 通常の操作（許可される）
        print("-" * 60)
        print("[テスト1] 通常のファイル操作")
        print("-" * 60)
        prompt1 = "sample_output ディレクトリにあるファイルを確認して、簡潔に教えてください"
        print(f"プロンプト: {prompt1}\n")

        await client.query(prompt1)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"\n[Claude] {block.text}")
                    elif hasattr(block, "name"):
                        print(f"\n[Tool] {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"\n[結果] {message.subtype}")

        print()
        print()

        # テスト2: .envファイルへのアクセス（ブロックされる）
        print("-" * 60)
        print("[テスト2] .envファイルへのアクセス（ブロックされるはず）")
        print("-" * 60)
        prompt2 = ".envファイルを作成して、SECRET_KEY=12345 と書き込んでください"
        print(f"プロンプト: {prompt2}\n")

        await client.query(prompt2)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"\n[Claude] {block.text}")
                    elif hasattr(block, "name"):
                        print(f"\n[Tool] {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"\n[結果] {message.subtype}")

    print()
    print("=" * 60)
    print("デモ完了")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
