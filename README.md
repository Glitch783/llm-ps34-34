# Company Policy Assistant (PS 34)

An enterprise-ready **Retrieval-Augmented Generation (RAG)** chatbot that helps employees quickly find answers from corporate policy documents (Leave, Business Travel, and Expense Reimbursements) with verified source citations.

---

## 📌 Problem Statement (PS 34)
* **Problem:** Employees struggle to find exact details across multiple scattered HR and finance policy manuals (leave types, travel allowances, reimbursement deadlines).
* **Solution:** An AI-powered RAG assistant that chunks and indexes policy PDFs into ChromaDB with source metadata. It retrieves relevant sections and uses Google Gemini to answer questions with verifiable file names and page numbers.

---

## 🚀 Key Features
* **Multi-PDF Policy Ingestion:** Pre-loaded with official sample policies (`Leave_Policy.pdf`, `Travel_Policy.pdf`, `Reimbursement_Policy.pdf`).
* **Vector Search with ChromaDB:** Splits documents into semantic chunks and stores embeddings with document metadata (`source`, `page`).
* **Zero-Hallucination Prompt Grounding:** Constrained to answer exclusively from retrieved context, preventing fabricated allowances or policies.
* **Source & Page Attribution:** Displays expandable badges showing the exact source policy PDF and page number used for each response.
* **Modern Editorial Lexicon UI (Option 1):** Executive legal & publication design inspired by Stripe Press and Notion, featuring a warm linen canvas (`#FAF8F5`), British Racing Green accents (`#14453D`), editorial serif typography (Fraunces & Inter), ledger telemetry strip, and academic footnote-style citations.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **LLM & API:** Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`) via `google-genai`
* **Vector Store:** ChromaDB
* **PDF Processing:** `pypdf`, `fpdf2`
* **UI Framework:** Streamlit

---

## ⚙️ How to Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Glitch783/llm-ps34-34.git
cd llm-ps34-34
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate sample policy PDFs (optional if already in `policies/`)
```bash
python generate_policies.py
```

### 4. Run the Streamlit application
```bash
streamlit run app.py
```

### 5. Using the App
1. Enter your **Google Gemini API Key** in the sidebar (get a free key at [Google AI Studio](https://aistudio.google.com/)).
2. Ask questions using the chat input or click one of the preset quick queries.
3. Review answers along with cited source files and page numbers!

---

## 📂 Project Structure
```text
llm-ps34-34/
├── app.py                   # Streamlit web application & chat UI
├── rag_pipeline.py          # ChromaDB indexing, embedding & RAG retrieval engine
├── generate_policies.py     # Script to generate sample policy PDFs
├── requirements.txt         # Project dependencies
├── .gitignore               # Excludes .env, venv/, and chroma_db/
├── README.md                # Project documentation
├── policies/                # HR Policy PDFs
│   ├── Leave_Policy.pdf
│   ├── Travel_Policy.pdf
│   └── Reimbursement_Policy.pdf
└── screenshots/             # Output test screenshots for submission
```

---

## 📸 Sample Outputs & Citations
* **Query:** *"How many days of paid leave can I carry forward to next year?"*
  * **Answer:** Employees can carry forward a maximum of 10 unused paid leaves to the next year.
  * **Citation:** `Leave_Policy.pdf` (Page 1)
* **Query:** *"What is the daily per diem allowance for domestic business travel?"*
  * **Answer:** The daily per diem is \$45 (INR 1,800) for domestic travel covering meals and incidentals without requiring itemized receipts.
  * **Citation:** `Travel_Policy.pdf` (Page 1)
