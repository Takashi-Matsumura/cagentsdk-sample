"""
Claude Agent SDK - カスタムツール定義
====================================
独自のツールを作成してエージェントに渡す例

このサンプルでは:
- @toolデコレータでカスタムツールを定義
- create_sdk_mcp_serverでMCPサーバーを作成
- ClaudeSDKClientでカスタムツールを使用
を学びます。

【重要】
- query()はカスタムツール未対応 → ClaudeSDKClientを使う
- ツール名は mcp__{server_name}__{tool_name} 形式
- 戻り値は {"content": [{"type": "text", "text": "..."}]} 形式
"""

import asyncio
from typing import Any

from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    ClaudeSDKClient,  # query()ではなくClaudeSDKClientを使用
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
)


# ============================================================
# 1. カスタムツールの定義（@toolデコレータを使用）
# ============================================================

@tool(
    "add",                          # ツール名
    "2つの数値を足し算します",        # ツールの説明（AIがツール選択時に参照）
    {"a": float, "b": float}        # パラメータのスキーマ
)
async def add_numbers(args: dict[str, Any]) -> dict[str, Any]:
    """加算ツール"""
    a, b = args["a"], args["b"]
    result = a + b
    print(f"       [実行] add({a}, {b}) = {result}")
    return {
        "content": [{
            "type": "text",
            "text": f"{a} + {b} = {result}"
        }]
    }


@tool(
    "multiply",
    "2つの数値を掛け算します",
    {"a": float, "b": float}
)
async def multiply_numbers(args: dict[str, Any]) -> dict[str, Any]:
    """乗算ツール"""
    a, b = args["a"], args["b"]
    result = a * b
    print(f"       [実行] multiply({a}, {b}) = {result}")
    return {
        "content": [{
            "type": "text",
            "text": f"{a} × {b} = {result}"
        }]
    }


@tool(
    "celsius_to_fahrenheit",
    "摂氏温度を華氏温度に変換します",
    {"celsius": float}
)
async def temperature_convert(args: dict[str, Any]) -> dict[str, Any]:
    """温度変換ツール"""
    celsius = args["celsius"]
    fahrenheit = (celsius * 9 / 5) + 32
    print(f"       [実行] celsius_to_fahrenheit({celsius}) = {fahrenheit:.1f}")
    return {
        "content": [{
            "type": "text",
            "text": f"{celsius}°C = {fahrenheit:.1f}°F"
        }]
    }


# ============================================================
# 2. MCPサーバーの作成（ツールをグループ化）
# ============================================================

calculator_server = create_sdk_mcp_server(
    name="calculator",      # サーバー名
    version="1.0.0",
    tools=[                 # 登録するツール
        add_numbers,
        multiply_numbers,
        temperature_convert,
    ]
)


# ============================================================
# 3. エージェントの実行（ClaudeSDKClientを使用）
# ============================================================

async def main():
    print("=" * 60)
    print("Claude Agent SDK - カスタムツール定義")
    print("=" * 60)
    print()
    print("【登録したツール】")
    print("  - mcp__calculator__add")
    print("  - mcp__calculator__multiply")
    print("  - mcp__calculator__celsius_to_fahrenheit")
    print()

    # エージェントのオプション設定
    options = ClaudeAgentOptions(
        # カスタムMCPサーバーを登録
        mcp_servers={"calculator": calculator_server},
        # 使用可能なツールを指定（カスタムツールのみに制限）
        allowed_tools=[
            "mcp__calculator__add",
            "mcp__calculator__multiply",
            "mcp__calculator__celsius_to_fahrenheit",
        ],
    )

    # ClaudeSDKClientを使用（カスタムツールはquery()未対応のため）
    async with ClaudeSDKClient(options=options) as client:

        # プロンプト：複数の計算を依頼
        prompt = """
以下の計算をしてください：
1. 123 + 456
2. 7 × 8
3. 25°C は華氏で何度？
"""

        print(f"プロンプト: {prompt}")
        print("-" * 60)

        await client.query(prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"[Claude] {block.text}")
                    elif hasattr(block, "name"):
                        # ツール使用を検出
                        print(f"\n[Tool] {block.name}")

            elif isinstance(message, ResultMessage):
                print()
                print("-" * 60)
                print(f"[結果] 完了: {message.subtype}")


if __name__ == "__main__":
    asyncio.run(main())
