# GBF Damage Parser

Original [github](https://github.com/sjieh/scuffed-gbfr-parser)

This is a fork of the original parser, making it a bit more user friendly and adding some features.

Features:

- Tracks **YOUR** damage accurately, including turrets in Protobaha and other similar quests and Rosetta's plants
- Automatic reset upon entering every **BOSS** quest
- *New Save your runs to a file

Planned features:

- Load runs from a file
- Saving/Showing mission name
- Calculating average damage of all the run, and comparing to the current run

Known bugs/nuances:

- Counts AI party member damage, but not online party member damage
- Protobaha Skyfall 1 adds ~20mil to damage for some reason lol
- Survival quests don't use the same timer function that boss quests do, so the parser doesn't reset automatically on them
