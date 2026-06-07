from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily= TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """"
    Search all over the web and give me a information about all yet to be profitable
    small caps in stock market all over the world

    """
    result=tavily.search(query=query,max_results=5)

    out=[]

    for r in result["results"]:
        out.append(
            f"Title:{r['title']}\nURLs:{r['url']}\nSnippet:{r['content'][:500]}\r"
        )
    return '\n----\n'.join(out)


print(web_search.invoke("Which is the best stock?"))

@tool
def scrap_web(url:str) -> str:
    """"Scrap and return clean data from the given URL for deeper learning"""
    try:
        resp=requests.get(url,timeout=8,headers={"User_Agents":"Mozilla/5.0"})
        soup=BeautifulSoup(resp.text , "html-parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=' ',strip=True)[:300]
    except Exception as e:
        return f"Could not scrap URL : {str(e)}"



