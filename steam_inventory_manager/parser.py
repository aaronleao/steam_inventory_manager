"""This module provides the function to parse the command line arguments."""

import argparse
import logging
import sys
from steam_inventory_manager import steam_api_handler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__package__)

def check_args(args):
    """Check the command line arguments for validity."""
    if args.steam_ids is None:
        if args.steam_users is None:
            raise SystemExit("Please provide either --profile-id or --profile-user.")
        elif args.steam_users:
            args.steam_ids = [steam_api_handler.resolve_vanity(args.api_key, steam_user) for steam_user in args.steam_users]

    if args.steam_ids is None and args.steam_users is None:
        raise SystemExit("Please provide either --profile-id or --profile-user.")

    # Always display player summaries if inventory is requested
    if args.display_inventory:
        args.display_player = True

    if args.display_inventory_full and not args.display_inventory:
        args.display_inventory = True

def get_args():
    """Parse the command line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch Steam inventory.")
    parser.add_argument("--steam-ids", nargs="+", type=str, help="17-digit SteamIDs.")
    parser.add_argument("--steam-users", nargs="+", type=str, help="List of users.")
    parser.add_argument(
        "--app-id", type=str, default="570", help="The app ID (Dota 2=570)."
    )
    parser.add_argument(
        "--api-key", type=str, help="Your Steam API key (optional for some games)."
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite the inventory files."
    )
    parser.add_argument(
        "--display-player", action="store_true", help="Display player summaries."
    )
    parser.add_argument(
        "--display-inventory",
        action="store_true",
        help="Display {BUNDLE, COURIER, HERO_BUNDLE, WARD, WEATHER} items.",
    )
    parser.add_argument(
        "--display-inventory-full",
        action="store_true",
        help="Display also {HERO, MISC} items.",
    )

    args = parser.parse_args()
    check_args(args)
    # logger.info("Args %s", vars(args))
    return args
