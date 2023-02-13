# Assignment1 Survailence Robot
# 1. Introduction 
This github repository shows how to build a finit-state machine in ROS environment based on [SMACH](http://wiki.ros.org/smach/Tutorials) ros-package, and how to build a topological onotology of the wrold, in this small project, Protogé is used for building the ontology, [ARMOR](https://github.com/EmaroLab/armor_rds_tutorial) service is used for access and modify the ontology.
#### Environment
 It is a 2D-environmen built up with 4 rooms `R1 R2 R3 R4`, 2 corridors `C1 C2` and one special room `E` used as a waiting room befor filling the map, and a charging station as well. And 7 doors `D1 ... D7`  
 
 #### Senario
 We have a survallience robot that moves in a 2D environment. First the robot waits in room **E** untill the whol map  is loaded into the ontology, then the robot keeps moving between the corridors **C1** and **C2** for infinit time. The robot must go to the charging station **E** when its battery is low, otherwise he must visit the **urgent** rooms if any, then goes back to its normal behavior moving between cooridors.
 
 #### Ontology
* Entity 
* Individuals 
  * `C1 C2 E`: Cooridors 
  * `R1 R2 R3 R4`: Rooms
  * `D1 D2 D3 D4 D5 D6 D7`: Doors
* Object properties
  * isIn
  * canReach
  * hasDoor 
  * connectedTo
* Data properties 
  * Now
  * visitedAt
  * uregencyThreshold
  
  # 2. Discreption of software architecture 
  ![uml](https://github.com/awaistahir29/survailence_robot/blob/main/diagram/Assignment_1.jpg)
  
  The software architecture is buily up by **four nodes**, a **list of parameters** and **two customized messages** they are listed bellow. Each node has a specific task to do:
 1. user_interface
 2. state_machine
 3. battery_controller
 4. armor 
 * List of paramerters
 * List of meesages 
### 1- user_interface 
 This node interact with the user in an infinit loop, allows the user to access and modify the onotology by just entring some specific inputs, then this node call the armor server in the appropriate command. Also this node publish the state of the map in the topic `/battery_state`. It publishes **0** if it is not fully loaded and **1** if it is fully loaded. 
   * The required inputs are: 
     * The type of operation `manipulation, query, utils`
     * The name of operation `ADD, LOAD, ...`
     * The primary_command_spec
     * The secondary_command_spec 
     * The number of arguments 
     * Arguments
     
### 2- state_machine
It controlls how the robot changes its state based on the reasoning of the topological ontology, and the battery state of the robot. This node subscribes to two topics `/battery_state` and `/map_state`, and it calls the armor server for updating the loaded ontology. The states of the robot are listed bellow.
  * filling_map
  * moving_in_corridors
  * visiting_urgent
  
  ### 3- battery_controller 
 This is a publisher to the topic `/baterry_state`, it publishes different state of the battery `True`or`False` in a specific duration, the durations to be full or low are passed as **parameters**.
  ### 4- armor
 The ARMOR package is an external package used to communicate with the Cluedo OWL ontology, it is a ROS wrapper that helps to make this communication possible. For more information about ARMOR [click here](https://github.com/EmaroLab/armor_rds_tutorial)
 ### List of parameters 
 It is a **yaml** file that list all the parameters used in this project which are 
 * time_to_stay_in_location defeault value = 1 (s)
 * time_of_one_charge  defeault value = 30 (s)
 * time_of_charging  defeault value = 15 (s)
 * visitedAt_R1  defeault value = 1665579740
 * visitedAt_R2  defeault value = 1665579740
 * visitedAt_R3  defeault value = 1665579740
 * visitedAt_R4  defeault value = 1665579740
 * visitedAt_C1  defeault value = 1665579740
 * visitedAt_C2  defeault value = 1665579740
 * visitedAt_E  defeault value = 1665579740
### List of messages 
* Map_state.msg: `int32 map_state`, carry the state of the map
  * It is 1 if the map is fully loaded 
  * It is 0 if the map is not fully loaded
* Battry_state.msg: `int32 battery_state`, carry the state of the battery
  * It is 1 if the battery is full
  * It is 0 if the battery is low
  
  There are four states in this state diagram, the task of each state is explained below:
1. **MapLoading**: The robots keeps waiting in room **E** untill the whole map is loaded, the robot can know if the map is fully loaded by subscribing to the topic `/map_state`. When the map is fully loaded the robot go to `MOVING_IN_CORRIDORS` state trough the transition `move`.
2. **Normal**: The robots keeps moving between `C1` and `C2` for infinit time, the robots keep cheking the state of the battery by subscribing to the topic `/battery_state`, if the battery is `low` the robot goes to `CHARGING` state trough the transition `tired`. if the battery is not low, the robot cheks if there is an `urgent` room by quering the `individuals of the class urg`. If there is an urgent room the robot goes to `VISITING_URGENT` state through the transition `urgent`.
3. **Visiting_urgent**:  First, the robots checks if the battery is low goes to `CHARGING` state, else it checkes it the urgent room is reacheable by quering the object properties of the robot `canReach`, if the room can be reached it visit it and return back to the `MOVING_IN_CORRIDORS` trough the transition `visited`. If the urgent room is not reacheable it goes to `MOVING_IN_CORRIDORS` state through the transition `not_reached`, in this case the robot will change the corridors and visit it again.
4. **Battery Low**: The robot keeps checking the state of the battery, if it is full it goes to `MOVING_IN_COORIDORS` state the the transition `charged`, otherwise, it stays in the `CHARGING` state. 

# 3. Instalation and running procedures
1. Clone the repository in your work_space `git clone https://github.com/awaistahir29/survailence_robot.git`
2. (optional!) Change the other parameters if you want to test some relevent parts of the code
3. If you do not have [smach_package](http://wiki.ros.org/smach/Tutorials/Getting%20Started), run this command:
 `sudo apt-get install ros-noetic-smach-ros`
4. If you do not have armor installed, follow this git hub repository 
`https://github.com/EmaroLab/armor_rds_tutorial.git`
5. Open new terminal and run `roslaunch assignment solution.launch`
* When you run this command, three windows and the should pop-up
  1. user_interface.py
  2. state_machine.py
  3. battery.py
  * user_inerface.py: allows you to load the ontology, and notify the algorithm if the map is fully loaded
  * state_machine.py: prints the state transition of the robot, helps you to understand and debug 
  * battery.py: allows you to monitor the state of the better
  * charging
  
  # 5. Working hypothesis and environement
In this project there are many assumptions made on the environement in order to make the project simpler, the assumptions are explained bellow
1. The movement of the robot is not performed in real world, so if we make a simulation we will not see the robot moving. The movements is performed only on the level of onotology. A movement is defined by changing the location of the robot by `isIn`, and updating the time `now`.
2. Initializing the `visitedAt` data proporty of a location to different values to avoid making all of them **urgent** at the same time 
3. When a robot is in a specific location, it can reach only the locations that need **one door** transmition


## Pssible Limitations
1. "The time to do a move" and "the time to stay in a location" and "the time step to be updated" is considered to be the same, and it is passed as a parameter to the code by the parameter `time_to_stay_in_location`
2. The robot does not move it there is a missing part in the map, this is not practical, because in real life if we have a person in the same situation, the persone starts moving and discouvering the environment by himself, and starts acting even if he does not know the whole environment 
## Possible improvements
1. The movement can be improved by consediring a real motion in cartesian space, this is can be done by including the `planer` and `controller` nodes in the architecture. for more information about planer and controller nodes visit this [repository](https://github.com/buoncubi/arch_skeleton.git)  
2. The time can be continuously updated and depends on the distance and speed of the robot to reach a specific location
3. Make the robot willing to move by knowing just its current position and how he can reach another position and building the map by itself

# 7. Author and Teachers contacts 
* Author 
  * name: Awais Tahir
  * email: awaistahir29@gmail.com
* Teachers
  * name: Luca Buoncompagni luca.buoncompagni@edu.unige.it
  * name: Carmine Recchiuto carmine.recchiuto@dibris.unige.it
