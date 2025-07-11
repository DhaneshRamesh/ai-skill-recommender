# 🧠 AI Skill Recommender (FastAPI Backend)

This is a FastAPI-based backend that extracts and recommends job-relevant skills from uploaded resumes (PDF/DOCX). It uses BERT-based Named Entity Recognition and Sentence Transformers for semantic matching with a custom skill database.

---

## 🚀 Features

* 🔍 **Skill Extraction**: Extracts entities from resumes using `dslim/bert-base-NER`
* 🧠 **Semantic Matching**: Matches extracted skills with predefined roles using `all-MiniLM-L6-v2`
* 📄 **File Upload**: Accepts `.pdf` and `.docx` resumes
* ⚡ **FastAPI**: Lightweight, blazing-fast backend with OpenAPI docs
* 🌐 **Auto-generated Swagger UI** at `/docs`

---

## 💪 Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/DhaneshRamesh/ai-skill-recommender.git
cd ai-skill-recommender
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install fastapi uvicorn python-multipart transformers torch sentence-transformers
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

### 4. Access the docs

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
You can test the `/recommend` endpoint here.

---

## 📁 Project Structure

```
.
├── main.py
├── data/
│   └── skills_db.json              # Predefined roles with skill lists
└── utils/
    ├── extract_text.py             # Extracts text from PDF and DOCX
    ├── extract_skills.py           # BERT-based skill extraction
    └── match_skills.py             # Embedding + semantic matching
```

---

## 📦 API Endpoint

### `POST /recommend`

**Form Data:**

* `file`: Resume file (.pdf or .docx)

**Response:**

```json
{
  "extracted_skills": ["Python", "SQL", "Machine Learning"],
  "recommended_roles": ["Data Scientist", "ML Engineer"]
}
```

---

## 💡 To-Do

* [ ] Deploy to Render/Hugging Face Spaces
* [ ] Add frontend (Streamlit or React)
* [ ] Improve model filtering and scoring

---

## 🤝 Contributors

* Dhanesh Ramesh
* Kaushik Narumanchi

---

## 📜 License

MIT License
