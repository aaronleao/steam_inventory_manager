"""Main entry point for the Steam inventory query CLI."""

# Description: Main entry point for the Steam inventory query CLI.
#
# This module is responsible for handling the main entry point for the Steam inventory query CLI.
# It performs the following steps:
# 1. Resolves Steam IDs from Steam usernames if necessary.
# 2. Fetches the inventory for each Steam ID.
# 3. Displays the fetched inventories if the display option is enabled.

from steam_inventory_manager import filesystem_handler
from steam_inventory_manager import parser
from steam_inventory_manager import player


def main():
    """
    Main function to handle the Steam inventory query process.

    This function performs the following steps:
    1. Resolves Steam IDs from Steam usernames if necessary.
    2. Fetches Player summaries
    3. Fetches Player inventory
    4. Displays the fetched inventories if the display option is enabled.
    """

    # Get args
    args = parser.get_args()

    print(args.steam_ids, args.steam_users)

    players = [
        player.Player(args.api_key, steam_id, args.overwrite, args.app_id)
        for steam_id in args.steam_ids
    ]

    for p in players:
        if args.display_player:
            p.print()
        if args.display_inventory:
            p.print_inventory(args.display_inventory_full)

    # players[0].update_inventory_json_descriptions()

    # filesystem_handler.write_json("saida.json", players[0].inventory_json_descriptions)


if __name__ == "__main__":
    # Create cache dir
    filesystem_handler.create_cache_dir()
    main()
