"""
Conversation Manager
Handles conversation flow, context persistence, and session management
"""

import logging
from typing import Dict, Optional
from .context import ConversationContext


class ConversationManager:
    """
    Manages multiple conversation contexts and handles persistence.
    Enables the bot to maintain relationships with multiple students.
    """

    def __init__(self):
        """Initialize the conversation manager"""
        self.logger = logging.getLogger(__name__)
        self.contexts: Dict[str, ConversationContext] = {}
        self.logger.info("ConversationManager initialized")

    def get_or_create_context(self, user_id: str) -> ConversationContext:
        """
        Get existing context or create a new one for a user

        Args:
            user_id: Unique identifier for the user

        Returns:
            ConversationContext for the user
        """
        if user_id not in self.contexts:
            self.logger.info(f"Creating new context for user {user_id}")
            self.contexts[user_id] = ConversationContext(user_id)

        return self.contexts[user_id]

    def update_context(self, user_id: str, context: ConversationContext):
        """
        Update the context for a user

        Args:
            user_id: Unique identifier for the user
            context: Updated conversation context
        """
        self.contexts[user_id] = context
        self.logger.debug(f"Updated context for user {user_id}")

    def delete_context(self, user_id: str):
        """
        Delete a user's conversation context

        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.contexts:
            del self.contexts[user_id]
            self.logger.info(f"Deleted context for user {user_id}")

    def get_active_contexts_count(self) -> int:
        """Get the number of active conversation contexts"""
        return len(self.contexts)

    def clear_all_contexts(self):
        """Clear all conversation contexts (use with caution)"""
        count = len(self.contexts)
        self.contexts = {}
        self.logger.warning(f"Cleared {count} conversation contexts")
