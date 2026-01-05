"""
Claude Agent SDK 基本サンプル
============================
最もシンプルなquery()関数を使ったエージェントの例

このサンプルでは:
- query()関数の基本的な使い方
- エージェントからのメッセージ処理
- ストリーミング応答の受け取り方
を学びます。
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    print("=" * 50)
    print("Claude Agent SDK - 基本サンプル")
    print("=" * 50)
    print()

    # シンプルなプロンプトでエージェントを実行
    # query()は非同期イテレータを返し、エージェントの応答をストリーミングで受け取れる
    prompt = "現在のディレクトリにあるファイルを一覧表示して、簡単に説明してください。"

    print(f"プロンプト: {prompt}")
    print("-" * 50)
    print()

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            # 使用可能なツールを制限（セキュリティのため）
            allowed_tools=["Bash", "Read", "Glob"],
            # パーミッションモード: 読み取りのみなのでdefaultで十分
            permission_mode="default",
        ),
    ):
        # メッセージの種類に応じて処理を分岐
        if isinstance(message, AssistantMessage):
            # AssistantMessage: Claudeからの応答
            for block in message.content:
                if hasattr(block, "text"):
                    # テキストブロック: Claudeの説明や回答
                    print(f"[Claude] {block.text}")
                elif hasattr(block, "name"):
                    # ツール使用ブロック: どのツールを使ったか
                    print(f"[Tool] {block.name} を使用中...")

        elif isinstance(message, ResultMessage):
            # ResultMessage: エージェントの実行結果
            print()
            print("-" * 50)
            print(f"[結果] 完了: {message.subtype}")


if __name__ == "__main__":
    asyncio.run(main())
