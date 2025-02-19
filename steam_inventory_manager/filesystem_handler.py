"""File system handler for the Steam Inventory Query package."""

import json
import logging
import os
import sys

from steam_inventory_manager import constants

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__package__)


def create_cache_dir():
    """Create the cache directory if it does not exist."""
    if not os.path.exists(constants.CACHE_DIR):
        os.makedirs(constants.CACHE_DIR)

def read_json(json_file_path: str) -> dict:
    """Read the inventory from the given file path."""
    with open(json_file_path, "r", encoding="utf-8") as file:
        logger.info("Reading '%s'.", json_file_path)
        inventory_json = json.load(file)
        return inventory_json

def write_json(json_file_path: str, inventory_json: dict):
    """Write the inventory to the given file path."""
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(inventory_json, file, indent=4)
    logger.info("Inventory saved in: '%s'.", json_file_path)
