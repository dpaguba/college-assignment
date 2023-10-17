package service

import view.Refreshable

/**
 * Abstract service class handles multiples [Refreshable]s which are notified of changes to refresh
 * via the [onAllRefreshables] method.
 *
 * @property refreshables contains [Refreshable]s
 */
abstract class AbstractRefreshingService {

    private val refreshables = mutableListOf<Refreshable>()

    /** addRefreshable adds the provided [newRefreshable] to all services */
    fun addRefreshable(newRefreshable: Refreshable) {
        refreshables.add(newRefreshable)
    }

    /** addRefreshables adds each of the provided [newRefreshables] to all services */
    fun addRefreshables(vararg newRefreshables: Refreshable) {
        newRefreshables.forEach { addRefreshable(it) }
    }

    /**
     * onAllRefreshables executes the passed method on all [Refreshable]s registered with the
     * service class that extends this [AbstractRefreshingService]
     */
    fun onAllRefreshables(method: Refreshable.() -> Unit) = refreshables.forEach { it.method() }
}
