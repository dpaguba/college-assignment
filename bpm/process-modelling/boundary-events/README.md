# Boundary events

An event attached to the edge of an activity, triggering a recovery path
when something happens during it.

- **Interrupting** (solid border): the activity is abandoned and the case
  leaves on the exception flow.
- **Non-interrupting** (double dashed border): the exception path starts
  alongside while the activity keeps running.

The order example from the lecture has both on one activity: new customer
data arrives and is filed alongside, a cancellation arrives and the check
stops.

An error event is always interrupting, and it has no choice: the activity
has already declared that it cannot finish, so there is nothing left to
continue. The same holds for cancel.

## What they save

Without boundary events every exception has to sit in the control flow: a
gateway after each activity asking whether something came up. The model
roughly doubles in size, and the normal path, which is what the reader came
for, disappears among the exceptions.
