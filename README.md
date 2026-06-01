markdown# Ujima SACCO — Multi-Agent Loan Triage Prototype

An autonomous multi-agent framework built with **CrewAI** and powered by **Groq (Llama 3.1)**. This system simulates an empathetic, harvest-aligned financial literacy and loan screening process for cooperative members in Kenya.

## 👥 The Agent Team

- **Financial Literacy Coach (Scout Agent)**: Detects seasonal financial stress signals, reviews harvest timelines, and drafts supportive member communications.
- **Loan Triage Officer (Guardian Agent)**: Conducts objective, non-biased risk analysis matching requested capital against cyclical agricultural yields.
- **Human-in-Loop Coordinator (Hunter Agent)**: Synthesizes automated risk profiles into high-dignity briefing packets assigned to matching human experts.

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd Ujima_Sacco_Agents
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Install requirements:
   ```bash
   pip install crewai litellm python-dotenv
   ```

4. Create a `.env` file and add your Groq credentials:
   ```text
   GROQ_API_KEY=your_secret_key_here
   ```

5. Execute the pipeline:
   ```bash
   python UJima_agents.py
   ```
