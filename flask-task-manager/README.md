# Flask Task Manager

A simple, modern web application for managing tasks with a clean interface and REST API.

## Features

- **CRUD Operations**: Create, read, update, and delete tasks
- **Modern UI**: Responsive design with gradient styling
- **REST API**: JSON endpoints for task management
- **Docker Ready**: Containerized deployment option
- **Lightweight**: File-based storage using JSON

## Quick Start

### Local Development

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd flask-task-manager
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   # source venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies and run:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

4. **Open your browser:** http://localhost:5000

### Docker Deployment

**Basic usage:**
```bash
docker build -t flask-task-manager .
docker run -p 5000:5000 flask-task-manager
```

**With data persistence:**
```bash
# Development (mount local file)
docker run -p 5000:5000 -v ${PWD}/tasks.json:/app/tasks.json flask-task-manager

# Production (named volume)
docker volume create task-data
docker run -p 5000:5000 -v task-data:/app flask-task-manager
```

## Usage

### Web Interface
- Navigate to http://localhost:5000/tasks
- Use the form to add new tasks with name and author
- Click tasks to edit or delete them

### REST API
- `GET /api/tasks` - Retrieve all tasks
- `POST /tasks` - Create new task (JSON: `{"name": "...", "author": "..."}`)
- `PUT /tasks/<name>` - Update task
- `DELETE /tasks/<name>` - Delete task
- `GET /health` - Health check endpoint

## Project Structure

```
flask-task-manager/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── tasks.json         # Task data storage
└── templates/
    └── index.html     # Web interface
```

## Technical Details

- **Backend**: Flask 3.1.1 with Python 3.10+
- **Storage**: JSON file (`tasks.json`)
- **Frontend**: Vanilla JavaScript with modern CSS
- **Container**: Alpine Linux base image
- **Port**: 5000 (configurable via `PORT` environment variable)

## Requirements

- Python 3.10 or higher
- Flask 3.1.1 (see `requirements.txt` for full dependencies)
- Docker (optional, for containerized deployment)

## Data Format

Tasks are stored as JSON objects with the following structure:
```json
{
  "task_name": {
    "author": "author_name",
    "date_create": "YYYY-MM-DD"
  }
}
```

## Troubleshooting

- **Port already in use**: Change port with `PORT=8000 python app.py`
- **Permission denied on tasks.json**: Ensure the file is writable
- **Docker build fails**: Check Docker daemon is running and try `docker system prune`

