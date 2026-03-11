from src.deployment import mcp

def main_call():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main_call()
