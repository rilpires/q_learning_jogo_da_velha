
import random
import json
import sys
import os

class LearningAgent():

    def __init__(self , actions , alpha , discount_factor , parameters_file="params.json" ):
        self.Q = {}
        if( os.path.exists(parameters_file) ):
            self.Q = json.load(open(parameters_file))
        self.all_actions = actions
        self.alpha = alpha
        self.discount_factor = discount_factor
        self.last_action = None
        self.last_state = None
        self.need_feedback = False
    
    def estimate_next_play( self , S , exploration_probability=0.2):
        self.last_state = S.copy()
        if( self.need_feedback ):
            print("Warning: LearningAgent needs feedback for last estimated play!")
        self.need_feedback = True
        # Se está em um estado desconhecido, retorna uma ação aleatória
        if not str(S) in self.Q:
            new_q = {}
            for action in self.all_actions:
                new_q[action] = 0
            self.Q[ str(S) ] = new_q
            random_action = self.all_actions[ random.randint(0,len(self.all_actions)-1) ]
            self.last_action = random_action
            return random_action
        
        # Se está em um estado conhecido, decide se explora ou toma melhor ação conhecida
        else:
            # Exploration
            if random.random() < exploration_probability:
                random_action = self.all_actions[ random.randint(0,len(self.all_actions)-1) ]
                self.last_action = random_action
                return random_action

            # Exploitation
            else:
                best_action = None
                best_value = None
                for action in self.all_actions:
                    if best_action == None or self.Q[str(S)][action] > best_value:
                        best_value = self.Q[str(S)][action]
                        best_action = action
                self.last_action = best_action
                return best_action 

    def feedback( self , new_state , reward ):
        if( self.need_feedback == False ):
            print("Warning! feedbacking 2 or mores times in a row for the same action")
        self.need_feedback = False

        Q = self.Q
        s1 = str(self.last_state)
        s2 = str(new_state)
        last_action = self.last_action

        if not str(new_state) in Q:
            new_Q = {}
            for action in self.all_actions:
                new_Q[action] = 0
            Q[str(new_state)] = new_Q

        best_from_new_state = None
        for action in self.all_actions:
            if best_from_new_state == None or self.Q[s2][action] > best_from_new_state:
                best_from_new_state = Q[s2][action]
        self.Q[s1][last_action] = Q[s1][last_action]*(1-self.alpha) + self.alpha*( reward + self.discount_factor*best_from_new_state )
        
    def save_params( self , file_name="params.json"):
        json.dump(self.Q,open(file_name,mode="w"))


