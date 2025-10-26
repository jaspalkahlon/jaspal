"""
API Integration Layer
RESTful API endpoints for the Fashion Guru Bot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Any
import os

from ..core.bot import FashionGuruBot


class FashionGuruAPI:
    """
    Flask-based REST API for the Fashion Guru Bot.
    Provides endpoints for chat, module access, and bot management.
    """

    def __init__(self, bot: FashionGuruBot, config: Dict[str, Any]):
        """
        Initialize the API

        Args:
            bot: FashionGuruBot instance
            config: API configuration
        """
        self.bot = bot
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize Flask app
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for all routes

        # Register routes
        self._register_routes()

    def _register_routes(self):
        """Register all API routes"""

        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'service': 'Fashion Guru Bot',
                'modules': self.bot.list_modules()
            }), 200

        @self.app.route('/chat', methods=['POST'])
        def chat():
            """
            Main chat endpoint

            Expected JSON body:
            {
                "user_id": "unique_user_id",
                "message": "user's message",
                "context": {} (optional)
            }
            """
            try:
                data = request.get_json()

                if not data:
                    return jsonify({'error': 'No JSON body provided'}), 400

                user_id = data.get('user_id')
                message = data.get('message')

                if not user_id or not message:
                    return jsonify({'error': 'user_id and message are required'}), 400

                # Process the query
                response = self.bot.process_query(user_id, message)

                return jsonify({
                    'success': True,
                    'response': response
                }), 200

            except Exception as e:
                self.logger.error(f"Error processing chat request: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/modules', methods=['GET'])
        def list_modules():
            """List all available modules"""
            return jsonify({
                'modules': self.bot.list_modules()
            }), 200

        @self.app.route('/modules/<module_name>', methods=['GET'])
        def module_info(module_name):
            """Get information about a specific module"""
            module = self.bot.get_module(module_name)

            if not module:
                return jsonify({'error': f'Module {module_name} not found'}), 404

            return jsonify({
                'name': module_name,
                'type': type(module).__name__,
                'available': True
            }), 200

        @self.app.route('/context/<user_id>', methods=['GET'])
        def get_context(user_id):
            """Get conversation context for a user"""
            try:
                context = self.bot.conversation_manager.get_or_create_context(user_id)
                return jsonify({
                    'user_id': user_id,
                    'context': context.to_dict()
                }), 200
            except Exception as e:
                self.logger.error(f"Error getting context: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/context/<user_id>', methods=['DELETE'])
        def delete_context(user_id):
            """Delete conversation context for a user"""
            try:
                self.bot.conversation_manager.delete_context(user_id)
                return jsonify({
                    'success': True,
                    'message': f'Context for user {user_id} deleted'
                }), 200
            except Exception as e:
                self.logger.error(f"Error deleting context: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/stats', methods=['GET'])
        def stats():
            """Get bot statistics"""
            return jsonify({
                'active_conversations': self.bot.conversation_manager.get_active_contexts_count(),
                'modules_loaded': len(self.bot.modules)
            }), 200

    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """
        Run the API server

        Args:
            host: Host to bind to
            port: Port to bind to
            debug: Debug mode
        """
        self.logger.info(f"Starting Fashion Guru API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_api(config: Dict[str, Any]) -> FashionGuruAPI:
    """
    Factory function to create API instance

    Args:
        config: Configuration dictionary

    Returns:
        FashionGuruAPI instance
    """
    # Initialize bot
    bot = FashionGuruBot(config)

    # Create and return API
    return FashionGuruAPI(bot, config.get('api', {}))
