# 🤝 Contributing to AirBreaker

First off, thank you for considering contributing! 🎉

## Code of Conduct
This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### 🐛 Reporting Bugs
- Check if the bug already exists in Issues
- Use the Bug Report template
- Include: OS, Python version, network card model, logs

### 💡 Suggesting Enhancements
- Check if the feature is already in the Roadmap
- Open a Feature Request issue
- Describe the use case and expected behavior

### 🔧 Pull Requests
1. Fork the repo
2. Create a new branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest`
5. Commit with clear message: `git commit -m "feat: add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📦 Development Setup

```bash
# Clone
git clone https://github.com/stanislavzxc/AirBreaker.git
cd AirBreaker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing

# Run
python main.py