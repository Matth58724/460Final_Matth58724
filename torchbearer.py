"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Matthew Kloth
Student ID:   131379895

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():

    explain = ("Why a single shortest-path run from S is not enough, name the specific decision it cannot make: "
    "While it can find a cheapest possible path for each node, it cant put all that info together to find the best order"
    "What I mean is it cant figure out that while this option may be better right now, it will acutally mess everything up later down the line"
    "What decision remains after all inter-location costs are known:"
    "After all that is know we need to figure out our specific order in hitting all the relic rooms, like what I just said above."
    "Why this requires a search over orders, not a single computation (one sentence):"
    "A single computation would give us 1 possible answer out of the pool of many different answers.")

    return explain

    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """


# =============================================================================
# PART 2
# =============================================================================

# PART 2a
def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    """
    # I hope im not oversimplifying this
    # We basically just need to make a list of the sources we want
    return [spawn] + relics





# 2b
def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    # Just Dijkstra's

    # Start everything at infinity
    distance = {node: float('inf') for node in graph}
    distance[source] = 0 # Whatever we're on rn

    # Then the minheap which will store the cost and then the node
    heap = [(0, source)]

    while heap:
        cost, u = heapq.heappop(heap) # Get the cheapest node

    # If we already have a more effiecient path then we'll skip, it'd also help to properly indent
        if cost > distance[u]:
            continue

        # Look at all the nodes adjacent to u and their weights
        for v, weight in graph[u]:
            new_cost = distance[u] + weight
            if new_cost < distance[v]: # If we found a cheaper one
                distance[v] = new_cost
                heapq.heappush(heap, (new_cost, v)) # push v back to heap
    return distance # Final shortest distances for all nodes


# 2c
def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """

    distance_table = {}

    # Spawn + all relics
    sources = select_sources(spawn, relics, exit_node)

    # Run Dijkstras for every source
    for source in sources:
        distance_table[source] = run_dijkstra(graph, source)

    return distance_table








# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    dijkstra_explain = ("For nodes already finalized (in S): _True shortest distance since its finalized and won't be looked at again_"
    "**For nodes not yet finalized (not in S):**"
    "_Shortest distance that we've found so far, can still be improved until it becomes finalized_"
    "**Initialization : why the invariant holds before iteration 1:**"
    "_S literally can't be anything less than 0 so it holds_"
    "**Maintenance : why finalizing the min-dist node is always correct:**"
    "_Because we will always pull the cheapest option from the min heap_"
    "**Termination : what the invariant guarantees when the algorithm ends:**"
    "_Guarantees that we now have the cheapest route from the source to every node possible_"
    "_Correct routing decisions just means that our path is the best path it can possibly be and if they were wrong then we wouldn't have the best path_")

    return dijkstra_explain


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    explainSearch = ("**The failure mode:** _Greedy picks the local best option which can screw everything up later rather than looking at all options available._"
    "**Counter-example setup:** _Lets take this table:_"
    "|Current | -A- | -B- | -C- | -D- | -E- |"
    "| --A--- | --- | -1- | -5- | -5- | 500 |"
    "| --B--- | --- | --- | 500 | -1- | -5- |"
    "| --C--- | --- | -1- | --- | -1- | 500 |"
    "| --D--- | -2- | -1- | -1- | --- | 500 |"
    "| --E--- | --- | --- | -2- | --- | --- |"
    "This was annoying to format"
    "Lets say we pick A to start and go: A->B->D->C->E = 503  "
    "But this would be cheaper be A->C->D->B->E = 12"
    "So greedy cant be optimal"
    "**What greedy picks:** _A->B_"
    "**What optimal picks:** _A->C_"
    "**Why greedy loses:** _Looks at the smaller picture rather than the larger picture. Wins the battle but loses the war_"
    "_Explore every possible ORDER of combinations._")
    return explainSearch


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    # Still pretty simple for now
    # These 3 are self explanatory, I barely changed the names from explore (I'm a very creative person)
    current_location = spawn
    relics_to_visit = set(relics)
    fuel_cost_sofar = 0

    # We'll start with the cost being infinity and nothing in the order since we haven't found anything yet
    best = [float('inf'), []]

    # Exploring
    _explore(dist_table, current_location, relics_to_visit, [], fuel_cost_sofar, exit_node, best)
    return (best[0], best[1]) # Return the best cost and best order that we can have





def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """



    # Thought process beforehand
    # We want to stop the recursion when we have no more relics to hit (base case)
    # We will also prune when we predict the cost will be greater than the current best
    # Want to do recursion for every new relic that we have to look at

    # Base case
    if not relics_remaining:
        final_cost = cost_so_far + dist_table[current_loc][exit_node]
        if final_cost < best[0]:
            best[0] = final_cost
            best[1] = list(relics_visited_order)
        return

    # Pruning
    # If the lower bound and the cost so far add up to anything more the current "best" 
    # then there is no possible way it will ever be better than best, so we should leave it and save resources.
    # And since the lower bound never overestimates, so if it can't beat the current best then we are gaurenteed to not be able to beat it
    lower_bound = (min(dist_table[current_loc][r] for r in relics_remaining) + min(dist_table[r][exit_node] for r in relics_remaining))
    if cost_so_far + lower_bound >= best[0]:
        return

    # Recursion
    for relic in list(relics_remaining):
        cost_to_relic = dist_table[current_loc][relic]
        
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        
        _explore(dist_table, relic, relics_remaining, relics_visited_order, cost_so_far + cost_to_relic, exit_node, best)
        
        # Backtracking, just reverse what we did
        relics_remaining.add(relic)
        relics_visited_order.pop()
    # This all actually wasnt that bad since the README helped me chip away step by step instead of throwing me into the entire algorithm immediately


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    # Get all distances into the table first
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    
    # Find the best route with the  distance table
    return find_optimal_route(dist_table, spawn, relics, exit_node)


    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
