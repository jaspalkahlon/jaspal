"""
Fashion Guru Bot - Core Bot Engine
The main orchestrator for the digital atelier assistant
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from .context import ConversationContext
from .conversation import ConversationManager


class FashionGuruBot:
    """
    Main bot class that orchestrates all modules and manages the conversation flow.
    Implements the guru-shishya parampara approach for fashion education.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Fashion Guru Bot

        Args:
            config: Configuration dictionary containing bot settings and module configs
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.conversation_manager = ConversationManager()
        self.modules = {}
        self._load_modules()

        self.logger.info("Fashion Guru Bot initialized successfully")

    def _load_modules(self):
        """Dynamically load all pillar modules"""
        from ..modules.pillar1.pattern_intelligence import PatternIntelligence
        from ..modules.pillar1.fabric_oracle import FabricOracle
        from ..modules.pillar1.troubleshooting import TroubleshootingCompanion
        from ..modules.pillar2.trend_synthesis import TrendSynthesisEngine
        from ..modules.pillar2.color_psychology import ColorPsychologyTool
        from ..modules.pillar2.design_critique import DesignCritiqueSystem

        # Load Pillar 1: Technical Mastery
        self.modules['pattern_intelligence'] = PatternIntelligence(
            self.config.get('pillar1', {}).get('pattern_intelligence', {})
        )
        self.modules['fabric_oracle'] = FabricOracle(
            self.config.get('pillar1', {}).get('fabric_oracle', {})
        )
        self.modules['troubleshooting'] = TroubleshootingCompanion(
            self.config.get('pillar1', {}).get('troubleshooting', {})
        )

        # Load Pillar 2: Creative Evolution
        self.modules['trend_synthesis'] = TrendSynthesisEngine(
            self.config.get('pillar2', {}).get('trend_synthesis', {})
        )
        self.modules['color_psychology'] = ColorPsychologyTool(
            self.config.get('pillar2', {}).get('color_psychology', {})
        )
        self.modules['design_critique'] = DesignCritiqueSystem(
            self.config.get('pillar2', {}).get('design_critique', {})
        )

        self.logger.info(f"Loaded {len(self.modules)} modules")

    def process_query(self, user_id: str, query: str, context: Optional[ConversationContext] = None) -> Dict[str, Any]:
        """
        Process a user query and route to appropriate modules

        Args:
            user_id: Unique identifier for the user
            query: User's question or request
            context: Optional conversation context for continuity

        Returns:
            Dictionary containing response and metadata
        """
        self.logger.info(f"Processing query from user {user_id}: {query[:50]}...")

        # Get or create conversation context
        if context is None:
            context = self.conversation_manager.get_or_create_context(user_id)

        # Update context with new query
        context.add_message("user", query)

        # Classify intent and route to appropriate module(s)
        intent = self._classify_intent(query, context)

        # Process through relevant modules
        response = self._process_with_modules(query, intent, context)

        # Add response to context
        context.add_message("assistant", response['message'])

        # Update context
        self.conversation_manager.update_context(user_id, context)

        return response

    def _classify_intent(self, query: str, context: ConversationContext) -> Dict[str, Any]:
        """
        Classify user intent to route to appropriate modules

        Args:
            query: User's question
            context: Conversation context

        Returns:
            Dictionary with intent classification and confidence
        """
        query_lower = query.lower()

        # Technical Mastery intents
        if any(keyword in query_lower for keyword in ['pattern', 'draft', 'measurement', 'construction', 'sew']):
            return {
                'primary_pillar': 'pillar1',
                'module': 'pattern_intelligence',
                'confidence': 0.9,
                'type': 'technical'
            }

        if any(keyword in query_lower for keyword in ['fabric', 'material', 'textile', 'drape', 'weight']):
            return {
                'primary_pillar': 'pillar1',
                'module': 'fabric_oracle',
                'confidence': 0.9,
                'type': 'technical'
            }

        if any(keyword in query_lower for keyword in ['problem', 'issue', 'fix', 'wrong', 'help', 'fit']):
            return {
                'primary_pillar': 'pillar1',
                'module': 'troubleshooting',
                'confidence': 0.85,
                'type': 'technical'
            }

        # Creative Evolution intents
        if any(keyword in query_lower for keyword in ['trend', 'fashion week', 'runway', 'street style', 'forecast']):
            return {
                'primary_pillar': 'pillar2',
                'module': 'trend_synthesis',
                'confidence': 0.9,
                'type': 'creative'
            }

        if any(keyword in query_lower for keyword in ['color', 'palette', 'hue', 'shade', 'combination']):
            return {
                'primary_pillar': 'pillar2',
                'module': 'color_psychology',
                'confidence': 0.9,
                'type': 'creative'
            }

        if any(keyword in query_lower for keyword in ['design', 'critique', 'feedback', 'improve', 'concept']):
            return {
                'primary_pillar': 'pillar2',
                'module': 'design_critique',
                'confidence': 0.85,
                'type': 'creative'
            }

        # Default to general assistance
        return {
            'primary_pillar': 'general',
            'module': 'pattern_intelligence',  # Default module
            'confidence': 0.5,
            'type': 'general'
        }

    def _process_with_modules(self, query: str, intent: Dict[str, Any], context: ConversationContext) -> Dict[str, Any]:
        """
        Process query through relevant modules

        Args:
            query: User's question
            intent: Classified intent
            context: Conversation context

        Returns:
            Response dictionary
        """
        module_name = intent.get('module')
        module = self.modules.get(module_name)

        if not module:
            return {
                'message': "I'm here to help with fashion design! Please ask about patterns, fabrics, trends, or design feedback.",
                'intent': intent,
                'timestamp': datetime.now().isoformat()
            }

        # Process through the module
        response = module.process(query, context)

        return {
            'message': response,
            'intent': intent,
            'module': module_name,
            'timestamp': datetime.now().isoformat(),
            'context_length': len(context.messages)
        }

    def get_module(self, module_name: str):
        """Get a specific module by name"""
        return self.modules.get(module_name)

    def list_modules(self) -> List[str]:
        """List all available modules"""
        return list(self.modules.keys())
