# Working assumptions

Let $G = (V, E)$ be an instance, $G \in$ {`hard_to_choose.txt`, `islands.txt`, `paris_map.txt`}.

1. **Connected components.** If $G$ has $k$ connected components, we compute $k$ paths, one per component, even though the statement mentions a single path. The total cost is the sum of the costs of the $k$ paths.
2. **Identical parallel edges.** If two vertices $i, j$ are linked by several edges with the same weight (whatever the order of $i$ and $j$ in the file), we keep a single edge, which the path must traverse at least once. This follows the repository author's intent: `example_solution.py` stores the edges in a `set`. Parallel edges with *different* weights are all kept.
3. **Open path.** The path does not have to return to its starting point, and both its start and its end are free (no depot). The greedy `example_solution.py` starts from vertex 0, but its comment (`# Pick a starting vertex`) suggests an arbitrary choice rather than an imposed depot.
4. **Output.** For each component, an ordered list of oriented edges $(u, v, w, c_u, c_v)$, in the repository format, where each edge starts where the previous one ends.

## Instances

Checked on the files: no loops, no isolated vertices, integer weights $\ge 1$. The last two columns are computed after merging identical parallel edges (assumption 2).

| Instance | $\|V\|$ | $\|E\|$ (file) | Merged edges | $\|E\|$ (kept) | Components | Odd vertices |
|---|--:|--:|--:|--:|--:|--:|
| `hard_to_choose` | 35 | 595 | 0 | 595 | 1 | 0 |
| `islands` | 60 | 760 | 54 | 706 | 3 | 50 |
| `paris_map` | 11 348 | 17 958 | 0 | 17 958 | 1 | 7 318 |
