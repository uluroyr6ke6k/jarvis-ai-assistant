"""
J.A.R.V.I.S. AI Engine
Handles AI/LLM interactions for command processing and responses
"""

import requests
import json
from typing import Optional, Dict, List
from config import (
    AI_ENGINE, OLLAMA_MODEL, OLLAMA_BASE_URL,
    MAX_CONTEXT_LENGTH, OPENAI_API_KEY, ANTHROPIC_API_KEY
)
from core.logger import log_info, log_error, log_debug

class AIEngine:
    """Handles AI interactions"""
    
    def __init__(self):
        """Initialize AI engine"""
        self.engine_type = AI_ENGINE
        self.conversation_history = []
        self.context_length = MAX_CONTEXT_LENGTH
        
        if self.engine_type == "ollama":
            self.base_url = OLLAMA_BASE_URL
            self.model = OLLAMA_MODEL
        
        log_info(f"AI Engine initialized: {self.engine_type}")
    
    def process_command(self, command: str) -> str:
        """
        Process user command and get AI response
        
        Args:
            command: User command/query
        
        Returns:
            str: AI response
        """
        try:
            log_debug(f"Processing command: {command}")
            
            # Add to history
            self.conversation_history.append({
                "role": "user",
                "content": command
            })
            
            # Get response based on engine type
            if self.engine_type == "ollama":
                response = self._ollama_request(command)
            elif self.engine_type == "openai":
                response = self._openai_request(command)
            elif self.engine_type == "anthropic":
                response = self._anthropic_request(command)
            else:
                response = "I'm not configured with a valid AI engine."
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Trim history if too long
            self._trim_history()
            
            return response
            
        except Exception as e:
            log_error(f"Error processing command: {e}", e)
            return "I encountered an error processing your request."
    
    def _ollama_request(self, command: str) -> str:
        """
        Send request to Ollama local LLM
        
        Args:
            command: User command
        
        Returns:
            str: Response from Ollama
        """
        try:
            url = f"{self.base_url}/api/generate"
            
            prompt = self._build_prompt(command)
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "No response received").strip()
            
        except requests.exceptions.ConnectionError:
            log_error("Cannot connect to Ollama. Make sure it's running on localhost:11434")
            return "I cannot connect to my AI engine. Please ensure Ollama is running."
        except Exception as e:
            log_error(f"Ollama request error: {e}", e)
            return "I encountered an error with my AI engine."
    
    def _openai_request(self, command: str) -> str:
        """
        Send request to OpenAI API
        
        Args:
            command: User command
        
        Returns:
            str: Response from OpenAI
        """
        if not OPENAI_API_KEY:
            log_error("OpenAI API key not configured")
            return "OpenAI API key is not configured."
        
        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history + [{"role": "user", "content": command}],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            log_error(f"OpenAI request error: {e}", e)
            return "I encountered an error with OpenAI."
    
    def _anthropic_request(self, command: str) -> str:
        """
        Send request to Anthropic Claude API
        
        Args:
            command: User command
        
        Returns:
            str: Response from Claude
        """
        if not ANTHROPIC_API_KEY:
            log_error("Anthropic API key not configured")
            return "Anthropic API key is not configured."
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=self.conversation_history + [{"role": "user", "content": command}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            log_error(f"Anthropic request error: {e}", e)
            return "I encountered an error with Anthropic."
    
    def _build_prompt(self, command: str) -> str:
        """
        Build prompt with system context
        
        Args:
            command: User command
        
        Returns:
            str: Full prompt with context
        """
        system_prompt = """You are J.A.R.V.I.S., a personal AI assistant. 
You are helpful, friendly, and professional.
You can help with:
- PC control and automation
- YouTube channel management
- Image and video generation
- 3D modeling
- General questions and tasks
- Scheduling and reminders

Keep responses concise and actionable."""
        
        # Build context from history
        context = system_prompt
        for msg in self.conversation_history[-4:]:  # Last 4 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"\n{role}: {msg['content']}"
        
        context += f"\nUser: {command}\nAssistant:"
        return context
    
    def _trim_history(self, max_messages: int = 10):
        """
        Trim conversation history to prevent exceeding context length
        
        Args:
            max_messages: Maximum messages to keep
        """
        if len(self.conversation_history) > max_messages:
            self.conversation_history = self.conversation_history[-max_messages:]
            log_debug(f"Trimmed history to {max_messages} messages")
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        log_info("Conversation history cleared")
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history.copy()

# Global AI engine instance
ai_engine = None

def get_ai_engine():
    """Get or create AI engine instance"""
    global ai_engine
    if ai_engine is None:
        ai_engine = AIEngine()
    return ai_engine
