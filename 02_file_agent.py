"""
Claude Agent SDK - ファイル操作エージェント
==========================================
Write/Editツールを使ったファイル操作の例

このサンプルでは:
- Writeツールで新規ファイル作成
- Readツールでファイル内容確認
- Editツールで既存ファイルの編集
- permission_mode="acceptEdits" の動作
を学びます。
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    print("=" * 60)
    print("Claude Agent SDK - ファイル操作エージェント")
    print("=" * 60)
    print()

    # エージェントへの指示
    # 複数のステップを含むタスクを依頼
    prompt = """
以下のタスクを順番に実行してください：

1. `sample_output/hello.py` というファイルを作成し、"Hello, World!"を出力するPythonコードを書いてください
2. 作成したファイルの内容を確認してください
3. そのファイルを編集して、ユーザーの名前を入力として受け取り、挨拶するように改良してください
4. 最終的なコードを表示してください

※ sample_outputディレクトリがなければ作成してください
"""

    print(f"プロンプト: {prompt}")
    print("-" * 60)
    print()

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            # ファイル操作に必要なツールを許可
            allowed_tools=["Write", "Edit", "Read", "Bash", "Glob"],
            # ファイル編集を自動承認（重要！）
            # これがないと毎回確認プロンプトが出る
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(f"[Claude] {block.text}")
                elif hasattr(block, "name"):
                    # ツール名と入力を表示
                    tool_name = block.name
                    print(f"\n[Tool] {tool_name} を使用中...")

                    # ツールの入力内容も表示（学習用）
                    if hasattr(block, "input"):
                        input_data = block.input
                        if tool_name == "Write" and "file_path" in input_data:
                            print(f"       → ファイル作成: {input_data.get('file_path')}")
                        elif tool_name == "Edit" and "file_path" in input_data:
                            print(f"       → ファイル編集: {input_data.get('file_path')}")
                        elif tool_name == "Read" and "file_path" in input_data:
                            print(f"       → ファイル読取: {input_data.get('file_path')}")

        elif isinstance(message, ResultMessage):
            print()
            print("-" * 60)
            print(f"[結果] 完了: {message.subtype}")


if __name__ == "__main__":
    asyncio.run(main())
