from config.config import Config
from config.browser_config import BrowserConfig
from config.environment import Environment
# from config.links import Links

config = Config()
config.print_config()

__all__ = [
    "config",
    # "Links"
]