# Smart Resume Screener

A professional full-stack web application for intelligent resume parsing, screening, and shortlisting using Azure Document Intelligence and Google Gemini AI.

## Architecture

- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS (Black & White Professional Theme)
- **Backend**: FastAPI + Python 3.11
- **Database**: MongoDB Atlas
- **AI/ML**: Azure Document Intelligence + Google Gemini API
- **Auth**: JWT Bearer Tokens

## Features

- ✓ Resume upload (PDF/DOCX) with Azure Document Intelligence parsing
- ✓ AI-powered JSON extraction using Gemini with schema validation
- ✓ Job description matching with semantic scoring
- ✓ Profile editor for parsed resumes
- ✓ Advanced search and shortlisting
- ✓ JWT authentication
- ✓ GridFS storage for raw files
- ✓ Responsive black & white UI

## Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- MongoDB Atlas account (already configured)

### 1. Environment Setup

Create `.env` files in both backend and frontend directories:

**backend/.env**
```env
GEMINI_API_KEY=AIzaSyDScK_dcj0L1Vi2GKRGTOHYfY8YBkuSHaY
GEMINI_MODEL=gemini-pro
AZURE_DOC_INTELLIGENCE_ENDPOINT=https://arc1.cognitiveservices.azure.com/
AZURE_DOC_INTELLIGENCE_KEY=5CiYiFLezoXUdBJrQ9f5KxrQS4QBUG5Lm7tjdceRZsg1A5o1kEpeJQQJ99BJACqBBLyXJ3w3AAALACOGRIzy
MONGODB_URI=mongodb+srv://ARC-RESUME:69O52bQXpzSHroMS@clusterarc.kxpp16z.mongodb.net/
JWT_SECRET=your-secure-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440
DATABASE_NAME=resume_screener
ENVIRONMENT=development
```

**frontend/.env.local**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed demo user (optional)
python scripts/seed_user.py

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run at: http://localhost:3000

### 4. Default Credentials

```
Username: admin@resumescreener.com
Password: admin123
```

## 📁 Project Structure

```
smart-resume-screener/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration & env variables
│   │   ├── models.py               # Pydantic models
│   │   ├── database.py             # MongoDB connection
│   │   ├── auth.py                 # JWT authentication
│   │   ├── dependencies.py         # FastAPI dependencies
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py            # Auth endpoints
│   │   │   ├── resumes.py         # Resume CRUD endpoints
│   │   │   └── upload.py          # Upload & parsing endpoints
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── azure_parser.py    # Azure Doc Intelligence
│   │       ├── gemini_service.py  # Gemini LLM orchestration
│   │       ├── scoring.py         # Match scoring algorithm
│   │       └── storage.py         # GridFS storage
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_endpoints.py
│   ├── scripts/
│   │   └── seed_user.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx           # Landing/login page
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx       # Main dashboard
│   │   │   ├── upload/
│   │   │   │   └── page.tsx       # Upload interface
│   │   │   ├── resumes/
│   │   │   │   ├── page.tsx       # Resume list
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx   # Resume editor
│   │   │   └── search/
│   │   │       └── page.tsx       # Search & shortlist
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── UploadForm.tsx
│   │   │   ├── ResumeCard.tsx
│   │   │   ├── ResumeEditor.tsx
│   │   │   └── SearchFilters.tsx
│   │   ├── lib/
│   │   │   ├── api.ts             # API client
│   │   │   └── auth.ts            # Auth utilities
│   │   └── types/
│   │       └── index.ts           # TypeScript types
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.js
├── .env.example
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login` - Login with credentials
- `POST /api/auth/register` - Register new user

### Resume Operations
- `POST /api/upload` - Upload and parse resume
- `GET /api/resumes` - List all resumes (with filters)
- `GET /api/resumes/{id}` - Get single resume
- `PUT /api/resumes/{id}` - Update resume
- `DELETE /api/resumes/{id}` - Delete resume
- `POST /api/resumes/match` - Match resume against job description

### File Storage
- `GET /api/files/{file_id}` - Download original file

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Design System

The application uses a professional black & white theme:

- **Primary**: Black (#000000)
- **Secondary**: White (#FFFFFF)
- **Grays**: Various shades for depth
- **Accent**: Subtle gray highlights
- **Typography**: Inter font family
- **Design**: Clean, minimalist, corporate

## Security Features

- JWT bearer token authentication
- Password hashing with bcrypt
- Environment variable secrets
- Input validation with Pydantic
- CORS protection
- Rate limiting ready

## LLM Orchestration

The system uses Google Gemini for structured JSON extraction:

1. **Temperature**: 0.0-0.2 for deterministic output
2. **Schema Validation**: Pydantic models enforce structure
3. **Retry Logic**: Re-prompts once with stricter instructions on failure
4. **Fallback**: Rule-based parsing if LLM fails twice
5. **Few-shot Examples**: Included in prompt template

## Scoring Algorithm

The match score (0-100) combines:
- **Skills Overlap** (40%): Jaccard similarity of skills
- **Experience Match** (30%): Years and relevance
- **Education Match** (20%): Degree level and field
- **Semantic Similarity** (10%): Text embedding comparison

## 🚢 Production Deployment

### Backend (Python)
- Deploy to Railway, Render, or AWS Lambda
- Set environment variables in platform
- Use MongoDB Atlas connection string

### Frontend (Next.js)
- Deploy to Vercel or Netlify
- Set `NEXT_PUBLIC_API_URL` to backend URL
- Enable automatic deployments from Git

## License

MIT License

## Support

For issues or questions, please open a GitHub issue.

---

Built with passion using Next.js, FastAPI, MongoDB Atlas, Azure AI, and Google Gemini
