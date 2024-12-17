# A Task Scheduler for Mobile Edge Computing Using Priority-based Reinforcement Learning

## Overview
In edge computing, the scheduling problem involves properly allocating tasks offloaded by edge users to edge servers. Therefore, scheduling the tasks at the appropriate time and allocating the right resources can be modeled as a multi-objective optimization problem in MEC. Moreover, each task has specific requirements, further adding to the complexity of the optimization problem.

We propose a Q-learning (QL)-based task scheduling algorithm (named PBQ) for edge users who want to offload their tasks to edge servers. Therefore, we formulate the task scheduling problem in edge computing as a Markov Decision Process (MDP), where the RL agent uses Q-learning to derive the optimal policy.

A key challenge of reinforcement learning (RL) in edge computing environments is the large state space, which results in prolonged learning times due to numerous and frequently changing parameters. This delay conflicts with the edge users' demand for rapid task allocation to edge servers.

To accelerate the reinforcement learning process in the given scenario, we propose the following approaches:
- We prioritize tasks from edge users based on their deadlines (inspired by EDF), where tasks with the closest deadlines are given the highest priority in PBQ.
- We devide the whole tasks from edge users that are supposed to be allocated to edge servers into small portions, i.e., we divude the tasks in the group of four tasks instead of the whole tasks such as  

## Implementation
1. Regarding 'state': we generate the state space for Q-learning, which consists of all possible permutations of binary offloading decisions. Each state is represented as a binary matrix with n rows (indicating the number of tasks from edge users) and k columns (representing the number of edge servers). Each cell in the matrix specifies whether a given task is allocated to a particular edge server.
2. Regarding 'reward': if the 'next state' causes any edge server to transition into an 'idle' state, resulting in an available edge server with sufficient vacant processor utilization not being utilized for task execution, the agent receives the negative reward.
3. Regarding 'reward': if the agent assigns task t<sub>1</sub> to server Si or task Tj to server Sj in the current state and reassigns them to server Sj and Si, respectively, a negative reward is incurred. This transition involves the transmission of tasks from one server to another, resulting in data transmission, bandwidth overhead, preempting task execution, and additional caching and queuing processes.

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
