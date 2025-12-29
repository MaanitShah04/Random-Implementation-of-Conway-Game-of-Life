# Random-Implementation-of-Conway-s-Game-of-Life
Random Implementation and Experiments with Conway's Game of Life

If we treat the grid as a matrix $C$ where $C_{i,j} \in \{0, 1\}$ represents the state of a cell (0 = dead, 1 = alive), and let $N_{i,j}$ be the sum of the 8 neighbours for that cell:

$$
N_{i,j} = \sum_{x=-1}^{1} \sum_{y=-1}^{1} C_{i+x, j+y} - C_{i,j}
$$

The state of the cell at the next timestep ($t+1$) is determined by this boolean logic:

$$
C_{i,j}^{(t+1)} = 
\begin{cases} 
1 & \text{if } N_{i,j} = 3 \\
1 & \text{if } C_{i,j}^{(t)} = 1 \text{ AND } N_{i,j} = 2 \\
0 & \text{otherwise}
\end{cases}
$$

In the code, this is vectorised using NumPy boolean masks to update the whole grid at once:
`New State = (Neighbors == 3) OR (Current State == 1 AND Neighbors == 2)`
