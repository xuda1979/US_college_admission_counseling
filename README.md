# US College Admission Counseling Platform

This project provides a full-stack foundation for a US university counseling assistant that helps applicants evaluate and improve their applications using GPT-5 through the OpenAI API.

The repository now ships with a production-ready Docker image that bundles the API and the compiled React single-page application so that the platform can be deployed to a standard web server with a single command.

## Project Structure

```
.
├── backend/             # FastAPI application, models, services, and Alembic migrations
├── frontend/            # React + Vite dashboard for applicants
├── docs/                # Additional documentation and compliance guidance
└── README.md
```

## Backend Setup

1. Copy `.env.example` to `.env` and fill in the required secrets:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env to set OPENAI_API_KEY and JWT_SECRET_KEY
   ```

2. Install dependencies using [Poetry](https://python-poetry.org/):
   ```bash
   poetry install
   ```

3. Apply database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

4. Start the FastAPI server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

The backend exposes REST endpoints under `/api` for authentication, evaluations, essays, milestones, and suggestions. When a built frontend is available, it also serves the single-page dashboard under `/app`, making the platform fully web-based. It integrates with GPT-5 for holistic evaluations, improvement recommendations, and essay critiques.

## Frontend Setup

1. Install dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

2. Copy `.env.example` to `.env` (create manually) and configure the backend API URL:
   ```env
   VITE_API_URL=/api
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The React dashboard includes dedicated routes for the applicant overview, evaluation history, essay studio, and planner timeline. It uses React Query for data fetching and Axios for authenticated API calls.

4. Build the production assets so they can be served by FastAPI:
   ```bash
   npm run build
   ```

   The generated files live in `frontend/dist/`. The FastAPI app automatically serves this directory when `FRONTEND_BUILD_DIR` points to it (the default), so running `uvicorn` will host the API and the compiled web client together.

## Containerized Deployment

To deploy the full stack behind a single web service, use the provided Docker setup. The multi-stage image builds the React dashboard, installs the FastAPI backend, applies database migrations, and serves everything through Uvicorn.

1. Copy the Docker environment template and populate the required values:
   ```bash
   cp backend/.env.docker.example backend/.env.docker
   # Edit backend/.env.docker to set OPENAI_API_KEY and JWT_SECRET_KEY
   ```

2. Start the stack:
   ```bash
   docker compose up --build
   ```

   The service exposes port `8000` by default. Visit `http://localhost:8000/app` to access the frontend and `http://localhost:8000/docs` for the interactive API documentation. Static assets and the API share the same container, making deployment on platforms such as DigitalOcean, Fly.io, Render, or any Docker-compatible host straightforward.

3. To run database migrations manually (for example during upgrades), execute:
   ```bash
   docker compose run --rm web alembic upgrade head
   ```

## Documentation

Additional documentation lives under `docs/`:

- `docs/api.md` – Endpoint reference and usage examples
- `docs/prompts.md` – Prompt templates used for evaluations, recommendations, and essay reviews
- `docs/compliance.md` – Privacy and FERPA-style data protection guidelines

## Testing

You can run backend tests with:
```bash
cd backend
poetry run pytest
```

Frontend linting is available via:
```bash
cd frontend
npm run lint
```

## Security & Privacy

The platform includes JWT authentication, password hashing, and scaffolding for role-based access. Sensitive configuration is environment-driven. Review the compliance documentation before deploying to production.
