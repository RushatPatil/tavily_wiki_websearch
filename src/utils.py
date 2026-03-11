import os
import asyncio

from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

class Tools:
    def __init__(self):
        self.tavily = TavilySearch(
                api_key=os.getenv("TAVILY_API_KEY"),
                max_results=5,
                topic="news",
                include_answer=True,
                include_raw_content=True,
                include_images=False,
                include_image_descriptions=False,
                search_depth="advanced",
                time_range="year"
            )

        self.wiki = WikipediaQueryRun(
                api_wrapper=WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=10000)
            )


    async def async_search_tavily(self, questions_list: list) -> list:
        # Use asyncio.gather() to run all queries concurrently
        tasks = [self.tavily.arun({"query": question}) for question in questions_list]
        responses = await asyncio.gather(*tasks)

        results = []
        for question, response in zip(questions_list, responses):
            results.append({"query":question,"sources":[{"source_id":i+1,"content":item["content"]} for i, item in enumerate(response["results"])]})
        return results

    async def async_search_wiki(self, questions_list: list) -> list:
        # Use asyncio.gather() to run all queries concurrently
        tasks = [self.wiki.arun({"query": query}) for query in questions_list]
        responses = await asyncio.gather(*tasks)

        results = []
        for query, response in zip(questions_list, responses):
            print(f"Wiki response for '{query}': {response[:200]}...")
            # Wikipedia returns a single string, so we wrap it as one source
            results.append({"query":query,"sources":[{"source_id":1,"content":response}]})
        return results