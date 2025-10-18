"""Windows Use Agent integration module."""

import os
import time
from datetime import datetime
from typing import Dict, Optional, Any
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Import the Windows Use Agent
try:
    from windows_use.agent import Agent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    print("[AgentManager] windows_use.agent not found. Agent features will be disabled.")

load_dotenv()


class AgentManager:
    """Manages the Windows Use Agent and its integrations."""
    
    def __init__(self):
        self.agent: Optional[Any] = None
        self.agent_ready = False
        self.agent_error: Optional[str] = None
        self.advanced_features = False
        
        # Advanced modules (optional)
        self.workflow_engine = None
        self.context_manager = None
        self.security_manager = None
        self.integration_manager = None
        
        # Initialize the agent
        self._initialize_agent()
    
    def _initialize_agent(self) -> None:
        """Initialize the Windows Use Agent with LLM."""
        if not AGENT_AVAILABLE:
            self.agent_error = "windows_use.agent package not installed"
            self.agent_ready = False
            return
        
        try:
            # Initialize LLM (Gemini)
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
            
            # Build instructions
            instructions = [
                (
                    "Claude Desktop, Perplexity, and ChatGPT apps are installed. "
                    "Collaborate with them for advanced reasoning when required."
                )
            ]
            
            # Add location instruction if available
            location_instruction = self._build_location_instruction()
            if location_instruction:
                instructions.append(location_instruction)
            
            # Create agent
            self.agent = Agent(instructions=instructions, llm=llm, use_vision=True)
            self.agent_ready = True
            print("[AgentManager] Agent initialized successfully")
            
        except Exception as error:
            self.agent_error = str(error)
            self.agent_ready = False
            print(f"[AgentManager] Agent init failed: {error}")
            return
        
        # Try to load advanced features
        self._load_advanced_features()
    
    def _build_location_instruction(self) -> Optional[str]:
        """Build location context instruction from environment."""
        profile = self._get_user_profile()
        
        if not any(profile.values()):
            return None
        
        parts = []
        if profile.get("city"):
            parts.append(f"City: {profile['city']}")
        if profile.get("region"):
            parts.append(f"Region: {profile['region']}")
        if profile.get("country"):
            parts.append(f"Country: {profile['country']}")
        if profile.get("timezone"):
            parts.append(f"Timezone: {profile['timezone']}")
        
        if parts:
            location_str = ", ".join(parts)
            return f"User location: {location_str}. Use this for local searches, weather, time-aware tasks."
        
        return None
    
    def _get_user_profile(self) -> Dict[str, Optional[str]]:
        """Get user profile from environment variables."""
        return {
            "city": os.getenv("WINDOWS_USE_CITY") or os.getenv("USER_CITY"),
            "region": os.getenv("WINDOWS_USE_REGION") or os.getenv("USER_REGION"),
            "country": os.getenv("WINDOWS_USE_COUNTRY") or os.getenv("USER_COUNTRY"),
            "timezone": os.getenv("WINDOWS_USE_TIMEZONE"),
            "latitude": os.getenv("WINDOWS_USE_LAT") or os.getenv("USER_LATITUDE"),
            "longitude": os.getenv("WINDOWS_USE_LON") or os.getenv("USER_LONGITUDE"),
        }
    
    def _load_advanced_features(self) -> None:
        """Try to load advanced enterprise features."""
        try:
            from windows_use.agent.context_manager.context_manager import ContextManager
            from windows_use.agent.integrations.integration_manager import IntegrationManager
            from windows_use.agent.security.security_manager import SecurityManager
            from windows_use.agent.workflow_engine.smart_workflow_engine import SmartWorkflowEngine
            
            self.workflow_engine = SmartWorkflowEngine()
            self.context_manager = ContextManager()
            self.security_manager = SecurityManager()
            self.integration_manager = IntegrationManager()
            self.advanced_features = True
            print("[AgentManager] Advanced features loaded successfully")
            
        except ImportError as error:
            self.advanced_features = False
            print(f"[AgentManager] Advanced modules unavailable: {error}")
    
    def execute_command(self, command: str, mode: str = "Basic") -> Dict[str, Any]:
        """Execute a command using the agent.
        
        Args:
            command: The natural language command to execute
            mode: The execution mode (Basic, Advanced, Expert)
        
        Returns:
            Dictionary with status, message, duration, and response
        """
        start_time = time.perf_counter()
        
        # Check if agent is ready
        if not self.agent_ready:
            return {
                "status": "error",
                "message": "Agent not configured. Check API keys and network.",
                "duration": "0s",
                "response": self.agent_error or "Agent initialization failed"
            }
        
        try:
            # Execute the command
            result = self.agent.invoke(query=command)
            duration = f"{time.perf_counter() - start_time:.2f}s"
            
            # Extract response
            response = getattr(result, "content", str(result))
            
            # Create summary (first line, max 90 chars)
            summary = (response.strip().splitlines() or ["Command completed."])[0][:90]
            
            return {
                "status": "success",
                "message": f"✅ {summary}",
                "duration": duration,
                "response": response,
                "mode": mode
            }
            
        except Exception as error:
            duration = f"{time.perf_counter() - start_time:.2f}s"
            return {
                "status": "error",
                "message": f"❌ Command failed: {str(error)}",
                "duration": duration,
                "response": str(error),
                "mode": mode
            }
    
    def is_ready(self) -> bool:
        """Check if the agent is ready."""
        return self.agent_ready
    
    def get_error(self) -> Optional[str]:
        """Get the last agent error."""
        return self.agent_error
    
    def has_advanced_features(self) -> bool:
        """Check if advanced features are available."""
        return self.advanced_features
