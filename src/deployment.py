from mcp.server.fastmcp import FastMCP
from utils import Tools
import asyncio
import json 

tools = Tools()

mcp = FastMCP("WebSearch_WikiSearch")

@mcp.tool()
async def web_search(questions: str) -> dict:
    """
    Accepts a dictionary containing two keys of search queries derived from decomposed claims
    and performs parallel web searches using **Tavily and Wikipedia** to retrieve relevant,
    factual information.

    Args:
        questions: A dictionary with two keys - one for Tavily questions and one for Wikipedia questions,
                   each containing a list of queries.

            {
                "tavily_questions" : ["The original Tavily question used for search", "...", ...],
                "wikipedia_questions" : ["The original Wikipedia keyword query used for search", "...", ...]
            }

        Example:
            {
                "tavily_questions" : ["What is India's GDP growth rate in 2024?",
                                      "Which G20 nation had the highest GDP growth in 2024?"],
                "wikipedia_questions" : ["India GDP growth 2024",
                                         "G20 economies GDP ranking"]
            }

    Returns:
        A dictionary with status, message, and data fields for consistent agent consumption:

        Structure - Success Example :-
            {
                "status": "success",
                "message": "Successfully retrieved 2 Tavily results and 2 Wikipedia results",
                "data": {
                    "tavily_results": [
                        {
                            "query": "What is India's GDP growth rate in 2024?",
                            "sources": [
                                {"source_id": 1, "content": "India's GDP grew at 8.2% in 2024..."},
                                {"source_id": 2, "content": "Economic analysts report..."},
                                ...
                            ]
                        },
                        {
                            "query": "Which G20 nation had the highest GDP growth in 2024?",
                            "sources": [
                                {"source_id": 1, "content": "Among G20 nations, India led with 8.2%..."},
                                {"source_id": 2, "content": "The top performing economies..."},
                                ...
                            ]
                        }
                    ],
                    "wiki_results": [
                        {
                            "query": "India GDP growth 2024",
                            "sources": [
                                {"source_id": 1, "content": "India's economy is the 5th largest by nominal GDP..."},
                                {"source_id": 2, "content": "The economic growth trends..."},
                                ...
                            ]
                        },
                        {
                            "query": "G20 economies GDP ranking",
                            "sources": [
                                {"source_id": 1, "content": "The G20 comprises 19 countries and the EU..."},
                                {"source_id": 2, "content": "Member nations account for..."},
                                ...
                            ]
                        }
                    ]
                }
            }

        Structure - Error Example :-
            {
                "status": "error",
                "message": "Error searching information from internet: API rate limit exceeded",
                "data": {
                    "tavily_results": [],
                    "wiki_results": []
                }
            }
    """
    try:

        if isinstance(questions,str):
            questions = json.loads(questions)
            print(questions)

        print("Checkpoint 1")
        tavily_results, wiki_results = await asyncio.gather(
            tools.async_search_tavily(questions_list=questions['tavily_questions']),
            tools.async_search_wiki(questions_list=questions['wikipedia_questions'])
        )

        # Return structured response with status and message
        return {
            "status": "success",
            "message": f"Successfully retrieved {len(tavily_results)} Tavily results and {len(wiki_results)} Wikipedia results",
            "data": {
                "tavily_results": tavily_results,
                "wiki_results": wiki_results
            }
        }

    except Exception as e:
        # Return consistent structure even on error
        return {
            "status": "error",
            "message": f"Error searching information from internet: {str(e)}",
            "data": {
                "tavily_results": [],
                "wiki_results": []
            }
        }


if __name__ == "__main__":
    mcp.run()