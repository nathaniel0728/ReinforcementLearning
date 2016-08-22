'''
    rudimentary concepts of reinforcement learning
    n-bandits problem
    nathaniel choe
'''

import random
import math


def create_q_actual(arms, variance):
    
    array = [0.0] * arms
    for ite in range(arms):
        array[ite] = random.uniform(-variance, variance)
    
    return array


def stationary_bandit(arms, plays, initial, variance, epsilon, alpha):
    
    q_actual = create_q_actual(arms, variance)
    q_estimate = [initial] * arms
    guesses = []

    for play in range(plays):
        
        max_index = 0
        
        #greedy
        if random.random() > epsilon:
            if play == 0:
                max_index = (int)(random.random() * arms)
            else:
                max_index = q_estimate.index(max(q_estimate))
            guesses.append(q_actual[max_index])
            
        #epsilon-greedy
        else:
            max_index = (int)(random.random() * arms)
            guesses.append(q_actual[max_index])
        
        q_c = q_estimate[max_index]
        q_estimate[max_index] = q_c + alpha * (q_actual[max_index] - q_c)
    
    return (sum(guesses) / plays)

def init(arms, plays, iterations):
    
    variance = 1.0
    initial = 0.0 - variance
    epsilon = 0.0
    alpha = 0.8
    

    data = []
    print(arms,"-bandits problem with ",plays," plays - averaged over ", iterations)
    epsilon = 0.0
    print("average w/ epsilon: ",epsilon)
    for i in range(iterations):
        data.append(stationary_bandit(arms, plays, initial, variance, epsilon, alpha))
    print(sum(data) / iterations)
    
    data = []
    print(arms,"-bandits problem with ",plays," plays - averaged over ", iterations)
    initial = 5.0
    print("average w/ epsilon: ",epsilon,", optimistic initial", initial)
    for i in range(iterations):
        data.append(stationary_bandit(arms, plays, initial, variance, epsilon, alpha))
    print(sum(data) / iterations)

    data = []
    epsilon = 0.1
    print("average w/ epsilon: ",epsilon)
    for i in range(iterations):
        data.append(stationary_bandit(arms, plays, initial, variance, epsilon, alpha))
    print(sum(data) / iterations)
    

init(100, 10000, 200)

