package service

import view.Refreshable

/**
 * This class abstracts the refreshing service.
 *
 * @property refreshables is a list of all refreshables. You can add refreshables by calling [addRefreshable]
 */
abstract class AbstractRefreshingService {
    private val refreshables = mutableListOf<Refreshable>()

    /**
     * Adds a refreshable to the refreshables list.
     * This is the list which defines the all in [onAllRefreshables]
     *
     * @param newRefreshable is a new refreshable that should be updated
     */
    fun addRefreshable(newRefreshable : Refreshable) {
        refreshables += newRefreshable
    }

    /**
     * Call this to refresh the view
     *
     * @param method is the method that should be called and therefore the view to show
     */
    fun onAllRefreshables(method: Refreshable.() -> Unit){
        refreshables.forEach {it.method()}
    }

    /**
     * Removes all refreshables
     */
    fun removeRefreshables(){
        refreshables.clear()
    }
}