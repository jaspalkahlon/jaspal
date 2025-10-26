"""
Webhook Integration
Support for popular messaging platforms and webhooks
"""

import logging
from typing import Dict, Any, Callable
import hmac
import hashlib


class WebhookHandler:
    """
    Handles webhooks from various messaging platforms.
    Supports Slack, Discord, Telegram, and custom webhooks.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize webhook handler

        Args:
            config: Webhook configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.handlers: Dict[str, Callable] = {}

    def register_handler(self, platform: str, handler: Callable):
        """
        Register a handler for a specific platform

        Args:
            platform: Platform name (slack, discord, telegram, etc.)
            handler: Handler function
        """
        self.handlers[platform] = handler
        self.logger.info(f"Registered handler for platform: {platform}")

    def handle_slack(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Slack webhook

        Args:
            payload: Slack webhook payload

        Returns:
            Response for Slack
        """
        # Handle Slack challenge
        if 'challenge' in payload:
            return {'challenge': payload['challenge']}

        # Extract message
        event = payload.get('event', {})
        user_id = event.get('user')
        text = event.get('text')
        channel = event.get('channel')

        if not user_id or not text:
            return {'error': 'Invalid Slack payload'}

        return {
            'user_id': user_id,
            'message': text,
            'channel': channel,
            'platform': 'slack'
        }

    def handle_discord(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Discord webhook

        Args:
            payload: Discord webhook payload

        Returns:
            Response for Discord
        """
        user_id = payload.get('author', {}).get('id')
        text = payload.get('content')
        channel = payload.get('channel_id')

        if not user_id or not text:
            return {'error': 'Invalid Discord payload'}

        return {
            'user_id': user_id,
            'message': text,
            'channel': channel,
            'platform': 'discord'
        }

    def handle_telegram(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Telegram webhook

        Args:
            payload: Telegram webhook payload

        Returns:
            Response for Telegram
        """
        message = payload.get('message', {})
        user_id = message.get('from', {}).get('id')
        text = message.get('text')
        chat_id = message.get('chat', {}).get('id')

        if not user_id or not text:
            return {'error': 'Invalid Telegram payload'}

        return {
            'user_id': str(user_id),
            'message': text,
            'channel': str(chat_id),
            'platform': 'telegram'
        }

    def verify_signature(self, payload: bytes, signature: str, secret: str, algorithm: str = 'sha256') -> bool:
        """
        Verify webhook signature

        Args:
            payload: Raw payload bytes
            signature: Signature from webhook
            secret: Webhook secret
            algorithm: Hash algorithm (default: sha256)

        Returns:
            True if signature is valid
        """
        if algorithm == 'sha256':
            expected_signature = hmac.new(
                secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        return hmac.compare_digest(signature, expected_signature)

    def process_webhook(self, platform: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process webhook from any platform

        Args:
            platform: Platform name
            payload: Webhook payload

        Returns:
            Processed message data
        """
        handler = self.handlers.get(platform)

        if not handler:
            # Try default handlers
            if platform == 'slack':
                return self.handle_slack(payload)
            elif platform == 'discord':
                return self.handle_discord(payload)
            elif platform == 'telegram':
                return self.handle_telegram(payload)
            else:
                self.logger.error(f"No handler found for platform: {platform}")
                return {'error': f'Unsupported platform: {platform}'}

        return handler(payload)


# Example webhook integration with Flask
def create_webhook_routes(app, bot, webhook_handler: WebhookHandler):
    """
    Add webhook routes to Flask app

    Args:
        app: Flask app instance
        bot: FashionGuruBot instance
        webhook_handler: WebhookHandler instance
    """

    @app.route('/webhook/<platform>', methods=['POST'])
    def webhook(platform):
        """Generic webhook endpoint"""
        from flask import request, jsonify

        try:
            payload = request.get_json()

            # Process webhook
            processed = webhook_handler.process_webhook(platform, payload)

            if 'error' in processed:
                return jsonify(processed), 400

            # Extract message data
            user_id = processed.get('user_id')
            message = processed.get('message')

            # Process with bot
            response = bot.process_query(user_id, message)

            # Format response for platform
            return jsonify({
                'success': True,
                'response': response['message'],
                'platform': platform
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    return app
