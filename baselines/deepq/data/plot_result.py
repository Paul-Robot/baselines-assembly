# -*- coding: utf-8 -*-
"""
# @Time    : 24/10/18 2:40 PM
# @Author  : ZHIMIN HOU
# @FileName: plot_result.py
# @Software: PyCharm
# @Github    ： https://github.com/hzm2016
"""

import matplotlib.pyplot as plt
import numpy as np

"""=================================Plot result====================================="""
YLABEL = ['Fx(N)', 'Fy(N)', 'Fz(N)', 'Mx(Nm)', 'My(Nm)', 'Mz(Nm)']
Title = ["X axis force", "Y axis force", "Z axis force",
         "X axis moment", "Y axis moment", "Z axis moment"]
COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'pink',
        'brown', 'orange', 'teal', 'coral', 'lightblue', 'lime', 'lavender', 'turquoise',
        'darkgreen', 'tan', 'salmon', 'gold', 'lightpurple', 'darkred', 'darkblue']
"""================================================================================="""


# plot the forces and moments
def plot_learning_force_and_moment(path_2, path_3, name):
    V_force = np.load(path_2)
    V_state = np.load(path_3)

    initial_position = np.array([539.88427, -38.68679, 190.03184, 179.88444 - 180, 1.30539, 0.21414])

    high = np.array([40, 40, 0, 5, 5, 5, 542, -36, 192, 5, 5, 5])
    low = np.array([-40, -40, -40, -5, -5, -5, 538, -42, 188, -5, -5, -5])
    scale = high - low
    length = 38
    v_forces = np.zeros([len(V_force), length, 6])
    for i in range(len(V_force)):
        for j in range(length):
            for m in range(6):
                v_forces[i, j, m] = np.array(V_force[i])[j, m]

    v_states = np.zeros([len(V_state), length, 6])
    for i in range(len(V_state)):
        for j in range(length):
            for m in range(6):
                v_states[i, j, m] = np.array(V_state[i])[j, m+6]
    mean_force = np.mean(v_forces, axis=0)
    std_force = np.std(v_forces, axis=0)
    mean_state = np.mean(v_states, axis=0)
    std_state = np.std(v_states, axis=0)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    plt.figure(figsize=(20, 10), dpi=100)

    plt.tight_layout(pad=3, w_pad=1., h_pad=0.5)
    plt.subplots_adjust(left=0.08, bottom=0.10, right=0.98, top=0.98, wspace=0.23, hspace=0.23)
    plt.subplot(1, 2, 1)
    for num in range(6):
        if num > 2:
            plt.plot((mean_force[:, num] * scale[num] + low[num]) * 10, linewidth=2.75)
            plt.fill_between(np.arange(len(mean_force[:, 0])),
                             ((mean_force[:, num] - std_force[:, num]) * scale[num] + low[num]) * 10,
                             ((mean_force[:, num] + std_force[:, num]) * scale[num] + low[num]) * 10, alpha=0.3)
        else:
            plt.plot(mean_force[:, num] * scale[num] + low[num], linewidth=2.75)
            plt.fill_between(np.arange(len(mean_force[:, 0])),
                             (mean_force[:, num] - std_force[:, num]) * scale[num] + low[num],
                             (mean_force[:, num] + std_force[:, num]) * scale[num] + low[num], alpha=0.3)
        # plt.plot(mean_force[:, num] * scale[num] + low[num], linewidth=2.)
        # plt.fill_between(np.arange(len(mean_force[:, 0])),
        #                  (mean_force[:, num] - std_force[:, num]) * scale[num] + low[num],
        #                  (mean_force[:, num] + std_force[:, num]) * scale[num] + low[num], alpha=0.3)

    plt.xlabel("Steps", fontsize=30)
    plt.ylabel("Forces$(N)$ / Moments$(10XNm)$", fontsize=30)
    plt.legend(labels=['$F_x$', '$F_y$', '$F_z$', '$M_x$', '$M_y$', '$M_z$'], loc='lower right', fontsize=30)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    plt.subplot(1, 2, 2)
    for num in range(6):
        plt.plot(mean_state[:, num] * scale[num + 6] + low[num + 6] - initial_position[num], linewidth=2.75)
        plt.fill_between(np.arange(len(mean_state[:, 0])),
                         (mean_state[:, num] - std_state[:, num]) * scale[num + 6] + low[num + 6] - initial_position[num],
                         (mean_state[:, num] + std_state[:, num]) * scale[num + 6] + low[num + 6] - initial_position[num], alpha=0.3)
    plt.xlabel("Steps", fontsize=30)
    plt.ylabel("Position$(mm)$ / Orientation$(\circ)$", fontsize=30)
    plt.legend(labels=['$P_x$', '$P_y$', '$P_z$', '$O_x$', '$O_y$', '$O_z$'], loc='lower right', fontsize=30)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    plt.savefig(name + '.pdf')
    plt.show()


def plot_raw_data(path_1):
    data = np.load(path_1)
    force_m = np.zeros((len(data), 12))

    plt.figure(figsize=(20, 20), dpi=100)
    plt.tight_layout(pad=3, w_pad=0.5, h_pad=1.0)
    plt.subplots_adjust(left=0.065, bottom=0.1, right=0.995, top=0.9, wspace=0.2, hspace=0.2)
    plt.title("True Data")
    for j in range(len(data)):
        force_m[j] = data[j, 0]
    k = -1
    for i in range(len(data)):
        if data[i, 1] == 0:
            print("===========================================")
            line = force_m[k+1:i+1]
            print(line)
            k = i
            for j in range(6):
                plt.subplot(2, 3, j + 1)
                plt.plot(line[:, j])
                # plt.plot(line[:, 0])

                if j == 1:
                    plt.ylabel(YLABEL[j], fontsize=17.5)
                    plt.xlabel('steps', fontsize=20)
                    plt.xticks(fontsize=15)
                    plt.yticks(fontsize=15)

                else:
                    plt.ylabel(YLABEL[j], fontsize=20)
                    plt.xlabel('steps', fontsize=20)
                    plt.xticks(fontsize=15)
                    plt.yticks(fontsize=15)
        i += 1
    plt.savefig('raw_data_random_policy1.jpg')


# plot the reward and step
def plot_compare(fuzzy_path, none_fuzz_path):

    reward_fuzzy = np.load(fuzzy_path)
    reward_none_fuzzy = np.load(none_fuzz_path)

    reward_average = np.zeros(len(reward_fuzzy))
    reward_none_average = np.zeros(len(reward_none_fuzzy))
    for i in range(len(reward_fuzzy)):
        sum_1 = 0
        sum_2 = 0
        num = 0
        for j in range(10):
            if j + i < len(reward_fuzzy):
                sum_1 += reward_fuzzy[i+j]
                sum_2 += reward_none_fuzzy[i+j]
                num += 1
        reward_average[i] = sum_1/num
        reward_none_average[i] = sum_2/num

    plt.figure(figsize=(10, 8), dpi=100)
    plt.subplot(1, 1, 1)
    plt.tight_layout(pad=4.9, w_pad=1., h_pad=1.)

    plt.plot(np.arange(len(reward_none_fuzzy) - 1), np.array(reward_average[1:]), color='r', linewidth=5, alpha=0.4)
    plt.plot(np.arange(len(reward_none_fuzzy) - 1), np.array(reward_none_average[1:]), color='b', linewidth=5, alpha=0.4)
    plt.plot(np.arange(len(reward_none_fuzzy) - 1), np.array(reward_none_fuzzy[1:]), color='b', linewidth=2.5, label='Normal DQN')
    plt.plot(np.arange(len(reward_none_fuzzy) - 1), np.array(reward_fuzzy[1:]), color='r', linewidth=2.5, label='Prediction-based DQN')
    # plt.ylim(-5, 1)
    plt.yticks(fontsize=24)
    plt.ylabel('Episode Step', fontsize=24)
    # plt.ylabel('Episode Reward', fontsize=24)
    plt.xticks(fontsize=24)
    plt.xlabel('Episodes', fontsize=24)
    plt.legend(fontsize=24, loc='lower right')

    # plot_reward('./episode_rewards_100.npy')
    # plt.figure(figsize=(15, 15), dpi=100)
    # plt.subplot(2, 1, 2)
    # plt.title('DQN With Knowledge')
    # plt.plot(np.arange(len(reward_fuzzy) - 1), np.array(reward_fuzzy[1:] * 10), color='b')
    # plt.ylabel('Episode Reward', fontsize=20)
    # plt.xlabel('Episodes', fontsize=20)

    plt.savefig('./figure/pdf/dqn_episode_step.pdf')
    plt.savefig('./figure/jpg/dqn_episode_step.jpg')
    plt.show()


def plot_continuous_data(path):
    raw_data = np.load(path)
    print(raw_data)
    plt.figure(figsize=(20, 15))
    plt.title('Episode Reward')
    plt.tight_layout(pad=3, w_pad=0.5, h_pad=1.0)
    plt.subplots_adjust(left=0.1, bottom=0.15, right=0.98, top=0.9, wspace=0.23, hspace=0.22)
    # plt.subplots_adjust(left=0.065, bottom=0.1, right=0.995, top=0.9, wspace=0.2, hspace=0.2)
    data = np.zeros((len(raw_data), 12))
    for j in range(len(raw_data)):
        data[j] = raw_data[j, 0]
    for j in range(6):
        plt.subplot(2, 3, j + 1)
        plt.plot(data[:, j], linewidth=2.5, color='r')
        # plt.ylabel(YLABEL[j], fontsize=18)
        if j>2:
            plt.xlabel('steps', fontsize=30)
        plt.title(YLABEL[j],fontsize=30)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.2)
    # plt.savefig('raw_data.pdf')
    plt.show()


if __name__ == "__main__":
    # reward_1 = np.load('./episode_rewards.npy')
    # reward_2 = np.load('./episode_rewards_1.npy')
    # reward_3 = np.load('./episode_rewards_2.npy')
    # reward_fuzzy = np.load('./episode_rewards_fuzzy.npy')
    # reward_none_fuzzy = np.load('./episode_rewards_none_fuzzy.npy')

    plot_compare('episode_steps_fuzzy_noise_final.npy', 'episode_steps_none_fuzzy_noise_final.npy')
    # plot_compare('episode_rewards_fuzzy_noise_final.npy', 'episode_rewards_none_fuzzy_noise_final.npy')

    # plot_learning_force_and_moment('./test_episode_state_fuzzy_final_new.npy', './test_episode_state_fuzzy_final_new.npy', 'dqn_none_fuzzy')
    # plot_learning_force_and_moment('./test_episode_state_none_fuzzy_final.npy', './test_episode_state_none_fuzzy_final.npy', 'dqn_none_fuzzy')
    # plot_learning_force_and_moment('episode_state_fuzzy_noise.npy', 'episode_state_fuzzy_noise.npy', 'dqn_none_fuzzy')
    # plot_learning_force_and_moment('episode_state_none_fuzzy_noise.npy', 'episode_state_none_fuzzy_noise.npy', 'dqn_fuzzy')

    #####
    # print(np.max(force, axis=0))
    # print(np.min(force, axis=0))
    # print(np.max(state, axis=0))
    # print(np.min(state, axis=0))
    # plot('./search_state.npy')
    # plot('./search_force.npy')

    # reward = np.hstack([reward_1[:49], reward_2[:49], reward_3])
    # reward_1 = np.load('episode_rewards.npy')
    # reward = np.load('episode_steps_none_fuzzy_noise_final.npy')
    # reward = np.hstack([reward_1, reward])
    # plot_reward(reward)