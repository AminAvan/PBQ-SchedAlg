# A Task Scheduler for Mobile Edge Computing Using Priority-based Reinforcement Learning

## Overview
In edge computing, the scheduling problem involves properly allocating tasks offloaded by edge users to edge servers. Therefore, scheduling the tasks at the appropriate time and allocating the right resources can be modeled as a multi-objective optimization problem in MEC. Moreover, each task has specific requirements, further adding to the complexity of the optimization problem.

We propose a Q-learning (QL)-based task scheduling algorithm (named PBQ) for edge users who want to offload their tasks to edge servers. Therefore, we formulate the task scheduling problem in edge computing as a Markov Decision Process (MDP), where the RL agent uses Q-learning to derive the optimal policy.

A key challenge of reinforcement learning (RL) in edge computing environments is the large state space, which results in prolonged learning times due to numerous and frequently changing parameters. This delay conflicts with the edge users' demand for rapid task allocation to edge servers.

To accelerate the RL-agent learning process, we design the following techniques in the PBQ method:
- We prioritize tasks from edge users based on their deadlines (inspired by EDF), where tasks with the closest deadlines are given the highest priority in PBQ.
- We partition the tasks offloaded by edge users, intended for allocation to edge servers, into smaller subsets. Each subset comprises tasks with the earliest deadlines, followed sequentially by subsets containing tasks with the next earliest deadlines. Consequently, the PBQ formulates a MDP for each subset of tasks individually, rather than for the entire set of tasks collectively.

## Implementation
1. Regarding 'state': we generate the states for Q-learning, which consists of all possible permutations of binary offloading decisions. Each state is represented as a binary matrix with 'n' rows (number of tasks from edge users) and 'k' columns (number of edge servers). Each cell in the matrix indicates whether a given task is allocated to a specific edge server (represented by a value of '1') or not allocated (represented by a value of '0').
2. Regarding 'action': at each step, the agent takes an action based on a randomly generated number. If the number is below '0.9', it selects the state with the highest reward from the Q-table; otherwise, it randomly selects the next state. The Q-table is initialized with zeros at the start of the learning process.
3. Regarding 'reward':
   1. If the 'next state' causes any edge server to transition into an 'idle' state, resulting in an available edge server with sufficient vacant processor utilization not being utilized for task execution, the agent receives the negative reward.
   2. If the agent initially assigns t<sub>1</sub> to S<sub>1</sub> and t<sub>2</sub> to S<sub>2</sub>, but reassigns them as t<sub>1</sub> → S<sub>2</sub> and t<sub>2</sub> → S<sub>1</sub> in the next state, a negative reward is incurred due to task transmission between servers. This results in data transfer overhead, increased bandwidth usage, interrupted task execution, and additional caching and queuing.
   3. If the 'next state' equals the 'current state' while assigned tasks still have "execution time", the agent receives a positive reward, as unnecessary task transmission between servers does not occur.
   4. If the next state results in unassigned tasks being allocated to edge servers without causing overloading, the agent receives a positive reward.

## Priority-Based Q-Learning (PBQ) for Accelerating Reinforcement Learning-Based Task Scheduling in Edge Computing
Large action-state spaces can slow learning progress and require substantial memory in Q-learning, as the number of states, actions, and the size of the action-state space grow exponentially with each additional variable.

For example, a network with four users and one server has $16$ possible states (each state is represented by a binary-matrix with columns as servers and rows as users, yielding $2^{(1\times 4)}=16$ states), while a network with four users and two servers has $256$ states (each represented by a $2 \times 4$ binary-matrix, yielding $2^{(2\times 4)}=256$ states). Fewer and smaller state spaces accelerate learning progress; thus, eliminating invalid or redundant states can improve Q-learning performance.

## Citation
If you found this code or our work useful, please cite it as:

```bibtex
@inproceedings{avan2023task,
  title={A Task Scheduler for Mobile Edge Computing Using Priority-based Reinforcement Learning},
  author={Avan, Amin and Kheiri, Farnaz and Mahmoud, Qusay H and Azim, Akramul and Makrehchi, Masoud and Rahnamayan, Shahryar},
  booktitle={2023 IEEE Symposium Series on Computational Intelligence (SSCI)},
  pages={539--546},
  year={2023},
  organization={IEEE}
}
```
