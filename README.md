# 🏗️ DDR Report Generator (AI-Powered)

An end-to-end AI system that converts **unstructured inspection + thermal PDF reports** into a **structured, client-ready Detailed Diagnostic Report (DDR)**.

---

## 🚀 Overview

This project solves a real-world problem:

> Converting messy inspection documents into actionable insights without manual effort.

The system:

* Parses raw PDFs
* Extracts structured observations using LLMs
* Applies rule-based reasoning
* Generates a professional DDR report

---

## 🧠 Key Features

* 📄 **PDF Parsing** (text + images extraction)
* 🤖 **LLM-based Information Extraction**
* 🧹 **Data Cleaning & Normalization**
* 🧠 **Merge Engine (Core Intelligence)**

  * Deduplication
  * Area normalization
  * Issue classification
  * Severity scoring
* 🌡️ **Thermal Data Interpretation**
* 📝 **Automated DDR Report Generation**
* ⚡ **Optimized Pipeline (batching + caching)**

---

## 🏗️ System Architecture

```text
PDF Reports
   ↓
Parser (PyMuPDF)
   ↓
LLM Extraction (Groq - LLaMA3)
   ↓
Merge Engine (Rules + Reasoning)
   ↓
DDR Generator (Structured Prompting)
   ↓
Final Report (Markdown)
```

---

## 📂 Project Structure

```
ddr_report_generator/
│
├── data/
│   ├── input/
│   └── output/
│
├── src/
│   ├── parser/
│   ├── extractor/
│   ├── merger/
│   ├── generator/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd ddr_report_generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variable

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Pipeline

```bash
python src/main.py
```

---

## 📊 Output

The system generates:

* 📄 Structured observations (JSON)
* 🧠 Merged & cleaned insights
* 📝 Final DDR report

Output location:

```
data/output/reports/final_ddr.md
```

---

## 🧠 Design Decisions

### 1. Hybrid AI Approach

Instead of relying purely on LLMs:

* LLM → extraction
* Rules → reasoning & reliability

---

### 2. Merge Engine (Core Innovation)

Handles:

* Area normalization (e.g., “Master Bedroom” → “Bedroom”)
* Deduplication
* Issue prioritization
* Severity scoring

---

### 3. Hallucination Control

* Strict prompting
* No assumption policy
* Missing data handled explicitly

---

### 4. Performance Optimization

* Batch processing (reduces API calls)
* Caching (avoids recomputation)
* Filtering low-signal pages

---

## ⚠️ Limitations

* Thermal-to-area mapping is approximate
* Depends on quality of input PDFs
* Some fields may be "Not Available" due to missing data

---

## 🔮 Future Improvements

* Image-based defect detection (CV)
* Better thermal-to-area alignment
* Web UI (Streamlit)
* Multi-property support

---

## 🎯 Conclusion

This project demonstrates a **production-style AI pipeline** combining:

* LLM capabilities
* Rule-based reasoning
* Real-world problem solving

---

## 👤 Author

**Atharva Dwivedi**

---
