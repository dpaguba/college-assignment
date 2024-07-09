# Modelling

| Topic | |
|---|---|
| [four-step-design](four-step-design/) | the order that makes the steps answerable |
| [star-schema](star-schema/) | one fact table and its dimensions |
| [snowflake-schema](snowflake-schema/) | normalising the small tables |
| [slowly-changing-dimensions](slowly-changing-dimensions/) | what to do when an attribute changes |

Part IV of the lecture. Every decision in the block follows from one
observation: the fact table holds a thousand times the rows of everything
else together, so a technique that saves space in the dimensions saves 0.1
percent and a join saved on the fact table saves everything.

The grain is the declaration the rest depends on. It decides which measures
may be stored, which attributes are dimensions, and how many rows the table
will hold.
