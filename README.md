LinkedIn AI Poster

A cutting-edge full-stack solution that seamlessly marries a React dashboard with a CrewAI multi-agent backend to research, draft, optimize, and publish LinkedIn posts — leveraging local Ollama/Mistral LLMs (you can use any LLM (llama3, deepseek-r1, qwen ...)) and real-time, topic-scoped trend data.
🚀 Key Features

    Topic-Scoped Trend Integration
    Fetches the top 3 trending headlines and links about your specified topic via Serper.dev for truly targeted, timely content.

    Configurable Agent Pipeline
    Modular YAML-driven agents handle research, planning, writing, SEO, review, export, and publishing—easily extendable and tunable.

    Local LLM Performance
    Runs on your hardware with Ollama/Mistral, ensuring fast, private, low-latency text generation.

    Automated Cadence
    Schedule new posts every quarter-hour or trigger them manually via the dashboard.

    React-Powered Dashboard
    Intuitive UI to enter topics, preview drafts, publish to LinkedIn, and view engagement metrics—all in one place.

    Markdown Archiving
    Each post is saved as timestamped Markdown for audit trails and future reuse.

🏗️ Architecture Overview

[React Frontend]  ↔  [FastAPI Backend]  ↔  [CrewAI Agents + Ollama]  ↔  [Serper & LinkedIn APIs]

    Frontend (React)

        Topic input, draft preview, publish button, metrics viewer

        Communicates with backend over secure REST endpoints

    Backend (FastAPI + CrewAI)

        Loads config/agents.yaml and config/tasks.yaml

        Orchestrates agents in a sequential pipeline

        Exposes /generate, /publish, and /metrics APIs

    Agents & Tools

        TrendAgent: fetch top-3 trending headlines about {topic}

        SearchAgent: gather detailed news summaries

        PlannerAgent: outline post structure

        WriterAgent: craft engaging copy

        SEOAgent: inject hashtags & keywords

        ReviewerAgent: polish grammar & style

        ExporterAgent: archive as Markdown

        PublisherAgent: post to LinkedIn API

⚙️ Installation

    Clone the repository

git clone https://github.com/yourorg/Linkedin-ai-poster.git
cd Linkedin-ai-poster/backend/linkedin/src/linkedin

Environment configuration
Create a .env file with:

    SERPER_API_KEY=your_serper_api_key
    OLLAMA_MODEL=mistral:latest
    LINKEDIN_ACCESS_TOKEN=your_li_token
    LINKEDIN_ORGANIZATION_ID=your_org_urn

Install Dependencies

pip install -r requirements.txt   # Backend
cd ../../frontend && npm install  # React UI

Launch Services

Backend:

    uvicorn main:app --reload --app-dir src/linkedin

Frontend:

        npm start

🚀 Getting Started

    Open your browser to http://localhost:3000.

    Enter a Topic and click Generate Draft.

    Review the AI-crafted post, then click Publish.

    Paste your LinkedIn post URN to Fetch Metrics in real-time.

🤝 Contributing

We welcome improvements! Fork, create a branch, submit a PR. Ideas include:

    New agent types (image, analytics, localization)

    Enhanced editor features in React

    Support for additional social platforms

Elevate your LinkedIn presence with data-driven, AI-powered content—automated end to end.
