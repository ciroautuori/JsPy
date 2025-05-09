# JsPy Portfolio Backend

A robust FastAPI backend application for portfolio management with static file handling, PostgreSQL database, and Docker containerization.

## Features

- **FastAPI Backend**: High-performance REST API built with FastAPI
- **PostgreSQL Database**: Reliable data persistence with PostgreSQL
- **Docker Support**: Containerized deployment with Docker and docker-compose
- **Static File Handling**: Built-in support for static files and images
- **Authentication**: JWT-based authentication with refresh tokens
- **Project Management**: CRUD operations for portfolio projects
- **User Management**: User authentication and authorization system

## Prerequisites

- Docker and Docker Compose
- Python 3.13+
- PostgreSQL 13+

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/ciroautuori/jspy.git
cd jspy
```

2. Start the application using Docker Compose:
```bash
docker-compose up -d
```

The application will be available at `http://localhost:8002`

## Manual Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit .env with your configurations
```

4. Run the application:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── crud/         # Database operations
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── static/       # Static files
│   ├── tests/            # Test suite
│   └── requirements.txt  # Python dependencies
└── docker-compose.yaml   # Docker composition
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `STATIC_FILES_DIR`: Static files directory path

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@ciroautuori](https://twitter.com/ciroautuori)

Project Link: [https://github.com/ciroautuori/jspy](https://github.com/ciroautuori/jspy)