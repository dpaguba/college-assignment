package view

import tools.aqua.bgw.core.BoardGameApplication

class SopraApplication : BoardGameApplication("SoPra Game") {

   private val helloScene = HelloScene()

   init {
        this.showGameScene(helloScene)
    }

}


# Modified 2025-08-11 10:24:33