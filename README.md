
# Autonomous Warehouse Robot Simulation
## Menna Emad Al ghorra / 120220620

An interactive 2D simulation of Autonomous Mobile Robots (AMRs) operating in a grid-based warehouse environment. The system models task scheduling, dynamic pathfinding via A* algorithm, obstacle avoidance, and battery management (charging cycles).

---

##  Features

* **Pathfinding & Navigation:** Implements the **A* (A-Star) Algorithm** to find the shortest collision-free paths around walls and warehouse shelves.
* **Task Allocation (Scheduler):** Assigns pending delivery tasks to the nearest available (IDLE) robot dynamically.
* **State Machine:** Robots operate using a robust State Machine (`IDLE`, `MOVING`, `DELIVERING`, `CHARGING`).
* **Battery Management:** Automatic detection of low battery levels (< 20%) prompting robots to prioritize rerouting to charging stations.
* **Interactive Pygame GUI:** Real-time visualization of warehouse layout, robots, charging stations, and delivery points.
* **Dynamic Event Generation:** Click anywhere on the warehouse grid to dynamically generate new package delivery orders.

---

##  Repository Structure


├── main.py            # SimulationEngine & main coordination logic
├── components.py      # Core data structures (Robot, Package, Warehouse, Scheduler)
├── gui.py             # Pygame visualization and user interaction interface
├── map.json           # Warehouse grid setup (dimensions, walls, stations)
└── README.md          # Project documentation

________________________________________________________________________________________________________________________________________________________

## Project report:
## 1. Introduction & Background
In modern logistics and supply chain operations, Autonomous Mobile Robots (AMRs) have transformed traditional warehouse management. Automated fulfillment centers rely heavily on fleet management systems to coordinate multiple robots tasked with picking, transporting, and delivering goods.

The core challenge of automated warehouse operations lies in designing systems capable of real-time multi-agent coordination. Robots must navigate around fixed obstacles (shelves, structural pillars) and dynamic agents (other robots), efficiently allocate tasks, and self-regulate health metrics such as battery levels. 

This report presents an **Autonomous Warehouse Robot Simulation** written in Python, incorporating pathfinding algorithms, finite state machines, automated scheduling, and interactive graphical visualization via Pygame.

---

## 2. System Architecture & Class Design

The system architecture follows a modular, object-oriented design split across distinct subcomponents:

              +-----------------------+
              |   SimulationEngine    |
              +-----------+-----------+
                          |
   +----------------------+----------------------+
   |                      |                      |
+------v-------+      +-------v------+      +--------v------+
|  Warehouse   |      |   Scheduler  |      | WarehouseGUI  |
+--------------+      +--------------+      +---------------+
|                      |
+------v-------+      +-------v------+
|    Robot     |      |   Package    |
+--------------+      +--------------+


### Key Classes Description:
1. **`Warehouse`**: Encapsulates the environment layout, loaded from `map.json`. It maintains grid dimensions, static obstacles (walls, shelves), charging stations, and drop-off destinations.
2. **`Robot`**: Represents an individual AMR. It tracks current position, battery state, operational mode, target destination, and calculated movement path.
3. **`Package`**: Defines cargo entity attributes, including unique package IDs, pickup coordinates, target delivery locations, and current status (`PENDING`, `PICKED_UP`, `DELIVERED`).
4. **`Scheduler`**: Manages task allocation. It matches unassigned packages with candidate robots using proximity heuristic calculations.
5. **`SimulationEngine`**: Drives discrete time-step execution, syncing robot position updates, battery depletion, and path planning.
6. **`WarehouseGUI`**: Handles Pygame rendering and user input event loops.

---

## 3. Methodologies & Algorithms

### 3.1 Pathfinding: A* (A-Star) Search Algorithm
To navigate the grid environment without colliding with obstacles, robots utilize the **A* Search Algorithm**. A* finds the optimal path by evaluating nodes based on the cost function:

$$f(n) = g(n) + h(n)$$

* **$g(n)$**: The exact movement cost from the starting position to node $n$.
* **$h(n)$**: The estimated heuristic cost from node $n$ to the goal.

In this grid environment, the **Manhattan Distance** heuristic is employed due to 4-directional movement constraints:

$$h(n) = \vert{}x_{goal} - x_n\vert{} + \vert{}y_{goal} - y_n\vert{}$$

### 3.2 Finite State Machine (FSM)
Each robot operates under a Finite State Machine to govern behavior transitions seamlessly:

       +--------------+
       |     IDLE     | <--------------+
       +------+-------+                |
              |                        |
     (New Task Assigned)     (Delivery Completed)
              |                        |
              v                        |
       +--------------+                |
       |    MOVING    |                |
       +------+-------+                |
              |                        |
        (Package Reached)              |
              |                        |
              v                        |
       +--------------+                |
       |  DELIVERING  |----------------+
       +------+-------+
              |
    (Battery < 20%)
              |
              v
       +--------------+
       |   CHARGING   |
       +--------------+

* **`IDLE`**: Robot is stationary at its location, awaiting task allocation. Power consumption is minimal.
* **`MOVING`**: Robot is traversing path towards the package pickup point.
* **`DELIVERING`**: Robot has retrieved the package and is transporting it to the drop-off location.
* **`CHARGING`**: Robot has interrupted tasks or reached low threshold (< 20%) and is routing/stationed at a charging pad until battery reaching 100%.

---

## 4. Implementation Details & GUI Integration

The user interface is built using **Pygame**, providing a visual grid visualization where each cell represents a $60 \times 60$ pixel area. 

### Visual Elements Color Scheme:
* **Background Grid**: Light Gray (`#F5F5F5` / `#C8C8C8`)
* **Obstacles & Shelves**: Solid Blue (`#2980B9`)
* **Robots (AMRs)**: Green Circles (`#2ECC71`)
* **Charging Stations**: Solid Yellow (`#F1C40F`)
* **Delivery Points**: Solid Purple (`#9B59B6`)

### Dynamic Event Handling
The simulation allows users to simulate dynamic demand spikes. Through event handling within `gui.py`, a left-click on any walkable grid square calculates grid coordinates $(G_x, G_y)$, creates a new `Package` instance, and pushes it into the `pending_packages` queue of the simulation engine.

---

## 5. Results & Operational Analysis

### 5.1 Idle State Stability
When all assigned tasks are fulfilled, robots transition to the `IDLE` state at their final delivery points. During this phase:
* Robot coordinates remain constant.
* Step counters continue in the `Terminal` for tracking uptime.
* Battery levels stop depleting, demonstrating energy optimization.

### 5.2 Dynamic Task Response
Upon adding new tasks (via mouse input), the `Scheduler` calculates Manhattan distances from all idle robots to the new pickup location and successfully assigns the task to the closest available robot.

---

## 6. Conclusion & Future Enhancements

The simulation demonstrates an effective multi-agent system capable of managing basic warehouse logistics through deterministic pathfinding and task scheduling.

### Future Work:
1. **Dynamic Obstacle Avoidance (Reservation Tables):** Implementing Space-Time A* or Multi-Agent Pathfinding (MAPF) algorithms (e.g., CBS) to prevent two robots from attempting to occupy the same grid square at identical time steps.
2. **Dynamic Charger Allocation:** Enabling robots to queue at charging stations when demand exceeds charger capacity.
3. **Advanced GUI Metrics:** Adding live UI panels showing current battery percentages, active task counts, and total system throughput.
