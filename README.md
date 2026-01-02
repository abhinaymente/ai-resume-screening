# 🤖 AI Resume Screening & Interview Automation Platform

A full-stack AI-powered hiring automation system that screens resumes, shortlists candidates, and sends automated interview emails using Google services — all through a clean web interface.

This project focuses on eliminating manual resume screening for fresher hiring and demonstrates real-world backend automation using AI and cloud APIs.

## 🔗 Live Demo
[**Click here to use the App**](https://ai-resume-screening-lw5y.vercel.app/)

---

## 🌟 Key Highlights

- End-to-end **AI-driven resume screening**
- Works with **any Google Form**
- Automated **candidate email communication**
- Interview scheduling logic with **Google Meet links**
- Production-style backend design
- Clean, recruiter-friendly UI

---


## 🚀 Features

- 📄 Resume intake via **Google Forms**
- 📊 Dynamic data fetching from **Google Sheets**
- ☁️ Resume download from **Google Drive**
- 🧠 AI-based eligibility decision using **Groq LLM**
- 📧 Automated email notifications (shortlisted / rejected)
- 🎥 Google Meet link generation for interviews
- 🌐 Modern FastAPI-based web dashboard
- 🔁 Reusable backend (no code change per form)

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Groq LLM (LLaMA-based)

### Google Services
- Google Sheets API
- Google Drive API
- Gmail API (OAuth 2.0)

### Frontend
- HTML, CSS (Clean UI)

---

## 🧩 System Architecture

- Google Form  
- Google Sheets  
- Flask Backend  
- Google Drive (Resume Download & Extraction)  
- AI Resume Evaluation (Groq)  
- Email Notification with Google Meet Link  

---

## ⚙️ Workflow Explained

1. Recruiter creates a Google Form with resume upload  
2. Form responses are stored in Google Sheets  
3. Recruiter pastes the Sheet link into the web app  
4. Backend downloads resumes from Drive  
5. Resume text is extracted (PDF/DOC)  
6. AI evaluates candidate eligibility  
7. Eligible candidates receive interview emails with Meet links  

---

📌 Use Cases

Fresher hiring automation

Campus placement screening

HR resume shortlisting

Internal recruitment tools

---


## ✅ Why this is BETTER

- ✔ Honest
- ✔ Technically correct
- ✔ Interview-safe
- ✔ Recruiter-friendly
- ✔ No false claims

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/abhinaymente/ai-resume-screening.git
cd ai-resume-screening
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key
GOOGLE_CREDENTIALS=base64_encoded_service_account_json
GMAIL_TOKEN=base64_encoded_gmail_token_json
```

### 4. Run the Application
```bash
uvicorn backend.main:app --reload
```

---

## 👤 Author

**Abhinay Mente**  
Computer Science Engineering Student  

- Interested in backend development, AI-driven automation, and cloud-based systems  
- Experienced in building end-to-end applications using Python, FastAPI, and APIs  
- Actively exploring real-world problem solving through projects  

📌 This project was built as a hands-on learning initiative to understand how AI and cloud services can be combined to automate real hiring workflows.
