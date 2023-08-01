# Akka practical

Two copies of the karaoke exercise:

| | |
|---|---|
| [akkablanko](akkablanko/) | the worked version, with the actors filled in |
| [akkaBlanko-main](akkaBlanko-main/) | the distributed template, plus a `Scheduler` the worked copy does not use |

The worked copy defines `LibraryActor`, `QueueManagerActor`,
`PlaybackClientActor`, `SpawnerActor` and `KaraokeSingerActor`, which
communicate through references handed over at construction: the spawner needs
the queue manager to give each singer it creates, so the queue manager is
spawned first.

Two message sends had been left unfinished and prevented compilation. Both are
completed: the spawner receives a parameterless `CreateSingerMessage`, and the
singer sends itself a `StartSingingMessage` after choosing a song. The sources
now parse with no syntax errors; building further needs the Akka jars, which
the Gradle wrapper fetches.
