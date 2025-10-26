"""
Fashion Guru Bot - Main Entry Point
Your Digital Atelier Assistant
"""

import os
import sys
import logging
import yaml
from typing import Dict, Any

from bot.core import FashionGuruBot
from bot.integrations.api import create_api


def setup_logging(log_level: str = 'INFO'):
    """
    Setup logging configuration

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('fashion_guru_bot.log')
        ]
    )


def load_config(config_path: str = 'config/config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to config file

    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logging.warning(f"Config file not found at {config_path}, using defaults")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration

    Returns:
        Default configuration dictionary
    """
    return {
        'bot': {
            'name': 'Fashion Guru Bot',
            'version': '1.0.0',
            'description': 'Your Digital Atelier Assistant'
        },
        'pillar1': {
            'pattern_intelligence': {},
            'fabric_oracle': {},
            'troubleshooting': {}
        },
        'pillar2': {
            'trend_synthesis': {},
            'color_psychology': {},
            'design_critique': {}
        },
        'api': {
            'host': '0.0.0.0',
            'port': 5000,
            'debug': False
        },
        'logging': {
            'level': 'INFO'
        }
    }


def run_cli_mode(bot: FashionGuruBot):
    """
    Run bot in CLI mode for testing

    Args:
        bot: FashionGuruBot instance
    """
    print("\n" + "="*60)
    print("  FASHION GURU BOT - Your Digital Atelier Assistant")
    print("="*60)
    print("\nWelcome! I'm here to help with all your fashion design needs.")
    print("Ask me about patterns, fabrics, troubleshooting, trends, colors, or design critique.")
    print("\nType 'exit' or 'quit' to end the session.\n")

    user_id = "cli_user"

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nGuru: Thank you for learning with me today. Keep creating!\n")
                break

            # Process query
            response = bot.process_query(user_id, user_input)

            print(f"\nGuru: {response['message']}\n")

        except KeyboardInterrupt:
            print("\n\nGuru: Session interrupted. Keep creating!\n")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            logging.error(f"Error in CLI mode: {str(e)}")


def create_app():
    """
    Create Flask app instance (for production deployment with gunicorn)

    Returns:
        Flask app instance
    """
    # Load config
    config = load_config('config/config.yaml')

    # Setup logging
    log_level = config.get('logging', {}).get('level', 'INFO')
    setup_logging(log_level)

    # Create and return API
    api = create_api(config)
    return api.app


def run_api_mode(config: Dict[str, Any]):
    """
    Run bot in API mode

    Args:
        config: Configuration dictionary
    """
    api = create_api(config)

    api_config = config.get('api', {})
    host = api_config.get('host', '0.0.0.0')
    port = api_config.get('port', 5000)
    debug = api_config.get('debug', False)

    print("\n" + "="*60)
    print("  FASHION GURU BOT API - Starting Server")
    print("="*60)
    print(f"\nServer running at http://{host}:{port}")
    print("\nAvailable endpoints:")
    print("  GET  /health           - Health check")
    print("  POST /chat             - Chat with bot")
    print("  GET  /modules          - List modules")
    print("  GET  /modules/<name>   - Module info")
    print("  GET  /context/<user>   - Get user context")
    print("  DELETE /context/<user> - Delete user context")
    print("  GET  /stats            - Bot statistics")
    print("\nPress Ctrl+C to stop the server\n")

    api.run(host=host, port=port, debug=debug)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Fashion Guru Bot - Your Digital Atelier Assistant')
    parser.add_argument('--mode', choices=['cli', 'api'], default='cli',
                        help='Run mode: cli for command line, api for REST API server')
    parser.add_argument('--config', default='config/config.yaml',
                        help='Path to configuration file')
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Logging level')

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)

    # Load configuration
    config = load_config(args.config)

    if args.mode == 'cli':
        # Initialize bot
        bot = FashionGuruBot(config)
        # Run CLI mode
        run_cli_mode(bot)
    else:
        # Run API mode
        run_api_mode(config)


if __name__ == '__main__':
    main()
