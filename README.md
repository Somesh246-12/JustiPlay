# JustiPlay  
## Gamified AI-Powered Practical Legal Education & Legal Awareness Platform

---

## 📌 Overview

Legal education is largely theoretical, leaving law students with limited practical exposure before entering real legal practice. At the same time, many citizens struggle to understand basic legal documents and procedures due to the high cost and complexity of professional legal services.

**JustiPlay** is a gamified, AI-assisted platform designed to address both problems in a **safe, ethical, and compliant manner**. It enables law students to gain hands-on practical experience through AI-driven simulations, while helping citizens improve legal awareness—**without providing legal advice or replacing professional legal services**.

---

## 🎯 Objectives

- Provide structured, practical legal training to law students  
- Simulate real-world legal interactions using AI  
- Improve communication, reasoning, and ethical awareness  
- Promote legal literacy among citizens  
- Ensure strict compliance with legal and regulatory norms  
- Build a scalable LegalTech + EdTech solution  

---

## 👥 User Roles

### 1. Law Student
- Participates in gamified learning levels  
- Interacts with AI mock clients  
- Practices legal reasoning and questioning  
- Receives structured AI feedback  

### 2. Citizen (Legal Awareness Seeker)
- Uploads legal documents for understanding  
- Receives plain-language summaries and risk indicators  
- Interacts with learners for **educational explanations only**

---

## 🧩 Platform Structure

### 🔹 Law Student Flow
- Login & role selection  
- Beginner → Intermediate → Advanced levels  
- AI Mock Client interaction (text + voice)  
- AI-based evaluation:
  - Clarity
  - Relevance
  - Ethical compliance  
- Session-based feedback and learning summary  

### 🔹 Citizen Flow
- Login as citizen  
- Document upload and analysis  
- Risk-level indication (Low / Medium / High)  
- View learner profiles  
- Request educational explanations (no advice)

---

## 🤖 AI Features

### AI Mock Client
- Simulates real client behavior  
- Multi-turn conversation memory  
- Natural language responses  
- Emotion-aware variation  

### AI Evaluation Engine
- Evaluates student questions (not legal correctness)  
- Focuses on:
  - Communication clarity  
  - Logical reasoning  
  - Ethical phrasing  
- Provides educational feedback only  

### Voice Interaction
- Speech-to-Text (student input)  
- Text-to-Speech (AI client responses)  
- Improves realism and engagement  

---

## ⚖️ Legal & Ethical Compliance

JustiPlay is **BCI-compliant by design**:

- ❌ No legal advice  
- ❌ No lawyer advertising  
- ❌ No legal representation  
- ❌ No certifications or professional claims  
- ✅ Educational simulations only  
- ✅ Mandatory disclaimers at every stage  
- ✅ Students identified strictly as learners  
- ✅ AI acts as an assistant and evaluator, not a decision-maker  

---

## 🏗️ Technology Stack

### Frontend
- HTML, CSS, JavaScript  
- Tailwind CSS  
- Role-based dashboards  

### Backend
- Python (Flask)  
- Blueprint-based modular architecture  
- Session-based role handling  

### AI & ML
- Google Vertex AI (Gemini)  
- Prompt-engineered simulations  
- Controlled generation for safety  

### Security
- Environment-based secrets  
- `.gitignore` for credentials  
- Role-based access control  

---

## 📂 Project Structure

```text
JustiPlay/
│
├── app.py
├── config.py
├── routes/
│   ├── auth.py
│   ├── student.py
│   ├── citizen.py
│   └── document.py
│
├── services/
│   └── ai/
│       ├── client_ai.py
│       └── evaluator_ai.py
│
├── templates/
│   ├── auth/
│   ├── student/
│   └── citizen/
│
├── static/
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run the Project

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/justiplay.git](https://github.com/your-username/justiplay.git)
cd justiplay
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Google Vertex AI Credentials

### 5. Run the application
```bash
python app.py
```
### 6. Open in browser
Visit the following URL to view the platform:
http://localhost:5000

---

## 🌍 Social Impact

- Improves employability and confidence of law students
- Reduces inequality in access to legal understanding
- Encourages ethical legal practice from early stages
- Supports legal literacy without commercialization

---

## 🔮 Future Scope

- Multiple case scenarios
- Advanced learning analytics
- Multilingual support
- University and NGO partnerships
- Academic certification programs
- Research datasets for legal education

---

## 🏁 Conclusion

JustiPlay reimagines legal education by shifting from passive theory to active, experiential learning. By combining AI-driven simulations, gamification, and ethical safeguards, it creates a scalable platform that benefits both law students and society—without crossing legal or regulatory boundaries.


