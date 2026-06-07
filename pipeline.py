from agents import build_search_agent,builder_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic : str) -> dict:

    state={}

    #search agent working
    print("\n"+"="*50)
    print("step 1 - search agent is working....")

    search_agent= build_search_agent()
    search_result =search_agent.invoke({
        "messages" : [{"role":"user", "content":f"Find recent , reliable and detailed information about:{topic}"}]
    })

    state["search_result"]=search_result['messages'][-1].content

    print("\n search result",state["search_result"])

    # step 2 - reader agent

    reader_agent= builder_reader_agent()
    reader_result=reader_agent.invoke({
        "messages":[
            {"role":"user","content":f"Based on the following search about {topic}"},
            {"role":"user","content":f"pick the most relevent URL and scrape it for deeper contant.\n"},
            {"role":"user","content":f"search result:\n{state['search_result'][:800]}"}
        ]
    })

    state["scraped_content"]= reader_result["messages"][-1].content

    print("\nscraped_content\n", state["scraped_content"])  

    #step 3 - writer code


    research_combined= (
        f"Search Result:\n{state['search_result']}\n\n"
        f"Detailed Scraped Content : \n{state['scraped_content']}"
    )

    state["report"]=writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    }
    )

    print("\n Final Reporet\n",state['report'])

    #critic report

    state["feedback"]=critic_chain.invoke({
        "report":state["report"]
    })

    print('\n critic report \n',state['feedback'])

    return state



if __name__=="__main__":
    topic=input("\n Enter a research topic :")
    run_research_pipeline(topic)

    
