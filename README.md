# 🏠 Physical Screen Visualizer

**AI-powered visualization of physical window and door screens for sales and installation planning.**

A modern, full-stack web application that helps sales representatives and homeowners visualize how physical security screens, lifestyle screens, and solar screens will look on their homes. Built with Django REST Framework and React, featuring AI vision integration, JWT authentication, and real-time processing.

## 🎯 What This Application Does

**This application visualizes PHYSICAL WINDOW AND DOOR SCREENS - not digital displays or security cameras.**

### Screen Types We Visualize:
- **Security Screens:** Stainless steel mesh for break-in protection (Boss Security Screens, etc.)
- **Lifestyle Screens:** Decorative screens (Phifer, Twitchell, standard fiberglass)
- **Solar Screens:** UV/heat blocking screens for energy efficiency
- **Pet-Resistant Screens:** Heavy-duty screens for homes with pets

### Primary Use Case:
1. Sales rep visits customer's home
2. Takes photo of house exterior (windows, doors, patios)
3. Uploads photo and selects screen type
4. AI generates realistic visualization showing screens installed
5. Customer sees exactly how their home will look with screens
6. Increased sales conversion and customer confidence

[![CI/CD Pipeline](https://github.com/yourusername/homescreen/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/homescreen/actions)
[![Coverage](https://codecov.io/gh/yourusername/homescreen/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/homescreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🤖 AI-Enhanced Visualization
- **Service-Agnostic Architecture:** Support for multiple AI providers (OpenAI, Google, Anthropic)
- **Intelligent Window Detection:** AI-powered detection of windows and doors in house photos
- **Realistic Screen Application:** Advanced mesh pattern application with lighting effects
- **Quality Assessment:** Automatic quality scoring and enhancement of generated images
- **Multiple Variations:** Generate different screen styles and patterns for comparison
- **Fallback Mechanisms:** Graceful degradation when AI services are unavailable
- **Real-time Monitoring:** Live status monitoring of AI service health and performance

### 🔐 Authentication & Security
- JWT-based authentication with refresh tokens
- Rate limiting and security headers
- User registration and profile management
- Account lockout protection

### 📱 Responsive Design
- Mobile-first responsive design
- Progressive Web App (PWA) capabilities
- Optimized for all screen sizes
- Accessibility compliant (WCAG 2.1 AA)

### 🚀 Performance
- Code splitting and lazy loading
- Virtual scrolling for large datasets
- Optimized image loading with WebP support
- Redis caching and database optimization

### 🧪 Testing & Quality
- Comprehensive unit and integration tests
- End-to-end testing with Cypress
- Code quality tools (ESLint, Prettier, Black)
- Pre-commit hooks and CI/CD pipeline

### 📊 Monitoring & Observability
- Health check endpoints
- Structured logging
- Error tracking with Sentry
- Performance monitoring

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 4.0+ with Django REST Framework
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7+
- **Authentication:** JWT with SimpleJWT
- **Task Queue:** Celery (optional)
- **Server:** Gunicorn with Gevent workers

### Frontend
- **Framework:** React 18+ with Hooks
- **State Management:** Zustand with persistence
- **Styling:** CSS3 with BEM methodology
- **Build Tool:** Create React App with optimizations
- **Testing:** Jest + React Testing Library + Cypress

### DevOps & Infrastructure
- **Containerization:** Docker with multi-stage builds
- **Orchestration:** Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Health checks and logging
- **Security:** Pre-commit hooks and security scanning

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ and npm
- Python 3.11+
- Git

### Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/homescreen.git
cd homescreen
```

2. **Start with Docker (Recommended):**
```bash
# Development environment
docker-compose -f docker-compose.dev.yml up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
```

3. **Manual setup (Alternative):**
```bash
# Backend setup
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend setup (in another terminal)
cd frontend
npm install
npm start
```

### Production Deployment

```bash
# Build and deploy with Docker
docker-compose up --build -d

# Or use the Makefile
make docker-run
```

## 📖 Documentation

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[AI Services Architecture](docs/AI_SERVICES_ARCHITECTURE.md)** - AI services architecture and design
- **[AI Services Developer Guide](docs/AI_SERVICES_DEVELOPER_GUIDE.md)** - Guide for extending AI services
- **[Component Documentation](docs/COMPONENT_DOCUMENTATION.md)** - Frontend component guide
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[Troubleshooting Guide](docs/TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions
- **[Backend Refactoring Guide](BACKEND_REFACTORING_GUIDE.md)** - Backend architecture details
- **[Frontend Refactoring Guide](FRONTEND_REFACTORING_GUIDE.md)** - Frontend architecture details

## 🧪 Testing

### Run All Tests
```bash
make test
```

### Backend Tests
```bash
# Unit tests with coverage
python -m pytest --cov=api --cov-report=html

# Or using make
make test-backend
```

### Frontend Tests
```bash
# Unit tests
cd frontend && npm run test:unit:coverage

# End-to-end tests
cd frontend && npm run test:e2e

# Or using make
make test-frontend
make test-e2e
```

## 🔧 Development

### Code Quality
```bash
# Format code
make format

# Run linting
make lint

# Run all quality checks
make check

# Security scan
make security
```

### Database Management
```bash
# Run migrations
make migrate

# Create superuser
make createsuperuser

# Reset database (development only)
make db-reset
```

### Useful Commands
```bash
# View all available commands
make help

# Start development server
make run

# Build for production
make build

# View logs
make logs
```

## 🏗️ Project Structure

```
homescreen/
├── 📁 api/                     # Django REST API
│   ├── 📁 ai_services/         # AI services framework
│   │   ├── 📁 providers/       # AI service providers
│   │   ├── 📄 interfaces.py    # Service interfaces
│   │   ├── 📄 registry.py      # Service registry
│   │   ├── 📄 factory.py       # Service factory
│   │   └── 📄 config.py        # Configuration manager
│   ├── 📁 migrations/          # Database migrations
│   ├── 📁 tests/               # Backend tests
│   ├── 📄 models.py            # Database models
│   ├── 📄 serializers.py       # API serializers
│   ├── 📄 views.py             # API views
│   ├── 📄 ai_enhanced_processor.py # AI-enhanced image processor
│   └── 📄 urls.py              # API routing
├── 📁 frontend/                # React frontend
│   ├── 📁 public/              # Static assets
│   ├── 📁 src/                 # Source code
│   │   ├── 📁 components/      # React components
│   │   │   ├── 📁 AI/          # AI service components
│   │   │   ├── 📁 Upload/      # Upload components
│   │   │   └── 📁 Results/     # Results components
│   │   ├── 📁 services/        # API services
│   │   ├── 📁 store/           # State management
│   │   ├── 📁 utils/           # Utility functions
│   │   └── 📄 App.js           # Main app component
│   ├── 📁 cypress/             # E2E tests
│   └── 📄 package.json         # NPM dependencies
├── 📁 homescreen_project/      # Django settings
├── 📁 docker/                  # Docker configuration
├── 📁 docs/                    # Documentation
│   ├── 📄 AI_SERVICES_ARCHITECTURE.md # AI services architecture
│   ├── 📄 AI_SERVICES_DEVELOPER_GUIDE.md # AI services development guide
│   └── 📄 API_DOCUMENTATION.md        # API reference
├── 📁 .github/                 # GitHub Actions
├── 📄 docker-compose.yml       # Production compose
├── 📄 docker-compose.dev.yml   # Development compose
├── 📄 Dockerfile               # Docker image
├── 📄 Makefile                 # Development commands
├── 📄 requirements.txt         # Python dependencies
└── 📄 requirements-dev.txt     # Development dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style and conventions
- Write tests for new features
- Update documentation as needed
- Run quality checks before submitting PRs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** Check the [docs/](docs/) directory
- **Issues:** Report bugs and request features via [GitHub Issues](https://github.com/yourusername/homescreen/issues)
- **Discussions:** Join the conversation in [GitHub Discussions](https://github.com/yourusername/homescreen/discussions)

## 🙏 Acknowledgments

- Django and React communities for excellent frameworks
- All contributors who helped improve this project
- Open source libraries that made this project possible

---

**Made with ❤️ by the Homescreen Visualizer Team**
