#!/usr/bin/env python3

import roslib
import rospy
import smach
import smach_ros
import time
import random
import re
import sys

from armor_api.armor_client import ArmorClient
urgency = False


def user_action():
    return random.choice(['discharged','timeup','charged','loaded','relaxed'])

# define state Unlocked
class Map_Receiving(smach.State):
    def __init__(self):
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['loaded'])
                             #input_keys=['unlocked_counter_in'],
                             #output_keys=['unlocked_counter_out'])
        
        self.client1 = ArmorClient('example', 'ontoRef')

    def execute(self, userdata):
        # function called when exiting from the node, it can be blccking
        self.client1.utils.load_ref_from_file('/home/awais/my_ros_ws/src/survailence_robot/map/topological_map_abox_new.owl', 
                                'http://bnc/exp-rob-lab/2022-23', 
                                buffered_manipulation=True, 
                                reasoner='PELLET', 
                                buffered_reasoner=True, 
                                mounted=False)

        #client1.query.check_ind_exists('C1')
        self.client1.manipulation.add_ind_to_class('C1', 'CORRIDOR')
        self.client1.manipulation.add_ind_to_class('C2', 'CORRIDOR')
        self.client1.manipulation.add_ind_to_class('D1', 'DOOR')
        self.client1.manipulation.add_ind_to_class('D2', 'DOOR')
        self.client1.manipulation.add_ind_to_class('D3', 'DOOR')
        self.client1.manipulation.add_ind_to_class('D4', 'DOOR')
        self.client1.manipulation.add_ind_to_class('D5', 'DOOR')
        self.client1.manipulation.add_ind_to_class('D6', 'DOOR')
        self.client1.manipulation.add_ind_to_class('D7', 'DOOR')
        self.client1.manipulation.add_ind_to_class('E1', 'ROOM')
        self.client1.manipulation.add_ind_to_class('ROBOT1', 'ROBOT')

        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C1', 'D6')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C1', 'D5')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C1', 'D2')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C1', 'D1')

        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C2', 'D5')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C2', 'D3')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C2', 'D4')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'C2', 'D7')

        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'E', 'D7')
        self.client1.manipulation.add_objectprop_to_ind('hasDoor', 'E', 'D6')

        self.client1.manipulation.add_objectprop_to_ind('isIn', 'Robot1', 'C1')
        
        self.client1.call('DISJOINT', 'IND', '', ['E','C1','C2','R1','R2','R3','R4','D1','D2','D3','D4','D5','D6','D7'])

        time1 = str(int(time.time()))

        # Add time
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','E', 'Long', time1)
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','C1', 'Long', time1)
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','C2', 'Long', time1)
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','R1', 'Long', time1)
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','R2', 'Long', time1)
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','R3', 'Long', time1)
        self.client1.manipulation.add_dataprop_to_ind('visitedAt','R4', 'Long', time1)

        res = self.client1.call('REASON', '', '', '')
        print("Response : ", res)

        if res.is_consistent == True:
            print("Successfully Received the Map\n")
            print("Replacing Visited At with Now()\n")
            now = self.client1.query.dataprop_b2_ind('now', 'Robot1')
            #print("Now Value of robot is: ", now)
            new_list = []
            for string in now:
                new_list.append(re.search('"' + '(.+?)'+'"', string).group(1))
                print('The current Now value is: ', new_list)
            ret = self.client1.manipulation.replace_dataprop_b2_ind('now', 'Robot1', 'Long', str(int(time.time())), new_list[0])
            res = self.client1.call('REASON', '', '', '')
            if ret == True:
                print("Replaced")

            now1 = self.client1.query.dataprop_b2_ind('now', 'Robot1')
            #print("New now Value of robot is: ", now1)
            #print("The VisitedAt of E is: ", now2)
            new_list1 = []
            for string in now1:
                new_list1.append(re.search('"' + '(.+?)'+'"', string).group(1))
                print('The new Now value is: ', new_list1)

            now2 = self.client1.query.dataprop_b2_ind('visitedAt', 'E')
            #print("The current VisitedAt of E is: ", now2)
            new_list2 = []
            for string in now2:
                new_list2.append(re.search('"' + '(.+?)'+'"', string).group(1))
                print('The current VisitedAT is: ', new_list2)

            ret1 = self.client1.manipulation.replace_dataprop_b2_ind('visitedAt', 'E', 'Long', new_list1[0], new_list2[0])
            res = self.client1.call('REASON', '', '', '')
            if ret1 == True:
                print("Replaced Visited at of E with new Now")
            #rospy.sleep(5)
            #rospy.loginfo('Executing state UNLOCKED (users = %f)'%userdata.unlocked_counter_in)
            #userdata.unlocked_counter_out = userdata.unlocked_counter_in + 1
            #return user_action()
            return 'loaded'

# define state Locked
class Normal(smach.State):
    def __init__(self):
        #self._helper = helper
        smach.State.__init__(self, 
                             outcomes=['discharged','timeup','charged','loaded','relaxed'])
                            #input_keys=['locked_counter_in'],
                            # output_keys=['locked_counter_out'])
        #self.sensor_input = 0
        
        self.rate = rospy.Rate(200)  # Loop at 200 Hz
        self.client1 = ArmorClient('example', 'ontoRef')

    def execute(self, userdata):
        # simulate that we have to get 5 data samples to compute the outcome
        return 'timeup'

# define state Locked
class Urgent(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['relaxed','discharged','timeup'])
                            # input_keys=['locked_counter_in'],
                            # output_keys=['locked_counter_out'])
        #self.sensor_input = 0
        self.rate = rospy.Rate(200)  # Loop at 200 Hz
        self.client1 = ArmorClient('example', 'ontoRef')

    def execute(self, userdata):
        # simulate that we have to get 5 data samples to compute the outcome
        return 'relaxed'

# define state Locked
class Battery_Low(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['charged','discharged'])
                             #input_keys=['locked_counter_in'],
                             #output_keys=['locked_counter_out'])
        #self.sensor_input = 0
        self.client1 = ArmorClient('example', 'ontoRef')
        self.rate = rospy.Rate(200)  # Loop at 200 Hz


    def execute(self, userdata):
        # simulate that we have to get 5 data samples to compute the outcome
        return 'charged'

        
def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])
    sm.userdata.sm_counter = 0

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('MAP_RECEIVING', Map_Receiving(),
                               transitions={'loaded':'NORMAL'})
                               #remapping={'locked_counter_in':'sm_counter', 
                               #           'locked_counter_out':'sm_counter'})
        smach.StateMachine.add('NORMAL', Normal(), 
                               transitions={'timeup':'URGENT',
                                            'discharged':'BATTERY_LOW',
                                            'charged':'NORMAL', 
                                            'loaded':'NORMAL',
                                            'relaxed':'NORMAL'})
                               #remapping={'unlocked_counter_in':'sm_counter',
                               #           'unlocked_counter_out':'sm_counter'})
        smach.StateMachine.add('URGENT', Urgent(), 
                               transitions={'relaxed':'NORMAL',
                                            'discharged':'BATTERY_LOW',
                                            'timeup':'URGENT'})
                               #remapping={'locked_counter_in':'sm_counter', 
                               #           'locked_counter_out':'sm_counter'})
        smach.StateMachine.add('BATTERY_LOW', Battery_Low(), 
                               transitions={'charged':'NORMAL',
                                            'discharged':'BATTERY_LOW'})
                               #remapping={'unlocked_counter_in':'sm_counter',
                               #           'unlocked_counter_out':'sm_counter'})


    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
