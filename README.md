VirtuOS – Operating System Simulation Modules
VirtuOS is a Python-based Operating System simulator designed to help students understand key OS concepts like process scheduling, memory management, file systems, and synchronization.
It provides a command-line interface where users can run simulations interactively.

⚙️ Features
🧩 1. Process Management

Create and list processes

Run FCFS (First Come First Serve) and SJF (Shortest Job First) scheduling

Display waiting and turnaround times

Reset process states for re-simulation

🧠 2. Memory Management

Set number of memory frames

Simulate FIFO Page Replacement Algorithm

Track and display page faults

🔒 3. Synchronization

Implements the Producer-Consumer problem using:

Semaphores (empty, full)

Mutex lock for critical section

Demonstrates multithreading behavior in Python

📂 4. File Management

Create, read, write, delete files

View file table with names and sizes

Persistent file simulation within session

💻 Commands Reference
Category	Command	Description
Process	create <name> <burst_time>	Create a new process
Process	list	Show all processes
Process	schedule fcfs	Run FCFS scheduling
Process	schedule sjf	Run SJF scheduling
Process	reset	Reset all process states
Memory	set frames <n>	Set number of memory frames
Memory	request pages <p1> <p2> ...	Simulate FIFO page replacement
File	file create <filename>	Create new file
File	file delete <filename>	Delete a file
File	file list	List all files
File	file write <filename> <data>	Write data into file
File	file read <filename>	Read file content
Sync	sync producer_consumer <items>	Run producer-consumer threads
System	exit	Exit VirtuOS
