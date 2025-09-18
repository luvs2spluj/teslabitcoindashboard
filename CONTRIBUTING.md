# Contributing to Financial App

Thank you for your interest in contributing to the Financial App! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- pnpm
- Git

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/financial-app.git
   cd financial-app
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

3. **Start development environment**
   ```bash
   make dev
   ```

4. **Initialize database**
   ```bash
   make migrate
   make seed
   ```

5. **Run tests**
   ```bash
   make test
   ```

## Development Workflow

### Code Style
- **Python**: Use Black for formatting, Ruff for linting, MyPy for type checking
- **TypeScript**: Use Prettier for formatting, ESLint for linting
- **Commits**: Use conventional commit messages

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Add integration tests for API endpoints
- Test both success and error scenarios

### Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

### Code Review Guidelines

- **Functionality**: Does the code work as intended?
- **Testing**: Are there adequate tests?
- **Documentation**: Is the code well-documented?
- **Performance**: Are there any performance concerns?
- **Security**: Are there any security vulnerabilities?

## Project Structure

```
/apps
  /web        # Next.js frontend
  /api        # FastAPI backend
/packages
  /shared     # Shared utilities
/infra
  /db         # Database migrations
  /docker     # Docker configuration
  /ci         # CI/CD workflows
/docs         # Documentation
```

## API Development

### Adding New Endpoints
1. Create route in `apps/api/app/api/`
2. Add Pydantic models for request/response
3. Implement business logic
4. Add tests
5. Update OpenAPI documentation

### Data Sources
1. Implement `DataSource` interface
2. Add error handling and rate limiting
3. Include validation
4. Add tests
5. Document usage

## Frontend Development

### Adding New Pages
1. Create page in `apps/web/app/`
2. Add components in `apps/web/components/`
3. Implement responsive design
4. Add TypeScript types
5. Test across browsers

### Components
- Use shadcn/ui for base components
- Follow Tailwind CSS patterns
- Implement dark mode support
- Ensure accessibility compliance

## Database Changes

### Migrations
1. Create migration with Alembic
2. Test migration on sample data
3. Include rollback procedure
4. Update documentation

### Models
- Use SQLAlchemy models
- Add proper relationships
- Include validation
- Document schema changes

## Security Considerations

- Never commit API keys or secrets
- Validate all inputs
- Use parameterized queries
- Implement rate limiting
- Follow OWASP guidelines

## Performance Guidelines

- Use Redis caching where appropriate
- Optimize database queries
- Implement pagination for large datasets
- Use CDN for static assets
- Monitor performance metrics

## Documentation

- Update README for new features
- Document API endpoints
- Include code examples
- Maintain architecture diagrams
- Keep setup instructions current

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Deploy to staging
6. Create release tag
7. Deploy to production

## Getting Help

- Check existing issues and discussions
- Join our Discord community
- Read the documentation
- Ask questions in GitHub Discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

