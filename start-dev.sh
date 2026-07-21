#!/bin/bash
# AstraIX Security Analyst - Development Startup Script
# Usage: ./start-dev.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════╗"
echo "║    AstraIX Security Analyst - Dev Startup         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please ensure Python 3.12 is installed."
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1 | grep -oE "3\.[0-9]+")
if [ "$PYTHON_VERSION" != "3.12" ]; then
    echo "⚠️  Warning: Expected Python 3.12, found $PYTHON_VERSION"
fi
echo "   ✅ Python $(python --version)"
echo ""

# Check if services are already running
echo "🔍 Checking running services..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ⚠️  Backend already running on port 8000"
else
    echo "   ℹ️  Backend not running"
fi

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "   ⚠️  Frontend already running on port 3000"
else
    echo "   ℹ️  Frontend not running"
fi
echo ""

# Start Backend
echo "🚀 Starting Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

source venv/bin/activate

# Check dependencies
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "   Starting FastAPI server..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "   Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "   ✅ Backend is ready!"
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo ""

# Start Frontend
echo "🎨 Starting Frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "⚠️  Installing frontend dependencies..."
    npm install --silent
fi

echo "   Starting Next.js dev server..."
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "   Waiting for frontend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "   ✅ Frontend is ready!"
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 1
fi
echo ""

echo "╔════════════════════════════════════════════════════╗"
echo "║         ✅ All Services Started Successfully       ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📍 Services:"
echo "   • Backend API:  http://localhost:8000"
echo "   • Swagger UI:   http://localhost:8000/docs"
echo "   • Frontend:     http://localhost:3000"
echo ""
echo "🛑 To stop all services, press Ctrl+C or run:"
echo "   pkill -f 'uvicorn app.main:app'"
echo "   pkill -f 'next dev'"
echo ""
echo "📝 Logs:"
echo "   Backend:  docker-compose logs -f backend (if using Docker)"
echo "   Frontend: Check frontend terminal"
echo ""

# Wait for interrupt
wait
