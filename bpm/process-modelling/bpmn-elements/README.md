# BPMN elements

The catalogue: events, tasks, gateways, the two kinds of flow, pools and
lanes, data objects and stores.

The one rule in this module that a model can violate is the rule about the
two flows. A **sequence flow** orders the steps of one participant and stays
inside its pool. A **message flow** goes between participants and always
crosses a pool boundary; inside a pool it would be meaningless, because the
participant would be sending a message to itself.

`check_flows` tests exactly that for every flow of a model, and it treats a
pool as lying inside itself, which removes the special case: a flow from a
node to a pool crosses a boundary if the node is in a different pool.

The example is the order process from the lecture: the customer sends a
purchase order, sales checks availability, and depending on the answer either
cancels or confirms, ships and invoices. Adding a sequence flow from the
supplier's receive event to the customer pool makes the check report one
error, which is the mistake this rule exists to catch.

Pool and lane are often mixed up: the pool is a participant, the lane a role
inside one. Two lanes of the same pool share a control flow; two pools do
not.
