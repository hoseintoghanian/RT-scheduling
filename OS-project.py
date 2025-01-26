import threading
import queue
import time

# Task class to represent each task
class Task:
    def __init__(self, task_id, arrival_time, exec_time, resource1, resource2, priority=None, repeat=None):
        self.task_id = task_id  # Unique ID for the task
        self.arrival_time = arrival_time  # Time when the task arrives
        self.exec_time = exec_time  # Total execution time required
        self.resource1 = resource1  # Amount of resource R1 required
        self.resource2 = resource2  # Amount of resource R2 required
        self.remaining_time = exec_time  # Time remaining to complete execution
        self.priority = priority  # Priority of the task (used in certain algorithms)
        self.repeat = repeat  # Number of repetitions (for periodic tasks)
        self.state = "Waiting"  # Task state: Waiting, Ready, Running, Completed

    def __str__(self):
        return f"Task({self.task_id}, Arrival={self.arrival_time}, ExecTime={self.exec_time}, R1={self.resource1}, R2={self.resource2}, State={self.state})"

# Subsystem class to manage tasks and resources
class Subsystem(threading.Thread):
    def __init__(self, subsystem_id, resources, algorithm, num_cores):
        super().__init__()
        self.subsystem_id = subsystem_id
        self.resources = resources  # [R1, R2]
        self.algorithm = algorithm  # Scheduling algorithm (e.g., Round Robin, SRTF)
        self.cores = [None] * num_cores  # Cores available in the subsystem
        self.ready_queue = queue.Queue()  # Ready queue for tasks
        self.waiting_queue = []  # Waiting queue for tasks
        self.completed_tasks = []  # List of completed tasks
        self.current_time = 0  # Internal clock for the subsystem
        self.lock = threading.Lock()  # For synchronization

    def add_task(self, task):
        """Add a task to the ready queue or waiting queue based on available resources."""
        if task.resource1 <= self.resources[0] and task.resource2 <= self.resources[1]:
            self.ready_queue.put(task)
            task.state = "Ready"
        else:
            self.waiting_queue.append(task)
            task.state = "Waiting"

    def release_resources(self, task):
        """Release resources used by a completed task."""
        self.resources[0] += task.resource1
        self.resources[1] += task.resource2

    def schedule_tasks(self):
        """Schedule tasks based on the selected algorithm."""
        with self.lock:
            if self.algorithm == "Round Robin":
                for i in range(len(self.cores)):
                    if not self.cores[i] and not self.ready_queue.empty():
                        task = self.ready_queue.get()
                        if task.resource1 <= self.resources[0] and task.resource2 <= self.resources[1]:
                            self.resources[0] -= task.resource1
                            self.resources[1] -= task.resource2
                            self.cores[i] = task
                            task.state = "Running"
                            print(f"Task {task.task_id} started on Core {i+1} in Subsystem {self.subsystem_id}")
                        else:
                            self.ready_queue.put(task)
            elif self.algorithm == "SRTF":
                tasks = list(self.ready_queue.queue)
                tasks.sort(key=lambda t: t.remaining_time)
                self.ready_queue.queue.clear()
                for t in tasks:
                    self.ready_queue.put(t)
                for i in range(len(self.cores)):
                    if not self.cores[i] and not self.ready_queue.empty():
                        task = self.ready_queue.get()
                        if task.resource1 <= self.resources[0] and task.resource2 <= self.resources[1]:
                            self.resources[0] -= task.resource1
                            self.resources[1] -= task.resource2
                            self.cores[i] = task
                            task.state = "Running"
                            print(f"Task {task.task_id} started on Core {i+1} in Subsystem {self.subsystem_id}")
                        else:
                            self.ready_queue.put(task)

    def release_completed_tasks(self):
        """Release completed tasks and free resources."""
        for i in range(len(self.cores)):
            if self.cores[i] and self.cores[i].remaining_time <= 0:
                task = self.cores[i]
                self.release_resources(task)
                self.cores[i] = None
                task.state = "Completed"
                self.completed_tasks.append(task)
                print(f"Task {task.task_id} completed in Subsystem {self.subsystem_id}")

    def is_done(self):
        """Check if all tasks are completed."""
        return self.ready_queue.empty() and not any(self.cores) and len(self.waiting_queue) == 0

    def run(self):
        while not self.is_done():
            self.current_time += 1

            # Move waiting tasks to ready queue if resources are available
            for task in self.waiting_queue[:]:
                if task.resource1 <= self.resources[0] and task.resource2 <= self.resources[1]:
                    self.ready_queue.put(task)
                    self.waiting_queue.remove(task)
                    task.state = "Ready"

            # Release completed tasks
            self.release_completed_tasks()

            # Schedule tasks to cores
            self.schedule_tasks()

            # Update remaining time for tasks running on cores
            for core in self.cores:
                if core:
                    core.remaining_time -= 1

            # Print current state
            print(f"Time: {self.current_time}, Subsystem {self.subsystem_id} State:")
            print(f"Resources: R1: {self.resources[0]}, R2: {self.resources[1]}")
            print(f"Waiting Queue: {[task.task_id for task in self.waiting_queue]}")
            print(f"Ready Queue: {[task.task_id for task in list(self.ready_queue.queue)]}")
            print(f"Cores: {[core.task_id if core else 'Idle' for core in self.cores]}")
            print("=" * 30)

            time.sleep(1)  # Simulate time progression

# MainSystem class to manage all subsystems
class MainSystem:
    def __init__(self):
        self.subsystems = []  # List of subsystems

    def add_subsystem(self, subsystem):
        self.subsystems.append(subsystem)

    def run(self):
        # Start all subsystems
        for subsystem in self.subsystems:
            subsystem.start()

        # Monitor system state until all subsystems are done
        while not all(subsystem.is_done() for subsystem in self.subsystems):
            time.sleep(5)  # Report system state every 5 seconds
            for subsystem in self.subsystems:
                print(f"Subsystem {subsystem.subsystem_id} State at Time {subsystem.current_time}:")
                print(f"Resources: R1: {subsystem.resources[0]}, R2: {subsystem.resources[1]}")

# Function to read input from a file
def parse_input(file_name):
    subsystems = []
    with open(file_name, 'r') as file:
        lines = file.readlines()

    current_resources = []
    subsystem_id = 0

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        if line == "$":  # End of a subsystem
            if current_resources:  # Only create subsystem if resources exist
                subsystem_id += 1
                subsystems.append(Subsystem(subsystem_id, current_resources, "Round Robin", 3))
                current_resources = []
            continue

        if len(current_resources) == 0:  # Reading resources for the subsystem
            current_resources = list(map(int, line.split()))
        else:  # Reading tasks for the subsystem
            task_info = line.split()
            if len(task_info) >= 6:  # Ensure task has all required fields
                task = Task(
                    task_id=task_info[0],
                    arrival_time=int(task_info[1]),
                    exec_time=int(task_info[2]),
                    resource1=int(task_info[3]),
                    resource2=int(task_info[4]),
                    priority=int(task_info[5]) if len(task_info) > 5 else None
                )
                if len(subsystems) > 0:  # Ensure subsystem exists before adding tasks
                    subsystems[-1].add_task(task)
                else:
                    print(f"Error: No subsystem available for task: {line}")
    return subsystems

# Example usage
def main():
    # Parse input from file
    input_file = "C:/Users/platin/Desktop/input.txt"
    subsystems = parse_input(input_file)

    # Define main system
    main_system = MainSystem()
    for subsystem in subsystems:
        main_system.add_subsystem(subsystem)

    # Run the main system
    main_system.run()

if __name__ == "__main__":
    main()






# input_file = "C:/Users/platin/Desktop/input.txt"