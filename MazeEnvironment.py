import random
import numpy as np

class MazeEnvironment:
    
    maze = []
    size = 0
    holes = 0

    def __init__(self, size, holes):
        
        self.size = size
        self.holes = holes
        self.initialize_maze()
        self.initialize_holes()
    
    def get_size(self):
        return self.size
    
    def get_maze(self):
        return self.maze

    def get_holes(self):
        return self.holes
    
    def initialize_maze(self):
        
        self.maze = ["F"]*(self.size**2)
        self.maze[0] = "S"
        self.maze[self.size**2-1] = "E"
    
    def initialize_holes(self):
        
        counter = 0
        while counter < self.holes:
            pos = (int)(random.random() * (self.size**2))
            if self.maze[pos] == "F" and pos != 0 and pos != (self.size**2 - 1):
                self.maze[pos] = "H"
                counter += 1
    

    def calculate_next_state(self, s, a):
        
        s1 = 0

        if a == 0: #up
            if s/self.size != 0:
                s1 = s - self.size
        elif a == 1: #right
            if s%self.size != self.size-1:
                s1 = s + 1
        elif a == 2: #down
            if s/self.size != self.size-1:    
                s1 = s + self.size
        elif a == 3: #left
            if s%self.size != 0:
                s1 = s - 1
        
        return s1

           

    def step(self, s, a):
        
        s1 = self.calculate_next_state(s, a)
        
        r = -1
        d = False

        if self.maze[s1] == "H":
            r = -1 
            d = True
        elif self.maze[s1] == "F":
            r = 0
            d = False
        elif self.maze[s1] == "E":
            r = 1
            d = True

        return s1, r, d 

   
    def display_maze(self):
        
        s = ""
        for i in range(self.size*self.size):
            if i == 0:
                s = s + self.maze[i] + " "
            elif i % self.size == self.size - 1:
                s = s + self.maze[i] + "\n"
            else:
                s += self.maze[i] + " "
        print(s)

    def play_maze(self, Q):
        
        s = 0
        for i in range(99):
            self.display_maze()
            a = np.argmax(Q[s, :])
            print("Current State: ", s, "Action: ", a)
            s1 = self.calculate_next_state(s, a)
            print("Current State: ", s1)
            s = s1
            if s == self.size*self.size-1:
                break


            
