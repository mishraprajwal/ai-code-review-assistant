# AI-Enabled Code Review Assistant

This project provides an AI-powered code review tool built with Java Spring Boot, Python, and TypeScript. It allows developers to paste code snippets and receive AI-generated feedback on code quality, potential bugs, performance, and best practices.

## Architecture

- **Backend**: Spring Boot REST API (Java) - Handles API requests and routes to AI service
- **AI Service**: Python Flask app with OpenAI integration - Processes code and generates reviews
- **Frontend**: React TypeScript app - User interface for code input and review display

## Prerequisites

- Java 17 or higher
- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API Key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

## Quick Start

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd ai-code-review-assistant
```

### 2. Configure OpenAI API Key

Create the `.env` file in the `ai` directory:

```bash
cd ai
cp .env.example .env  # If example exists, otherwise create .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Start All Services

Open **three separate terminals** and run each service:

#### Terminal 1: Backend (Port 8081)
```bash
cd backend
./mvnw spring-boot:run
```

#### Terminal 2: AI Service (Port 5000)
```bash
cd ai
# Create virtual environment (first time only)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

#### Terminal 3: Frontend (Port 5173)
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application

Open your browser and go to: **http://localhost:5173**

## Detailed Setup

### Backend Setup
```bash
cd backend
./mvnw clean compile  # Compile the project
./mvnw spring-boot:run  # Start the server
```
- **Port**: 8081
- **Endpoint**: `POST /api/review` - Accepts code as plain text, returns JSON with feedback

### AI Service Setup
```bash
cd ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
- **Port**: 5000
- **Endpoint**: `POST /review` - Accepts code, returns AI-generated review
- **Environment**: Requires `OPENAI_API_KEY` in `.env` file

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Development server
npm run build  # Production build
npm run preview  # Preview production build
```
- **Port**: 5173 (development), 4173 (preview)
- **Tech Stack**: React 19, TypeScript, Vite

## Testing

### Backend Tests
```bash
cd backend
./mvnw test
```

### AI Service Tests
```bash
cd ai
source .venv/bin/activate
python -m pytest test_app.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Usage

1. **Start all three services** as described in Quick Start
2. **Open the frontend** at http://localhost:5173
3. **Paste your code** into the textarea
4. **Click "Review Code"** to get AI feedback
5. **View the results** in the feedback section below

### Example Code Review
The AI will analyze your code for:
- Code quality and readability
- Potential bugs and security issues
- Performance optimizations
- Best practices and suggestions
- Time and space complexity analysis

## API Endpoints

### Backend API
- `POST /api/review` - Submit code for review
  - **Body**: Plain text code
  - **Response**: JSON `{"feedback": "AI review text"}`

### AI Service API
- `POST /review` - Process code review
  - **Body**: Plain text code
  - **Response**: JSON `{"feedback": "AI review text"}`

## Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Java 17+ is installed: `java -version`
- Check if port 8081 is available

**AI service fails:**
- Verify OpenAI API key is set in `ai/.env`
- Check API key has sufficient credits
- Ensure Python virtual environment is activated

**Frontend issues:**
- Run `npm install` to install dependencies
- Check if ports 5173 and 8081 are available
- Clear browser cache if UI doesn't update

**CORS errors:**
- Ensure backend is running on port 8081
- Check that frontend is accessing the correct backend URL

### Port Configuration
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8081
- **AI Service**: http://localhost:5000

### Logs
- **Backend**: Check terminal output or `backend/logs/`
- **AI Service**: Check terminal output
- **Frontend**: Check browser console (F12)

## Development

### Project Structure
```
ai-code-review-assistant/
├── backend/          # Spring Boot application
├── ai/              # Python Flask service
├── frontend/        # React TypeScript app
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

### Adding Features
- **Backend**: Add endpoints in `CodeReviewController.java`
- **AI Service**: Modify `app.py` for different AI providers
- **Frontend**: Update `App.tsx` for new UI features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.