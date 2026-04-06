# Steam Inventory Query

## Deps
```shell
python -m venv .env
source .env/bin/activate
python -m pip install -r requirements.txt
```

## Fetch Steam profile ID
[Profile ID finder](https://www.steamidfinder.com/)

## Fetch  Steam API Key
[Steam API Key](https://steamcommunity.com/dev/apikey)

## How to run
```shell
set env variable $STEAM_API_KEY
python steam_inventory_manager/cli.py --profile-users user1 ... userN
```
`[deprecated] python steam_inventory_manager/cli.py --profile-id 123123123`

## TODO
- [x] Add option to display the whole inventory, HERO and MISC as well.
- [ ] Refactor display_inventory function
- [ ] Add Github actions to perform system level test
- [ ] Generate page with the inventory periodically