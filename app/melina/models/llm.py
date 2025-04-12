from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain.schema.language_model import BaseLanguageModel
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class LLMType(str, Enum):
    """Types of supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MISTRAL = "mistral"
    LLAMA = "llama"
    GEMINI = "gemini"
    GROQ = "groq"
    OTHER = "other"

class LLMConfig(BaseModel):
    """Configuration for an LLM."""
    provider: LLMType
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    api_key: Optional[str] = None
    
    def create_model(self) -> BaseLanguageModel:
        """Create the appropriate LLM instance based on configuration."""
        if self.provider == LLMType.OPENAI:
            return ChatOpenAI(
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                api_key=self.api_key
            )
        elif self.provider == LLMType.ANTHROPIC:
            return ChatAnthropic(
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key
            )
        elif self.provider == LLMType.MISTRAL:
            return ChatMistralAI(
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key
            )
        elif self.provider == LLMType.LLAMA:
            return ChatOllama(
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key
            )
        elif self.provider == LLMType.GEMINI:
            return ChatGoogleGenerativeAI(
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key
            )
        elif self.provider == LLMType.GROQ:
            return ChatGroq(
                model_name=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key
            )
        # Add other providers as needed
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
