# The Torchbearer

**Student Name: Matthew Kloth**
**Student ID: 131379895**
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

**FYI I use Prettier and it auto formats stuff so sorry if that messes any of the format up**

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough, name the specific decision it cannot make:**
  _While it can find a cheapest possible path for each node, it can't put all that info together to find the best order_
  _What I mean is it can't figure out that while this option may be better right now, it will acutally mess everything up later down the line_

- **What decision remains after all inter-location costs are known:**
  _After all that is know we need to figure out our specific order in hitting all the relic rooms, like what I just said above._

- **Why this requires a search over orders, not a single computation (one sentence):**
  _A single computation would give us 1 possible answer out of the pool of many different answers._

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source                                                                 |
| ---------------- | ---------------------------------------------------------------------------------- |
| _Start_          | _We always start from here_                                                        |
| _Relic_          | _We will always get to each one of these and thus we will always depart from them_ |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property                    | Your answer                                    |
| --------------------------- | ---------------------------------------------- |
| Data structure name         | _Dictionary_                                   |
| What the keys represent     | _The nodes_                                    |
| What the values represent   | _Node cost_                                    |
| Lookup time complexity      | _O(1)_                                         |
| Why O(1) lookup is possible | _Dictionary so it find the values immediately_ |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** _All our sources so S + M or just M + 1_
- **Cost per run:** _nlogn, just Dijkstras_
- **Total complexity:** _All sources * nlogn. So M + 1 * (nlogn)_
- **Justification (one line):** _We'll run Dijkstras from every source node so its just our source node count \* how long Dijkstras takes to run_

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _True shortest distance since its finalized and won't be looked at again_

- **For nodes not yet finalized (not in S):**
  _Shortest distance that we've found so far, can still be improved until it becomes finalized_

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _S literally can't be anything less than 0 so it holds_

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Because we will always pull the cheapest option from the min heap_

- **Termination : what the invariant guarantees when the algorithm ends:**
  _Guarantees that we now have the cheapest route from the source to every node possible_

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_Correct routing decisions just means that our path is the best path it can possibly be and if they were wrong then we wouldn't have the best path_

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Greedy picks the local best option which can screw everything up later rather than looking at all options available._
- **Counter-example setup:** _Lets take this table:_
  |Current | -A- | -B- | -C- | -D- | -E- |
  | --A--- | --- | -1- | -5- | -5- | 500 |
  | --B--- | --- | --- | 500 | -1- | -5- |
  | --C--- | --- | -1- | --- | -1- | 500 |
  | --D--- | -2- | -1- | -1- | --- | 500 |
  | --E--- | --- | --- | -2- | --- | --- |
  This was annoying to format

  Lets say we pick A to start and go: A->B->D->C->E = 503  
  But this would be cheaper be A->C->D->B->E = 12
  So greedy cant be optimal

- **What greedy picks:** _A->B_
- **What optimal picks:** _A->C_
- **Why greedy loses:** _Looks at the smaller picture rather than the larger picture. Wins the battle but loses the war_

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Explore every possible ORDER of combinations._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

I kinda stole the name ideas from explore but made them more readable

| Component                | Variable name in code | Data type | Description                                                |
| ------------------------ | --------------------- | --------- | ---------------------------------------------------------- |
| Current location         | current_location      | node      | Where the torchbearer is right now                         |
| Relics already collected | relics_to_visit       | set       | Set of Relics we need to visit still                       |
| Fuel cost so far         | fuel_cost_sofar       | float     | Total fuel that we've burned to get where we are right now |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property                                    | Your answer                                                                                        |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Data structure chosen                       | Set                                                                                                |
| Operation: check if relic already collected | Time complexity: O(1)                                                                              |
| Operation: mark a relic as collected        | Time complexity: O(1)                                                                              |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1)                                                                              |
| Why this structure fits                     | Because anything you do to it is time of O(1) which makes it super fast, like a simpler dictionary |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _k!_
- **Why:** _Because every new relic we get to multiplies by the previous relics but is also -1 since we've already crossed out the path to get where we are._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
