"""
OpenAgents - A Scalable Open-Source AI Agents Framework

OpenAgents is a lightweight, modular framework for building AI agents with tool-calling capabilities
using open-source language models like those available through Ollama.

Features:
- Modular architecture for easy extension
- Tool calling system with automatic function registration
- Support for Ollama models (local open-source LLMs)
- Clean, maintainable codebase with clear file separation
- Extensible for multi-agent systems

This package requires Python 3.7+ and the following dependencies:
- requests
- (optional) psutil for memory monitoring

For examples, see the examples/ directory.
"""

from setuptools import setup, find_packages

setup(
    name="openagents",
    version="0.1.0",
    description="A scalable open-source AI agents framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Hanish Dhanwalkar",
    author_email="hanishdhanwalkar.iitb@gmail.com",
    url="https://github.com/yourusername/openagents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.8.0",
            "flake8>=3.9.2",
            "mypy>=0.812",
        ],
        "monitor": [
            "psutil>=5.8.0",
        ],
    },
)
