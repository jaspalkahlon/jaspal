"""
Conversation Context Management
Maintains state and history for meaningful, continuous conversations
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Message:
    """Represents a single message in the conversation"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationContext:
    """
    Manages conversation state and history for contextual responses.
    Implements memory to maintain the guru-shishya learning relationship.
    """

    def __init__(self, user_id: str, max_history: int = 50):
        """
        Initialize conversation context

        Args:
            user_id: Unique identifier for the user
            max_history: Maximum number of messages to keep in history
        """
        self.user_id = user_id
        self.max_history = max_history
        self.messages: List[Message] = []
        self.user_profile: Dict[str, Any] = {
            'skill_level': 'beginner',  # beginner, intermediate, advanced
            'interests': [],
            'learning_path': [],
            'projects': []
        }
        self.session_data: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.last_updated = datetime.now()

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add a message to the conversation history

        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata about the message
        """
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.last_updated = datetime.now()

        # Trim history if needed
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def get_recent_messages(self, n: int = 10) -> List[Message]:
        """Get the n most recent messages"""
        return self.messages[-n:]

    def get_conversation_summary(self) -> str:
        """Generate a summary of the conversation"""
        if not self.messages:
            return "No conversation history yet."

        recent = self.get_recent_messages(5)
        summary_parts = []

        for msg in recent:
            prefix = "User" if msg.role == "user" else "Guru"
            content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary_parts.append(f"{prefix}: {content_preview}")

        return "\n".join(summary_parts)

    def update_user_profile(self, key: str, value: Any):
        """Update user profile information"""
        self.user_profile[key] = value
        self.last_updated = datetime.now()

    def get_user_skill_level(self) -> str:
        """Get the user's current skill level"""
        return self.user_profile.get('skill_level', 'beginner')

    def set_session_data(self, key: str, value: Any):
        """Set session-specific data"""
        self.session_data[key] = value

    def get_session_data(self, key: str, default: Any = None) -> Any:
        """Get session-specific data"""
        return self.session_data.get(key, default)

    def clear_session_data(self):
        """Clear all session data"""
        self.session_data = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization"""
        return {
            'user_id': self.user_id,
            'messages': [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'metadata': msg.metadata
                }
                for msg in self.messages
            ],
            'user_profile': self.user_profile,
            'session_data': self.session_data,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationContext':
        """Create context from dictionary"""
        context = cls(data['user_id'])
        context.user_profile = data.get('user_profile', {})
        context.session_data = data.get('session_data', {})
        context.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        context.last_updated = datetime.fromisoformat(data.get('last_updated', datetime.now().isoformat()))

        for msg_data in data.get('messages', []):
            context.add_message(
                msg_data['role'],
                msg_data['content'],
                msg_data.get('metadata', {})
            )

        return context
