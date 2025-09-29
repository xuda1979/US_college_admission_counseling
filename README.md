# US College Admission Counseling Platform

This project provides a full-stack foundation for a US university counseling assistant that helps applicants evaluate and improve their applications using GPT-5 through the OpenAI API.

## Project Structure

```
.
├── backend/             # FastAPI application, models, services, and Alembic migrations
├── frontend/            # React + Vite dashboard for applicants
├── docs/                # Additional documentation and compliance guidance
└── README.md
```

## Backend Setup

1. Install dependencies using [Poetry](https://python-poetry.org/):
   ```bash
   cd backend
   poetry install
   ```

2. Create a `.env` file inside `backend/` with the following variables:
   ```env
   OPENAI_API_KEY=your-openai-key
   DATABASE_URL=sqlite+aiosqlite:///./data/app.db
   JWT_SECRET_KEY=replace-with-strong-secret
   CORS_ORIGINS=http://localhost:5173
   FRONTEND_BUILD_DIR=../frontend/dist
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
