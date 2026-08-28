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
