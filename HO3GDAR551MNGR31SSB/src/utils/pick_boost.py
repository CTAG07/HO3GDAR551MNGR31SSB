from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.ball_prediction_analysis import find_slice_at_time
from util.boost_pad_tracker import BoostPadTracker
from util.drive import steer_toward_target
from util.sequence import Sequence, ControlStep
from util.vec import Vec3 
Vector3 = Vec3

class goto_boost():
    #very similar to goto() but designed for grabbing boost
    #if a target is provided the bot will try to be facing the target as it passes over the boost
    def __init__(self,boost,target=None):
        self.boost = boost
        self.target = target
        
    def run(self,agent):
        car_to_boost = self.boost.location - agent.me.location
        distance_remaining = car_to_boost.flatten().magnitude()

        agent.line(self.boost.location - Vector3(0,0,500),self.boost.location + Vector3(0,0,500),[0,255,0])

             
