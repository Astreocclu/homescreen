"""
AI Service Providers Package

This package contains implementations of AI service providers that can be
used with the homescreen visualization system. Each provider implements
the standard interfaces defined in the parent package.

Available Providers:
- MockProvider: For testing and development
- OpenAIProvider: OpenAI GPT-4 Vision and DALL-E integration
- GoogleProvider: Google Cloud Vision API integration
- AnthropicProvider: Anthropic Claude Vision integration
"""

from .mock_provider import MockAIProvider
from .base_provider import BaseAIProvider
from .openai_provider import OpenAIProvider

__all__ = [
    'MockAIProvider',
    'BaseAIProvider',
    'OpenAIProvider'
]
