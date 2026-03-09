# Contributing to AI Data Analyst Agent

First off, thanks for considering contributing to AI Data Analyst Agent! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

**Bugs are tracked as GitHub Issues**. Provide the following information:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**
- **Include your OS and Python version**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub Issues. When creating an enhancement suggestion, provide:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Development Setup

1. **Fork the repository**

   ```bash
   git clone https://github.com/yourusername/ai-data-analyst-agent.git
   cd ai-data-analyst-agent
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**

   ```bash
   pip install -e ".[dev]"
   # Or using requirements files:
   pip install -r requirements.txt -r requirements-dev.txt
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Style

We follow PEP 8 with some modifications:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces
- **Use type hints** where possible
- **Use docstrings** for all functions and classes

Format your code with Black:

```bash
black src/ tests/ --line-length 100
```

Lint your code with Flake8:

```bash
flake8 src/ tests/ --max-line-length 100
```

### Testing

Write tests for all new features:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_specific.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

Test file naming convention: `test_*.py` or `*_test.py`

### Documentation

- Update README.md if adding features
- Add docstrings to all functions and classes
- Update PHASE\*.md files if architecture changes
- Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of function.

    Longer description if needed. Can span multiple lines.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is wrong

    Example:
        >>> example_function('test', 42)
        True
    """
    pass
```

## Commit Messages

Use clear and descriptive commit messages:

- Use the imperative mood ("Add feature" not "Added feature")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:

```
Add histogram visualization with KDE overlay

- Includes statistics box (mean, std, skew)
- Color-coded with GREEN (#2ecc71)
- UTF-8 safe for Windows compatibility

Fixes #42
```

## File Structure Guidelines

When adding new modules:

```
src/
├── module_name/
│   ├── __init__.py        # Add exports here
│   ├── main_file.py       # Main implementation
│   └── types.py           # Type definitions if needed
```

## Performance Guidelines

- Profile code before optimizations
- Ensure visualizations complete in <30 seconds for typical datasets
- Keep insight generation deterministic (no randomness)
- Test with datasets of various sizes (100 to 1M+ rows)

## Adding New Insight Types

1. Define in `src/insights/insight_types.py`
2. Add extraction method to `src/insights/insight_engine.py`
3. Add templates to `src/reporting/report_writer.py`
4. Write tests in `tests/test_insights.py`
5. Update documentation

## Versioning

We follow Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Update version in:

- `pyproject.toml`
- `setup.py`

## Additional Notes

### Issue and Pull Request Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

### Project Board

Check the [Project Board](https://github.com/yourusername/ai-data-analyst-agent/projects) for current priorities.

## Recognition

Contributors will be recognized in:

- README.md Contributors section
- Release notes
- Project documentation

---

Thank you for contributing! 🎉
