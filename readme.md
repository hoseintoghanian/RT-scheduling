# Project: Multi-Subsystem Task Scheduler

## Overview
This project implements a multi-subsystem task scheduling system using Python. Each subsystem is responsible for executing tasks, managing resources, and scheduling using algorithms like Round Robin. The system simulates real-time scheduling with resource constraints and multiple processing cores.

## Features
- **Task Scheduling:** Supports algorithms like Round Robin and Shortest Remaining Time First (SRTF).
- **Resource Management:** Dynamically allocates and releases resources for tasks.
- **Parallel Subsystems:** Each subsystem runs as a separate thread.
- **Real-Time Simulation:** Simulates task execution and resource management in real-time.

## How It Works
1. **Input Parsing:**
   - Reads configuration and task definitions from an input file.
   - Each subsystem is defined by its available resources and tasks.

2. **Subsystems:**
   - Each subsystem has:
     - Resources (e.g., R1, R2).
     - A ready queue for tasks ready to execute.
     - A waiting queue for tasks awaiting resources.
     - Multiple processing cores.

3. **Scheduling:**
   - Tasks are scheduled to cores based on the selected algorithm (default: Round Robin).
   - If resources are insufficient, tasks move to the waiting queue.

4. **Task Execution:**
   - Tasks execute on cores until completion, releasing their allocated resources.
   - The state of the system is printed at each time unit.

5. **Termination:**
   - The simulation ends when all tasks in all subsystems are completed.

## Input File Format
The input file should define resources and tasks for each subsystem. Format:

```
<resources_R1 R2>
<task_id arrival_time exec_time resource1 resource2 priority>
<task_id arrival_time exec_time resource1 resource2 priority>
...
$
<resources_R1 R2>
<task_id arrival_time exec_time resource1 resource2 priority>
...
$
```

### Example Input File
```
3 3
T11 1 4 1 1 1
T12 2 3 1 1 1
T13 3 2 2 1 2
$
4 5
T21 1 5 2 3 1
T22 2 4 1 2 2
$
5 6
T31 1 6 2 2 1
T32 3 3 1 1 3
T33 5 2 1 1 2
$
```

## Output
The program prints the state of each subsystem at every time unit, showing:
- Available resources.
- Tasks in the waiting and ready queues.
- Tasks running on each core.

### Example Output
```
Time: 1, Subsystem 1 State:
Resources: R1: 1, R2: 0
Waiting Queue: []
Ready Queue: [T12, T13]
Cores: [T11, Idle, Idle]
==============================
Time: 2, Subsystem 1 State:
Resources: R1: 1, R2: 0
Waiting Queue: []
Ready Queue: [T13]
Cores: [T12, Idle, Idle]
==============================
...
```

## Running the Project
1. Prepare the input file (`input.txt`) with the required format.
2. Place the input file in the same directory as the script or update the `input_file` path in the `main()` function.
3. Run the script:
   ```
   python OS-project.py
   ```

## Requirements
- Python 3.x

## Code Structure
- **Task Class:** Represents a task with attributes like ID, arrival time, execution time, and resources required.
- **Subsystem Class:** Manages tasks, resources, and cores for a subsystem.
- **MainSystem Class:** Orchestrates all subsystems.
- **parse_input Function:** Reads and parses the input file.
- **main Function:** Initializes and runs the system.

## Known Issues and Limitations
- The current implementation assumes the input file is correctly formatted.
- Scheduling algorithms other than Round Robin and SRTF are not implemented.
- The simulation runs in real-time, which may not suit all use cases.

## Future Enhancements
- Add support for more scheduling algorithms like Priority Scheduling.
- Implement more detailed logging for debugging.
- Improve resource allocation strategies to optimize performance.

## Contact
For any questions or suggestions, please contact the project maintainer.

