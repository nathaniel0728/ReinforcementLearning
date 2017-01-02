import gym
import numpy as np
import random
import math

import numpy as np
import tensorflow as tf

#env = gym.make("FrozenLake-v0")
#env = gym.make("CartPole-v0")

#Q = np.zeros([env.observation_space.n, env.action_space.n])
#Q = np.random.rand(env.observation_space.n, env.action_space.n)

rList = []

def calculate_next_state(s, a, size):
    
    s1 = 0

    if a == 0: #up
        if s/size != 0:
            s1 = s - size
    elif a == 1: #right
        if s%size != size-1:
            s1 = s + 1
    elif a == 2: #down
        if s/size != size-1:    
            s1 = s + size
    elif a == 3: #left
        if s%size != 0:
            s1 = s - 1
    return s1

def step(s, a, maze):
    
    s1 = calculate_next_state(s, a, (int)(math.pow(len(maze), 0.5)))
    
    r = -1
    d = False

    if maze[s1] == "H":
        r = -50 
        d = True
    elif maze[s1] == "F":
        r = -1
        d = False
    elif maze[s1] == "G":
        r = 5
        d = True

    return s1, r, d 


def create_maze(size, hole):
    maze = [0] * (size*size)
    
    for i in range(size*size):
        if i==0:
            maze[i] = "S"
        elif i==(size*size-1):
            maze[i] = "G"
        else:
            maze[i] = "F"

    hole_c_l = []
    hole_c = 0

    while hole_c < hole:
        pos = (int)(random.random()*(size*size))
        if pos not in hole_c_l and pos != 0 and pos != (size*size-1):
            hole_c_l.append(pos)
            maze[pos] = "H"
            hole_c += 1

    return maze

def display_maze(maze, size):
    s = ""
    for i in range(size*size):
        if i == 0:
            s = s + maze[i] + " "
        elif i % size == size - 1:
            s = s + maze[i] + "\n"
        else:
            s += maze[i] + " "
    print(s)

def play_maze(maze, Q, size):
    
    s = 0
    
    for i in range(99):
        display_maze(maze, size)
        a = np.argmax(Q[s, :])
        print("Current State: ", s, "Action: ", a)
        s1 = calculate_next_state(s, a, size)
        print("Current State: ", s1)
        s = s1
        if s == size*size-1:
            break


def learn(size, holes, maze):

    m = create_maze(size, holes)
    Q = np.zeros([size*size, 4])
    
    lr = 0.85
    y = 0.99
    e = 0.5
    num_episodes = 50000
    trials = 199

    for i in range(num_episodes):
        #s = env.reset()
        rAll = 0
        d = False
        j = 0
        s = 0
        while j < trials:
            j += 1
            if random.random() < e:
                a = random.randint(0, 3)
            else:
                a = np.argmax(Q[s, :])
            
            #s1, r, d, _ = env.step(a)
            s1, r, d = step(s, a, maze)
            
            Q[s, a] = Q[s, a] + lr*(r + y*np.max(Q[s1,:]) - Q[s, a])
            rAll += r
            s = s1
            if d == True:
                break
        e = 0.5 / (i + 1)
        rList.append(rAll)

    return Q

def nn_learn(size, holes, maze):
    
    inputs1 = tf.placeholder(shape=[1, size * size], dtype=tf.float32)
    W = tf.Variable(tf.random_uniform([size * size, 4], 0, 0.01))
    Qout = tf.matmul(inputs1, W)
    predict = tf.argmax(Qout, 1)

    nextQ = tf.placeholder(shape=[1,4], dtype=tf.float32)
    loss = tf.reduce_sum(tf.square(nextQ-Qout))
    trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
    updateModel = trainer.minimize(loss)

    init = tf.initialize_all_variables()
    
    
    lr = 0.85
    y = 0.99
    e = 0.5
    num_episodes = 500
    trials = 99
    
    with tf.Session() as sess:
        sess.run(init)
        for i in range(num_episodes):
            s = 0
            rAll = 0
            d = False
            j = 0
            while j < trials:
                j += 1
                a,allQ = sess.run([predict, Qout], feed_dict={inputs1:np.identity(size*size)[s:s+1]})
                if random.random() < e:
                    #predict is a 1x1 array with an action...
                    a[0] = (int)(random.random()*4)
                s1, r, d = step(s, a[0], maze)
                Q1 = sess.run(Qout, feed_dict={inputs1:np.identity(size*size)[s1:s1+1]})
                maxQ1 = np.max(Q1)
                targetQ = allQ  
                #targetQ is 1x4 array in a 1x1 array...
                targetQ[0, a[0]] = targetQ[0, a[0]] + lr * (r + y*maxQ1 - targetQ[0, a[0]])
                #lr = 1? original equation:
                # q(s, a) = q(s, a) + lr[r + y * max q(s',a') - q(s, a)]
                
                _, W1 = sess.run([updateModel, W], feed_dict={inputs1:np.identity(size*size)[s:s+1], nextQ:targetQ})
                rAll += r
                s = s1
                if d == True:
                    e = 1./((i/50) + 10)
                    break        
     
        Q = []
        for i in range(size*size):
            aTotal = sess.run(Qout, feed_dict={inputs1:np.identity(size*size)[i:i+1]})
            QT = []
            for j in aTotal[0]:
                QT.append(j)
            Q.append(QT)
        Q = np.asarray(Q)
        return Q

size = 10
holes = 10

m = create_maze(size, holes)
#Q = learn(size, holes, m)
Q = nn_learn(size, holes, m)
#print(Q)
play_maze(m, Q, size)






