# 🚀 Hybrid AI Log Classification API

A highly scalable, cost-effective REST API built with **FastAPI** to automatically categorize unstructured server and application logs.

Instead of relying on a single, expensive Large Language Model to process millions of logs, this system utilizes a **three-tier cascading architecture** to optimize for latency, compute efficiency, and financial cost.

## 🧠 System Architecture

The API routes incoming logs through three specialized layers:

1. **Tier 1: Deterministic Layer (Regex)** - Instantly catches known, repetitive system logs (e.g., "Backup successful") with zero latency and zero compute cost.
2. **Tier 2: Semantic ML Layer (BERT + Logistic Regression)** - Translates text into vector embeddings using a local Sentence Transformer (`all-MiniLM-L6-v2`). A pre-trained Logistic Regression model classifies standard errors. If the confidence score drops below 0.5, it flags the log as "Unclassified" to prevent silent failures.
3. **Tier 3: Zero-Shot Fallback (LLM)** - "Unclassified" edge-cases are routed to a Groq-hosted Llama-3 API. A highly constrained prompt forces the LLM to categorize novel anomalies without hallucinating.

## ✨ Key Features

- **Live Interactive Dashboard:** Fully documented Swagger UI (`/docs`).
- **Bulk Processing:** Upload massive CSV files and receive fully classified datasets in seconds.
- **Cost-Optimized:** Filters 80%+ of logs through local, free compute (Regex/BERT) before ever touching a paid LLM API.
- **Stateless Inference:** Safe from data leakage or catastrophic forgetting during production runtime.

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **Machine Learning:** Scikit-Learn, SentenceTransformers (Hugging Face)
- **LLM Integration:** Groq API (Llama-3)
- **Data Processing:** Pandas, NumPy
- **Deployment:** Render (Cloud PaaS)

<!-- ## 🌐 Live Demo

The API is successfully deployed to the cloud. You can test the interactive dashboard here:
👉 **[Click Here for the Live API Dashboard](https://YOUR_RENDER_URL.onrender.com/docs)** _(Replace with your actual Render URL)_ -->

## 💻 Local Installation & Setup

If you wish to run this pipeline locally, follow these steps:

**1. Clone the repository**

```bash
git clone [https://github.com/YOUR_USERNAME/log-classification-api.git](https://github.com/YOUR_USERNAME/log-classification-api.git)
cd log-classification-api
2. Install dependencies

Bash
pip install -r requirements.txt
3. Set up environment variables
Create a .env file in the root directory and add your Groq API key:

Code snippet
GROQ_API_KEY=your_actual_api_key_here
4. Run the server

Bash
uvicorn server:app --reload
The API will be accessible at http://127.0.0.1:8000/docs.

📡 API Endpoints
POST /classify/single: Accepts a single log string and returns the predicted category and the pipeline tier used.

POST /classify/csv: Accepts a CSV file upload, processes the batch efficiently through the pipeline, and returns a downloadable, classified CSV file.
```
