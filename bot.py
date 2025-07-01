from command import Command
import numpy as np
from buttons import Buttons
import joblib  
import pandas as pd  
import random 

VERTICAL_ACTION_THRESHOLD = 0.5 # restricts vertical movement 
HORIZONTAL_ACTION_THRESHOLD = 0.1 # encourages horizontal movement due to lower probability

class Bot:

    def __init__(self):
        self.my_command = Command()
        self.buttn = Buttons() 
        try:
            # these files are in the same directory as bot.py e.g /PythonAPI/
            self.model = joblib.load("sf_model.joblib")
            self.feature_columns = joblib.load("sf_features.joblib")
            print("ML Model loaded successfully from PythonAPI directory.")
        except FileNotFoundError:
            print("ERROR: Model files (sf_model.joblib or sf_features.joblib) not found in PythonAPI directory.")
            self.model = None
            self.feature_columns = None
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.feature_columns = None

    def fight(self, current_game_state, player_to_control):  # player_to_control is "1" or "2"
        if not self.model or not self.feature_columns:
            # sanity check, if model not loaded, return a command with no buttons pressed
            self.buttn = Buttons() 
            if player_to_control == "1":
                self.my_command.player_buttons = self.buttn
            elif player_to_control == "2":
                self.my_command.player2_buttons = self.buttn
            return self.my_command

        # which player is 'self' (the one being controlled by the bot) and which is the 'opponent'
        # as the model was trained from Player 1's perspective.
        if player_to_control == "1":
            p_self = current_game_state.player1
            p_opponent = current_game_state.player2
        elif player_to_control == "2":
            p_self = current_game_state.player2  # Bot controls P2, so P2 is 'self' for the model's "Player1" features
            p_opponent = current_game_state.player1  # P1 is 'opponent' for the model's "Player2" features
        else:
            print(f"Error: Invalid player_to_control argument: {player_to_control}")
            self.buttn = Buttons()  # Reset buttons
            # defaulting
            self.my_command.player_buttons = self.buttn
            return self.my_command

        # features
        current_features_dict = {
            'timer': current_game_state.timer,
            'has_round_started': int(current_game_state.has_round_started),
            'is_round_over': int(current_game_state.is_round_over),

            # Features for 'p_self' i-e which model will see as Player 1
            'Player1_ID': p_self.player_id,
            'health': p_self.health,  
            'x_coord': p_self.x_coord,  
            'y_coord': p_self.y_coord,  
            'is_jumping': int(p_self.is_jumping), 
            'is_crouching': int(p_self.is_crouching),  
            'is_player_in_move': int(p_self.is_player_in_move),  
            'move_id': p_self.move_id, 

            # Features for 'p_opponent' i-e which model sees as Player 2
            'Player2_ID': p_opponent.player_id,
            'Player2 health': p_opponent.health, 
            'Player2 x_coord': p_opponent.x_coord, 
            'Player2 y_coord': p_opponent.y_coord, 
            'Player2 is_jumping': int(p_opponent.is_jumping),  
            'Player2 is_crouching': int(p_opponent.is_crouching), 
            'Player2 is_player_in_move': int(p_opponent.is_player_in_move),  
            'Player2 move_id': p_opponent.move_id 
        }

        # feature vector
        try:
            input_feature_vector = [current_features_dict[fc_name] for fc_name in self.feature_columns]
        except KeyError as e:
            print(f"FATAL ERROR: A feature expected by the model was not found in current_features_dict: {e}")
            print(f"Expected features by model (from sf_features.joblib): {self.feature_columns}")
            print(f"Constructed current_features_dict keys: {list(current_features_dict.keys())}")
            # defaulting / sanity check
            self.buttn = Buttons()  # Reset buttons
            if player_to_control == "1":
                self.my_command.player_buttons = self.buttn
            elif player_to_control == "2":
                self.my_command.player2_buttons = self.buttn
            return self.my_command

        model_input_df = pd.DataFrame([input_feature_vector], columns=self.feature_columns)
        # getting probabilities for each action
        predicted_probabilities_list = self.model.predict_proba(model_input_df)
        prob_up = predicted_probabilities_list[0][0, 1]  # Prob of 'up' being true
        prob_down = predicted_probabilities_list[1][0, 1] # Prob of 'down' being true   
        prob_right = predicted_probabilities_list[2][0, 1]# Prob of 'right' being true
        prob_left = predicted_probabilities_list[3][0, 1] # Prob of 'left' being true
        
        print(f"Frame {current_game_state.timer}: Model Predicted Probabilities (Up, Down, Right, Left): "
              f"Up={prob_up:.4f}, Down={prob_down:.4f}, Right={prob_right:.4f}, Left={prob_left:.4f}")

        # what keys to press based on the probabilities and thresholds
        up_active = prob_up > VERTICAL_ACTION_THRESHOLD
        down_active = prob_down > VERTICAL_ACTION_THRESHOLD
        left_active = prob_left > HORIZONTAL_ACTION_THRESHOLD
        right_active = prob_right > HORIZONTAL_ACTION_THRESHOLD

        # if left and right are both active, choose one based on the probabilities
        # otherwise we don't move if both are active
        if left_active and right_active:
            if prob_left > prob_right:
                self.buttn.left = True
                self.buttn.right = False
            elif prob_right > prob_left:
                self.buttn.left = False
                self.buttn.right = True
            else: # equal probs so just set both to false
                self.buttn.left = False
                self.buttn.right = False
        else:
            # numpy bool was causing issues with the command so convert to python bool
            self.buttn.left = bool(left_active)  
            self.buttn.right = bool(right_active) 

        # if up and down are both active, choose one based on the probabilities
        # otherwise we don't move if both are active
        if up_active and down_active:
            if prob_up > prob_down:
                self.buttn.up = True
                self.buttn.down = False
            elif prob_down > prob_up:
                self.buttn.up = False
                self.buttn.down = True
            else: # equal probs so just set both to false
                self.buttn.up = False
                self.buttn.down = False
        else:
            # same as above, convert to python bool
            self.buttn.up = bool(up_active)  
            self.buttn.down = bool(down_active)
        

        is_making_directional_move = self.buttn.up or self.buttn.down or self.buttn.left or self.buttn.right
        if is_making_directional_move:
            action_button_probability = 0.1
        else:
            action_button_probability = 0.2 # more likely to press action buttons when not moving
        
        # action buttons (A, B, X, Y, L, R)
        self.buttn.A = random.random() < action_button_probability
        self.buttn.B = random.random() < action_button_probability
        self.buttn.X = random.random() < action_button_probability
        self.buttn.Y = random.random() < action_button_probability
        self.buttn.L = random.random() < action_button_probability
        self.buttn.R = random.random() < action_button_probability

        # remaining buttons
        self.buttn.select = False
        self.buttn.start = False

        print(f"Frame {current_game_state.timer}: Final Bot Actions: "
              f"Up={self.buttn.up}, Down={self.buttn.down}, Left={self.buttn.left}, Right={self.buttn.right}, "
              f"A={self.buttn.A}, B={self.buttn.B}, X={self.buttn.X}, Y={self.buttn.Y}, "
              f"L={self.buttn.L}, R={self.buttn.R}, Select={self.buttn.select}, Start={self.buttn.start}")

        # assigning buttons to the correct player in the command
        if player_to_control == "1":
            self.my_command.player_buttons = self.buttn
        elif player_to_control == "2":
            self.my_command.player2_buttons = self.buttn

        return self.my_command