from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket
from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3 
from utils.dodge import *
from objects import agent

class kickoff():

    def __init__(self, packet):
        self.my_car = packet.game_cars[self.index]
        self.car_location = Vec3(self.my_car.physics.location)
        self.car_velocity = Vec3(self.my_car.physics.velocity)
        self.ball_location = Vec3(packet.game_ball.physics.location)
        
    def run(self, packet):
        global controls
        if self.car_location.z > 1600:
            airborne = True
        else:
            airborne = False
        if not airborne:   
            controls.boost = True
            controls.throttle = 1.0
        controls = SimpleControllerState()
                     
    def select_kickoff(self, packet):
        if self.car_location == Vec3(-2048, -2560, self.car_location.z):
            self.front_diagonal_right()
        elif self.car_location == Vec3(2048, -2560, self.car_location.z):
            self.front_diagonal_left()
        elif self.car_location == Vec3(-256.0, -3840, self.car_location.z):
            self.back_diagonal_right()
        elif self.car_location == Vec3(256.0, -3840, self.car_location.z):
            self.back_diagonal_left()
        elif self.car_location == Vec3(0.0, -4608, self.car_location.z):
            self.straight_kickoff()


    def straight_kickoff(self, packet):
        if self.car_location.x == 0 and self.car_velocity == 900:
            self.front_flip()
        if (self.car_location - self.ball_location).magnitude() < 400:
            self.front_flip()

    def front_diagonal_right(self, packet):   
        if (self.car_location - self.ball_location).magnitude() < 500:
            self.diagonal_flip_right()

    def front_diagonal_left(self, packet):   
        if (self.car_location - self.ball_location).magnitude() < 500:
            self.diagonal_flip_left()

    def back_diagonal_left(self, packet):
        if agent.team_color == 'blue':
            target_location = Vec3(0.0, -2816.0, 70.0)
            while self.car_location.y < target_location.y:
                controls.steer = steer_toward_target(self.my_car, target_location)
                continue
            
            target_location = self.ball_location
            controls.steer = steer_toward_target(self.my_car, target_location)
            self.diagonal_flip_left()
            if (self.car_location - self.ball_location).magnitude() < 400:
                self.front_flip()
                
        if agent.team_color == 'orange':
            target_location = Vec3(0.0, 2816.0, 70.0)
            while self.car_location.y > target_location.y:
                controls.steer = steer_toward_target(self.my_car, target_location)
                continue
            
            target_location = self.ball_location
            controls.steer = steer_toward_target(self.my_car, target_location)
            self.diagonal_flip_left()
            if (self.car_location - self.ball_location).magnitude() < 400:
                self.front_flip()

    def back_diagonal_right(self, packet):
        if agent.team_color == 'blue':
            target_location = Vec3(0.0, -2816.0, 70.0)
            while self.car_location.y < target_location.y:
                controls.steer = steer_toward_target(self.my_car, target_location)
                continue
            
            target_location = self.ball_location
            controls.steer = steer_toward_target(self.my_car, target_location)
            self.diagonal_flip_right()
            if (self.car_location - self.ball_location).magnitude() < 400:

                self.front_flip()

        else:

            target_location = Vec3(0.0, 2816.0, 70.0)
            while self.car_location.y < target_location.y:
                controls.steer = steer_toward_target(self.my_car, target_location)
                continue
            
            target_location = self.ball_location
            controls.steer = steer_toward_target(self.my_car, target_location)
            self.diagonal_flip_right()
            if (self.car_location - self.ball_location).magnitude() < 400:

                self.front_flip()
    