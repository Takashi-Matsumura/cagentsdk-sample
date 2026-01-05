"""
Claude Agent SDK - 会話型エージェント
====================================
ClaudeSDKClientを使った継続的な会話の例

このサンプルでは:
- ClaudeSDKClientの基本的な使い方
- 複数ターンの会話（コンテキスト保持）
- query()との違い
を学びます。

【重要な違い】
- query(): 毎回新しいセッション、前の会話を忘れる
- ClaudeSDKClient: 同じセッションで継続、会話履歴を保持
"""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    print("=" * 60)
    print("Claude Agent SDK - 会話型エージェント")
    print("=" * 60)
    print()
    print("【デモ】3ターンの会話でコンテキストが保持されることを確認")
    print()

    # エージェントのオプション設定
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Glob"],
        permission_mode="default",
    )

    # ClaudeSDKClientを使用（async withで自動接続/切断）
    async with ClaudeSDKClient(options=options) as client:

        # ===== ターン1: 最初の質問 =====
        print("-" * 60)
        print("[ターン1] このプロジェクトにあるPythonファイルを教えて")
        print("-" * 60)

        await client.query("このプロジェクトにあるPythonファイルを教えてください。")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"[Claude] {block.text}")
                    elif hasattr(block, "name"):
                        print(f"[Tool] {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"[結果] {message.subtype}")

        print()

        # ===== ターン2: 前の会話を踏まえた質問 =====
        print("-" * 60)
        print("[ターン2] その中で一番シンプルなのはどれ？")
        print("-" * 60)

        # 「その中で」→ 前のターンの結果を参照している
        await client.query("その中で一番シンプルなのはどれですか？理由も教えてください。")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"[Claude] {block.text}")
                    elif hasattr(block, "name"):
                        print(f"[Tool] {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"[結果] {message.subtype}")

        print()

        # ===== ターン3: さらに続ける =====
        print("-" * 60)
        print("[ターン3] それの行数を教えて")
        print("-" * 60)

        # 「それ」→ 前のターンで言及されたファイルを参照
        await client.query("それの行数を教えてください。")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"[Claude] {block.text}")
                    elif hasattr(block, "name"):
                        print(f"[Tool] {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"[結果] {message.subtype}")

    print()
    print("=" * 60)
    print("デモ完了: 3ターンの会話でコンテキストが保持されました")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
