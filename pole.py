import gym
import tensorflow as tf
import random
import numpy as np

env = gym.make("CartPole-v0")
env.reset()

def learn():

    inputs1 = tf.placeholder(shape=[1, 4], dtype=tf.float32)
    W = tf.Variable(tf.random_uniform([4, 2], 0, 0.01))
    Qout = tf.matmul(inputs1, W)
    predict = tf.argmax(Qout, 1)

    nextQ = tf.placeholder(shape=[1,2], dtype=tf.float32)
    loss = tf.reduce_sum(tf.square(nextQ-Qout))
    trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
    updateModel = trainer.minimize(loss)

    init = tf.initialize_all_variables()
    
    
    lr = 0.55
    y = 0.99
    e = 0.1
    num_episodes = 1000
    trials = 999
    
    with tf.Session() as sess:
        sess.run(init)
        for i in range(num_episodes):
            rAll = 0
            d = False
            j = 0
            
            s = []
            ts = env.reset()
            s.append(ts)
            s = np.asarray(s)
            np.around(s, decimals=2)

            while j < trials:
                j += 1
                a,allQ = sess.run([predict, Qout], feed_dict={inputs1:np.asarray(s)})
                
                if random.random() < e:
                    #predict is a 1x1 array with an action...
                    ran = random.random()
                    if ran < 0.5:
                        a[0] = 0
                    else:
                        a[0] = 1
                
                ts1, r, d, _ = env.step(a[0])
                #if d:
                #    r = -50

                s1 = []
                s1.append(ts1)
                s1 = np.asarray(s1)
                np.around(s1, decimals=2)
                
                Q1 = sess.run(Qout, feed_dict={inputs1:s1})
                maxQ1 = np.max(Q1)
                targetQ = allQ 
                
                #targetQ is 1x4 array in a 1x1 array...
                targetQ[0, a[0]] = targetQ[0, a[0]] + lr * (r + y*maxQ1 - targetQ[0, a[0]])
                
                _, W1 = sess.run([updateModel, W], feed_dict={inputs1:s1, nextQ:targetQ})

                rAll += r
                s = s1
                if d == True:
                    e = 1./((i/50) + 10)
                    break        
            
            #exit()

        ts = env.reset()
        s = []
        s.append(ts)
        s = np.asarray(s)
        np.around(s, decimals=2)
        rTotal = 0
        for _ in range(1000):
            env.render()
            a = sess.run(predict, feed_dict={inputs1:s})
            if a[0] == 0:
                a = 0
            else:
                a = 1
            ts1, r, d, _ = env.step(a)
            rTotal += r
            if d:   
                print("RESET", rTotal)
                ts = env.reset()
                s = []
                s.append(ts)
                s = np.asarray(s)
                _ = 0
                rTotal = 0

            s1 = []
            s1.append(ts1)
            s1 = np.asarray(s1)
            np.around(s1, decimals=2)
            s = s1



learn()
