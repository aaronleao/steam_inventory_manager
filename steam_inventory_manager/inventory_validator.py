"""This module contains functions to validate the inventory data."""

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__package__)


def validate_format(inventory: dict) -> bool:
    """Validates the format of the inventory data."""
    if not inventory or "assets" not in inventory or "descriptions" not in inventory:
        logger.error("Error: Invalid inventory data.")
        return False
    return True


def validate_size(inventory: dict) -> bool:
    """Validates the size of the inventory data."""
    if len(inventory["assets"]) == 0:
        return False
    return True
