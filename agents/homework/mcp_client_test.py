from fastmcp import Client
import weather_server
import asyncio

async def main():
    async with Client("weather_server.py") as mcp_client:
        tools = await mcp_client.list_tools()
        print(tools)

if __name__ == "__main__":
    test = asyncio.run(main())