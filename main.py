import time
import numpy as np
import pandas as pd
from datetime import datetime, date
import itertools
import warnings
import csv
import psutil
warnings.simplefilter("ignore")

def get_memory_usage():
    # Get the current process ID
    process_id = psutil.Process()

    # Get the memory usage in bytes
    memory_info = process_id.memory_info()

    # Convert the memory usage to megabytes
    memory_usage_mb = memory_info.rss / (1024 ** 2)

    return memory_usage_mb


user_num = 6 # number of edge users
num_tasks = 24 # there are tasksets for 24 tasks, 48 tasks, 96 tasks in 'datasets' directory
num_resources = 1 # number of available edge servers that can be 1 or 2
initial_task_dataframe = pd.DataFrame(index=list(range(num_tasks)) ,columns=["user_id", "exection_time", "deadline"])
# input the address for dataset
initial_task_dataframe = pd.read_csv("datasets/task_dataframe_24.csv", index_col= 0)
list_of_cpu_records = []


# Define the matrix dimensions
def state_generator(user_num, server_num):
  state_list = list()
  # Define the allowed values for each cell
  CELL_VALUES = [0, 1]

  # Generate all possible permutations of the matrix
  permutations = list(itertools.product(*([CELL_VALUES]*user_num*server_num)))

  # Filter out permutations that violate the constraint
  valid_permutations = []
  counter = 0
  row_checker = list()
  for perm in permutations:
      matrix = [list(perm[i:i+server_num]) for i in range(0, user_num*server_num, server_num)]
      # pdb.set_trace()
      matrix = np.reshape(np.array(matrix),(user_num,server_num))
      column_sums = [sum(col) for col in zip(*matrix)]
      yy = list()
      for row in matrix:
        row_sum = sum(row)
        yy.append(row_sum)
      # pdb.set_trace()
      flag_row=all(x <= 1 for x in yy)
      col_sum = np.sum(matrix, axis= 0)
      flag_col = all(col_sum)


      if all(sum <= 1 for sum in column_sums) and (flag_row == True) or np.sum(matrix) == 0 :
          state_list.append(matrix)
          counter = counter + 1
  return state_list, counter


def reward_function(current_state, next_state, num_tasks, num_resources, task_dataframe, done):
  is_scheduled = False
  total_reward = 0
  active_server_num = np.sum(next_state)
  index_tasks = list(np.where(current_state == 1)[0])
  y = False
  for i in index_tasks:
      task_slice = task_dataframe.loc[i].copy()
      task_slice["exection_time"] -= 1
      task_dataframe.loc[i] = task_slice
      # pdb.set_trace()
  # print("task_dataframe in reward:", task_dataframe)


  execution_time_list = list(task_dataframe.loc[index_tasks]["exection_time"])
  all_greater_than_0 = all(x >= 0 for x in execution_time_list)
  # pdb.set_trace()
  if all(task_dataframe["exection_time"] == 0):
    # print("workload scheduled")
    is_scheduled = True
    #print("is_scheduled in rwrd func", is_scheduled)
    #print("workload scheduled, here is the dataframe:", task_dataframe)
  if active_server_num == 0:
    total_reward = -((num_resources*(num_tasks*num_resources))**num_tasks)
    done = True
  else:
    total_reward = total_reward + (active_server_num*(num_tasks*num_resources))
    if ((next_state == current_state) & (all_greater_than_0 == True )).any():
          total_reward = total_reward + (num_resources*(num_tasks*num_resources))
    elif ((next_state == current_state) & (all_greater_than_0 == False )).any():
          total_reward = total_reward - (num_resources*(num_tasks*num_resources))
  if any(task_dataframe["exection_time"] < 0):
    total_reward = -((num_resources*(num_tasks*num_resources))**num_tasks)
    # if there is any (-1) in the execution time of dataframe, then it should consider as a GAMEOVER for the learning
    done = True
  return total_reward, task_dataframe, done, is_scheduled



def q_learning(user_num, num_resources, top_not_excuted_tasks):
    total_episode_reward = 0
    state_list, counter = state_generator(user_num, num_resources)
    epsilon = 0.9  # Epsilon-greedy policy parameter
    alpha = 0.1  # Learning rate
    gamma = 0.9  # Discount factor
    q_table = np.zeros((counter,counter))
    episode_brocker = False
    episode = 0
    while(episode_brocker != True):
        episode = episode +1
        task_dataframe = top_not_excuted_tasks.copy()
        # pdb.set_trace()
        # print("episode =>", episode)
        #print("first data frame of ep", episode, "is:", task_dataframe)
        current_state = 0  # Start in the initial state (no tasks scheduled)
        total_reward = 0  # Track the total reward for the episode
        done = False
        while not done:
            # Choose an action based on the epsilon-greedy policy
            if np.random.uniform() < epsilon:
                action = np.argmax(q_table[current_state])
            else:
                action = np.random.randint(counter)
            next_state = action
            if next_state == 0:
              #q_table[:,0] = -((num_resources*(num_tasks*num_resources))**num_tasks) ## COMMENT FOR 192
              q_table[:,0] = -((num_resources*(num_tasks+num_resources))*num_tasks) ## add for 192

            r, task_dataframe, done, episode_brocker = reward_function(state_list[current_state], state_list[next_state], user_num, num_resources, task_dataframe, done)
            #print("is_scheduled in q-learn", episode_brocker)
            #print(task_dataframe)
            #print("reward =>", r)
            # Update the Q-value based on the reward and next state
            # pdb.set_trace()
            q_table[current_state, next_state] += alpha * (r + gamma * np.max(q_table[next_state]) - q_table[current_state, next_state])
            total_reward += r
            # pdb.set_trace()
            # Move to the next state
            if next_state == 0:
              q_table[:,0] = r
            current_state = next_state

            if (all(x == 0 for x in task_dataframe["exection_time"])):
                done = True
        # print("Last dataframe:", task_dataframe)
        # print("Episode:", episode, "Total Reward:", total_reward)
        # print('==================================================')
    return episode_brocker

# Determining the number of times that PBQ performs scheduling is useful for executing multiple runs
# to compute the average runtime and RAM usage.
for j in range(1, 2):
  now = datetime.now()
  today = date.today()
  current_time = now.strftime("%H:%M:%S")
  d2 = today.strftime("%B %d, %Y")
  # print("start:", d2,"at", current_time)
  ####
  tem_data_frame = initial_task_dataframe.copy()
  print(f"The {j}th round of runs:")
  # capture the start time
  start_time = 0
  start_time=time.time()
  for i in range(int(num_tasks/user_num)):
    #print("====================================================")
    # print("i=>", i)
    #now = datetime.now()
    #today = date.today()
    #current_time = now.strftime("%H:%M:%S")
    #d2 = today.strftime("%B %d, %Y")
    #print("start:", d2,"at", current_time)
    mask = tem_data_frame[tem_data_frame['exection_time'] > 0 ]
    sorted_task_dataframe =mask.sort_values(by=['deadline'])
    top_not_excuted_tasks = sorted_task_dataframe.head(user_num)
    original_indexs = sorted_task_dataframe.head(user_num).index
    top_not_excuted_tasks = top_not_excuted_tasks.reset_index()
    #print("tem_data_frame", tem_data_frame)
    #print("top_not_excuted_tasks", top_not_excuted_tasks)
    if (q_learning(user_num, num_resources, top_not_excuted_tasks)):
      # print("is_scheduled in LAST")
      tem_data_frame.loc[original_indexs, "exection_time"] = 0
      # now = datetime.now()
      # today = date.today()
      # current_time = now.strftime("%H:%M:%S")
      # d2 = today.strftime("%B %d, %Y")
      #print("end:", d2,"at", current_time)
  total_time = 0
  total_time=time.time()-start_time
  # runtime for each round of PBQ on a normal machine in scenario
  #   with one edge server and 24, 48, or 96 tasks, the runtime is approximately 1054, 2053, or 3186 seconds, respectively.
  #   with two edge servers and 24, 48, or 96 tasks, the runtime is approximately 82, 160, or 317 seconds, respectively.
  print(f"total time of {j}th run is: {total_time}")
  # Get and print the memory usage
  memory_usage = get_memory_usage()
  print(f"Memory Usage: {memory_usage:.2f} MB")