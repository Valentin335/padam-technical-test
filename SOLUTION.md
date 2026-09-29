# Solution

Covering every edge at minimum cost is the **Chinese Postman Problem**, here in its open-path variant (no return to the start). Working assumptions (one path per connected component, merged identical parallel edges, free start and end) are listed in [docs/hypotheses.md](docs/hypotheses.md).

## 0. Why the naive greedy fails

`example_solution` walks along uncovered edges until the current vertex has none left. It then stops, although uncovered edges remain elsewhere: it has no way to go back.

## 1. Fixing the greedy

When the walk gets stuck while edges remain, we resume from a vertex of the walk that still has unused edges, and insert the new sub-circuit there. A stack does this implicitly, in O(|E|) (`eulerian.py`).

It works only if the connected graph has **0 odd-degree vertices** (the walk is a circuit) or **2** (start from one of them, the walk ends at the other). `hard_to_choose` is a complete graph K35: all degrees are 34, so every edge is traversed once, for a cost of 1200 = sum of the weights, which is optimal.

## 2. Odd vertices: a minimum-weight perfect matching

The cost of a walk only depends on which edges are traversed twice, not on the order. Traversing an edge again amounts to **duplicating** it. Duplicating the edges of a path between two odd vertices makes both of them even and leaves the intermediate vertices unchanged (+2).

So the odd vertices must be paired, each pair linked by a shortest path, at minimum total cost: a **minimum-weight perfect matching** (Edmonds' Blossom algorithm). Once the edges are duplicated, the fixed greedy of part 1 builds the walk.

`paris_map` has 7318 odd vertices, i.e. 26.8M pairs: too many to compute all shortest paths. PyMatching (sparse blossom, Higgott & Gidney 2023) solves the matching directly on the sparse graph and returns the edges to duplicate (`eulerize.py`).

## 3. Open path: two dummy vertices

A perfect matching makes every vertex even, hence a circuit. But the path does not have to come back: 2 odd vertices may stay odd.

Two dummy vertices `s` and `t` are added, each linked to every odd vertex, and must be matched too. The vertex matched to a dummy vertex stays odd: it becomes the start or the end. An edge to a dummy vertex costs W (sum of the weights): taking 3 such edges instead of 1 costs 2W more, while freeing 2 more vertices saves at most one shortest path (≤ W). So each dummy vertex takes exactly one edge, and the matching chooses the best start and end. On `paris_map`: 27927 (circuit) → 27918.

Computing the circuit and removing its most expensive duplicated path afterwards is not optimal: freeing two vertices can change the whole pairing.

## 4. Algorithm

For each connected component:

1. `edges_to_duplicate`: minimum-weight perfect matching of the odd vertices + 2 dummy vertices (PyMatching);
2. `eulerian_path` (fixed greedy of part 1) on the edges + duplicated edges, from an odd vertex;
3. `check`: independent checker (contiguity, real edges and weights, every edge covered, one path per component).

| Instance | Components | Odd vertices | Cost | Lower bound W | Time |
|---|--:|--:|--:|--:|--:|
| `hard_to_choose` | 1 | 0 | 1200 | 1200 | < 2 s |
| `islands` | 3 | 20 + 10 + 20 | 486 + 797 + 492 = 1775 | 1753 | < 2 s |
| `paris_map` | 1 | 7318 | 27918 | 22924 | < 2 s |

Times measured on a Dell Latitude 5580 laptop (Intel Core i7-7820HQ @ 2.90 GHz, 16 GB RAM), Python 3.12, PyMatching 2.4, Python startup included.

Optimality follows from the matching. 

```bash
pip install -r requirements.txt
python main.py -i instances/paris_map.txt      # add -p to plot the instance and the path
```
