# ResearchBot-AI-Research-Pipeline
An autonomous multi-agent research pipeline that searches, scrapes, writes, and critiques research reports on any topic — powered by LangChain agents and a Streamlit UI.
ResearchBot runs a 4-step agentic pipeline:
🔍 Search Agent  →  📄 Reader/Scraper Agent  →  ✍️ Writer Chain  →  🔍 Critic Chain
RAG Project/
├── app.py                # Streamlit UI
├── pipeline.py           # Main pipeline orchestrator
├── agents.py             # Search & Reader agent definitions
├── tools.py              # Custom tools (search, scraper, etc.)
├── requirements.txt      # Python dependencies
└── .env                  # API keys (never commit this)
Deploy to Streamlit Cloud (Free Public URL)

 1.Push your project to GitHub (make sure .env is in .gitignore)
 2.Go to share.streamlit.io and sign in with GitHub
 3.Click New App → select your repo → set main file to app.py
 4.Under App Settings → Secrets, add your API keys:
  Tech Stack
 Author
Built by Hafeez — AI/ML Engineer in training, focused on LLM, RAG, and Generative AI.
