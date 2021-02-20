# Clash Royale River Race Deck Builder

Generate decks for the River Race based on the most successful decks in the game.

## config.ini

Key | Value | Description
--- | --- | ---
log | 0<br>1 | Enable console output
initial | 0<br>1  | Consider initial deck
excluded | e.g. Golem | Cards that should not be included
source | popular decks<br>top 200 players<br>royale api<br>clash royale api | The source for deck generation

## Enviroment Variables

The following command can be used to add the [Clash Royale API Key][cb956311] to the environment variables in Windows:

```batch
setx CLASH_ROYALE_API_KEY "Clash Royale API Key" /m
```

[cb956311]: https://developer.clashroyale.com/ "Clash Royale API Key"
