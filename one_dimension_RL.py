import pandas as pd
import random
import time

class oneD_RL :
    def __init__ (self, state_num, actions, epsilon = 0.6, gamma = 0.6, learning_rate = 0.1) :
        self.state_num = state_num
        self.actions = actions
        self.environment = []
        
        self.state = 0
        self.FINDTREASURE = "FINDED"
        self.EPSILON = epsilon
        self.GAMMA = gamma
        self.LEARNINGRATE = learning_rate
        self.EPISODES = 10

        self._initQTable()
        pass
    
    def _initQTable (self) :
        self.qTable = pd.DataFrame(
                            [[0 for i in range(len(self.actions))] for _ in range(self.state_num)],
                            columns = self.actions
                        )

        return self

    def chooseAction (self) :
        action = ''
        stateQ = self.qTable.loc[self.state, : ]

        if random.uniform(0, 1) > self.EPSILON :
            action = random.choice(self.actions)
        
        elif (stateQ == 0).all() :
            action = random.choice(self.actions)

        else :
            action = stateQ.idxmax()

        return action

    def calculateReward (self) :
        reward = 0

        if self.state == self.FINDTREASURE :
            reward = 1

        return reward

    def changeState (self, action) :
        if action in self.actions :
            if action == "left" :
                self.state = self.state - 1 if self.state > 0 else 0

            elif action == "right" :
                self.state = self.state + 1 if self.state < self.state_num else self.state_num

        if self.state == self.state_num :
            self.state = self.FINDTREASURE
        
        return self

    def showEnvironment (self) :
        self.environment = []

        for _ in range(self.state_num) :
            self.environment.append("-")
        self.environment.append("宝")

        self.environment[self.state] = "人"

        print("Environment : \r{}".format(''.join(self.environment)), end = '')
        time.sleep(0.5)

        return self
    
    def updateQTable (self, state_before_action, action, reward) :
        if self.state == self.FINDTREASURE :
            Q_probability_next_state = 0
        
        else :
            Q_probability_next_state = self.qTable.loc[self.state, : ].max()

        self.qTable.loc[state_before_action, action] += self.LEARNINGRATE * (
                                                            reward +
                                                            self.GAMMA * (
                                                                Q_probability_next_state
                                                            ) -
                                                            self.qTable.loc[state_before_action, action]
                                                        )

    def train (self) :
        for episode in range(self.EPISODES) :
            self.state = 0
            step = 0

            print("{} episode {} {}".format("=" * 10, episode, "=" * 10))

            while self.state != self.FINDTREASURE :
                self.showEnvironment()

                step += 1
                state_before_action = self.state

                action = self.chooseAction()

                reward = self.changeState(action).calculateReward()
                
                self.updateQTable(state_before_action, action, reward)

            print("\nEpisode {} : step => {}".format(episode, step))
            print(self.qTable)
            time.sleep(1.5)

if __name__ == "__main__" :
    test = oneD_RL( 7, ["left", "right"], epsilon = 0.9, learning_rate = 0.1)
    test.train()