# AI-Powered Full-Stack Personal Portfolio

A production-quality personal portfolio demonstrating full-stack engineering, AI/ML capabilities, DevOps, and more.

## Architecture
- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **AI/ML**: RAG (pgvector), LLM APIs
- **Infrastructure**: Docker, Docker Compose

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- Docker & Docker Compose

### Environment Variables
Copy `.env.example` to `.env` and fill in the required values:
```bash
cp .env.example .env
```

### Local Development (Docker)
To start the entire stack:
```bash
docker-compose up -d --build
```
This will start:
- Nginx Reverse Proxy on port 80
- Next.js Frontend (internal)
- Django Backend (internal)
- PostgreSQL & Redis (internal)

### Production Deployment
The project is containerized for production out-of-the-box. Ensure your production `.env` is secure:
1. Set `DEBUG=False`
2. Configure `CORS_ALLOWED_ORIGINS` (e.g., `https://myportfolio.com`)
3. Use strong passwords for PostgreSQL.

### CI/CD
A GitHub Actions workflow is included (`.github/workflows/ci.yml`) to automatically lint, build, and test the application on pushes to the `main` branch.

## API Endpoints

| Method | Endpoint | Purpose |
| ------ | -------- | ------- |
| GET | `/api/projects/` | Retrieve and search projects |
| GET | `/api/skills/` | Retrieve skills |
| GET | `/api/github/repositories/` | Fetch cached GitHub repositories |
| GET | `/api/analytics/summary/` | Retrieve analytics overview |
| POST | `/api/analytics/track/` | Record portfolio events |
| POST | `/api/contact/` | Submit contact form |
| GET | `/api/health/` | Production health check & DB status |
| POST | `/api/ai/search/` | Semantic knowledge base search |
