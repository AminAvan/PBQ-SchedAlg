# A Task Scheduler for Mobile Edge Computing Using Priority-based Reinforcement Learning

## Overview
In edge computing, the scheduling problem involves properly allocating tasks offloaded by edge users to edge servers. Therefore, scheduling the tasks at the appropriate time and allocating the right resources can be modeled as a multi-objective optimization problem in MEC. Moreover, each task has specific requirements, further adding to the complexity of the optimization problem.

We propose a Q-learning (QL)-based task scheduling algorithm (named PBQ) for edge users who want to offload their tasks to edge servers.

Therefore, we formulate the task scheduling problem in edge computing as a Markov Decision Process (MDP), where the RL agent uses Q-learning to derive the optimal policy.

We prioritize tasks from edge users based on their deadlines (inspired by EDF), where tasks with the closest deadlines are given the highest priority in PBQ.

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
