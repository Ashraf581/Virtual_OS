# VirtuOS - Operating System Simulation Modules
import threading
import time

# ------------------ Process Management ------------------
process_table = []

def reset_processes_state():
    """
    Resets all process states to 'New' to allow schedulers to be run again 
    with the original process set.
    """
    for p in process_table:
        p['state'] = "New"
    print("All process states have been reset to New.")

def schedule_fcfs():
    """
    Simple FCFS (First Come First Serve) Scheduling.
    """
    if not process_table:
        print("No processes to schedule.")
        return

    print("\n--- FCFS Scheduling ---")
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0

    # Reset old terminated processes
    for p in process_table:
        if p['state'] == "Terminated":
            p['state'] = "New"

    # All processes move to Ready
    for p in process_table:
        if p['state'] == "New":
            p['state'] = "Ready"
            print(f"{p['name']} → Ready")
    print()
    
    # Run each process in order
    for process in process_table:
        # Simulate I/O wait
        process['state'] = "Waiting"
        print(f"{process['name']} waiting (I/O)...")
        time.sleep(1)

        # Ready again
        process['state'] = "Ready"
        print(f"{process['name']} ready for CPU")

        # Running
        process['state'] = "Running"
        print(f"{process['name']} running...")
        time.sleep(process['burst_time'])

        # Update times
        waiting_time = current_time
        current_time += process['burst_time'] + 1  # +1 for simulated I/O
        turnaround_time = current_time

        # Terminate
        process['state'] = "Terminated"
        print(f"{process['name']} finished.\n")

        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time

    n = len(process_table)
    print(f"Average Waiting Time: {total_waiting_time / n:.2f}")
    print(f"Average Turnaround Time: {total_turnaround_time / n:.2f}")


def schedule_sjf():
    """
    Simple SJF (Shortest Job First) Scheduling.
    """
    if not process_table:
        print("No processes to schedule.")
        return

    print("\n--- SJF Scheduling ---")

    # Sort by burst time (Shortest Job First)
    sorted_processes = sorted(process_table, key=lambda x: x['burst_time'])

    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0

    # Reset old terminated processes
    for p in sorted_processes:
        if p['state'] == "Terminated":
            p['state'] = "New"

    # All processes move to Ready
    for p in sorted_processes:
        if p['state'] == "New":
            p['state'] = "Ready"
            print(f"{p['name']} → Ready")
    print()
    # Run processes based on burst time order
    for process in sorted_processes:
        # Simulate I/O wait
        process['state'] = "Waiting"
        print(f"{process['name']} waiting (I/O)...")
        time.sleep(1)

        # Ready again
        process['state'] = "Ready"
        print(f"{process['name']} ready for CPU")

        # Running
        process['state'] = "Running"
        print(f"{process['name']} running...")
        time.sleep(process['burst_time'])

        # Update times
        waiting_time = current_time
        current_time += process['burst_time'] + 1  # +1 for I/O simulation
        turnaround_time = current_time

        # Terminate
        process['state'] = "Terminated"
        print(f"{process['name']} finished.\n")

        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time

    n = len(sorted_processes)
    print(f"Average Waiting Time: {total_waiting_time / n:.2f}")
    print(f"Average Turnaround Time: {total_turnaround_time / n:.2f}")



def create_process(name, burst_time):
    """Creates a new process with a given name and CPU burst time."""
    if any(p['name'] == name for p in process_table):
        print(f"Process {name} already exists.")
        return
    if burst_time <= 0:
        print("Burst time must be a positive integer.")
        return
        
    process = {"name": name, "burst_time": burst_time, "state": "New"}
    process_table.append(process)
    print(f"Process {name} created with CPU burst time {burst_time}.")

def list_processes():
    """Displays the current process table."""
    if not process_table:
        print("No processes found.")
        return

    print("Current Processes:")
    print("{:<5} {:<15} {:<20}".format("Name", "Burst Time", "State"))
    print("-" * 45)
    for p in process_table:
        print("{:<5} {:<15} {:<20}".format(p['name'], p['burst_time'], p['state']))


# ------------------ Memory Management ------------------
memory_frames = []
frame_limit = 3
page_faults = 0

def set_frames(n):
    """Initializes main memory with a specified number of frames."""
    global frame_limit, memory_frames, page_faults
    if n <= 0:
        print("Frame limit must be greater than zero.")
        return
        
    frame_limit = n
    memory_frames = []
    page_faults = 0 
    print(f"Memory initialized with {frame_limit} frames.")

def request_pages(pages):
    """
    Simulates memory access using the First-In, First-Out (FIFO) page 
    replacement policy.
    """
    global memory_frames, page_faults
    print(f"\n--- Requesting Pages (FIFO Policy) ---")
    for page in pages:
        if page not in memory_frames:
            page_faults += 1
            if len(memory_frames) < frame_limit:
                # Page fault: Frame available
                memory_frames.append(page)
                print(f"Page {page} caused a page fault. Added to memory.")
            else:
                # Page fault: Replace the oldest page (FIFO)
                removed = memory_frames.pop(0)
                memory_frames.append(page)
                print(f"Page {page} caused a page fault. Replaced page {removed}.")
        else:
            print(f"Page {page} already in memory (Hit).")
            
        print(f"  Current Frames: {memory_frames}")
            
    print(f"Total Page Faults: {page_faults}")

# ------------------ Producer-Consumer (Synchronization) ------------------
buffer = []
buffer_size = 5

# Semaphores and Mutex for synchronization
empty = threading.Semaphore(buffer_size) # Counts empty slots
full = threading.Semaphore(0)            # Counts full slots
mutex = threading.Lock()                 # Ensures mutual exclusion for buffer access

def producer(items):
    """Thread function to produce items and put them in the buffer."""
    for item in items:
        empty.acquire() # Wait for an empty slot
        mutex.acquire() # Acquire lock for critical section
        buffer.append(item)
        print(f"[PRODUCER] Produced: {item} | Buffer: {buffer}")
        mutex.release() # Release lock
        full.release()  # Signal one full slot
        time.sleep(1)

def consumer(count):
    """Thread function to consume items from the buffer."""
    for _ in range(count):
        full.acquire()  # Wait for a full slot
        mutex.acquire() # Acquire lock for critical section
        if buffer:
            item = buffer.pop(0)
            print(f"[CONSUMER] Consumed: {item} | Buffer: {buffer}")
        mutex.release() # Release lock
        empty.release() # Signal one empty slot
        time.sleep(1)

# ------------------ File Management ------------------
file_table = {}

def create_file(filename):
    """Creates an entry for a new file in the file table."""
    if filename in file_table:
        print(f"File '{filename}' already exists.")
        return
    file_table[filename] = {"content": "", "size": 0}
    print(f"File '{filename}' created successfully.")

def delete_file(filename):
    """Removes a file entry from the file table."""
    if filename not in file_table:
        print(f"File '{filename}' not found.")
        return
    del file_table[filename]
    print(f"File '{filename}' deleted successfully.")

def list_files():
    """Lists all files, their names, and sizes."""
    if not file_table:
        print("No files found.")
        return
    print("Files in VirtuOS:")
    print("{:<15} {:<5}".format("Name", "Size"))
    print("-" * 20)
    for fname, fdata in file_table.items():
        print("{:<15} {:<5}".format(fname, fdata['size']))

def write_file(filename, data):
    """Appends data to the content of a file and updates its size."""
    if filename not in file_table:
        print(f"File '{filename}' not found.")
        return
    file_table[filename]["content"] += data
    file_table[filename]["size"] = len(file_table[filename]["content"])
    print(f"Data written to '{filename}' successfully. New size: {file_table[filename]['size']}")

def read_file(filename):
    """Displays the content of a file."""
    if filename not in file_table:
        print(f"File '{filename}' not found.")
        return
    print(f"Content of '{filename}':")
    print(file_table[filename]["content"])

# ------------------ Command Interface ------------------
while True:
    raw_command = input("\n> ").strip()
    command = raw_command.lower()

    if command == "exit":
        print("Exiting VirtuOS...")
        break

    # Process Commands
    elif command.startswith("create"):
        parts = raw_command.split()
        if len(parts) != 3:
            print("Invalid command. Use: create <process_name> <burst_time>")
            continue
        name, burst = parts[1], parts[2]
        if not burst.isdigit():
            print("Burst time must be a number.")
            continue
        create_process(name, int(burst))

    elif command == "list":
        list_processes()
    elif command == "schedule fcfs":
        schedule_fcfs()
    elif command == "schedule sjf":
        schedule_sjf()
    elif command == "reset":
        reset_processes_state()

    # Memory Commands
    elif command.startswith("set frames"):
        parts = raw_command.split()
        if len(parts) != 3 or not parts[2].isdigit():
            print("Invalid command. Use: set frames <number>")
            continue
        set_frames(int(parts[2]))

    elif command.startswith("request pages"):
        parts = raw_command.split()
        if len(parts) < 3 or not all(p.isdigit() for p in parts[2:]):
            print("Invalid command. Use: request pages <page_numbers> (e.g., request pages 1 2 3 4)")
            continue
        pages = [int(p) for p in parts[2:]]
        request_pages(pages)

    # File Commands
    elif command.startswith("file create"):
        parts = raw_command.split()
        if len(parts) != 3:
            print("Invalid command. Use: file create <filename>")
            continue
        create_file(parts[2])

    elif command.startswith("file delete"):
        parts = raw_command.split()
        if len(parts) != 3:
            print("Invalid command. Use: file delete <filename>")
            continue
        delete_file(parts[2])

    elif command == "file list":
        list_files()

    elif command.startswith("file write"):
        # Use maxsplit to correctly capture all subsequent text as data
        parts = raw_command.split(maxsplit=3)
        if len(parts) != 4:
            print("Invalid command. Use: file write <filename> <data>")
            continue
        write_file(parts[2], parts[3])

    elif command.startswith("file read"):
        parts = raw_command.split()
        if len(parts) != 3:
            print("Invalid command. Use: file read <filename>")
            continue
        read_file(parts[2])

    # Synchronization Command
    elif command.startswith("sync producer_consumer"):
        parts = raw_command.split()
        if len(parts) < 3:
            print("Invalid command. Use: sync producer_consumer <item1> <item2> ...")
            continue
        items = parts[2:]
        # Start producer and consumer threads
        prod_thread = threading.Thread(target=producer, args=(items,))
        cons_thread = threading.Thread(target=consumer, args=(len(items),))
        print("Starting Producer and Consumer threads...")
        prod_thread.start()
        cons_thread.start()
        prod_thread.join()  # Wait for producer to finish
        cons_thread.join()  # Wait for consumer to finish
        print("\nProducer-Consumer simulation complete.")

    else:
        print("Unknown command. Available commands: create, list, schedule fcfs, schedule sjf, reset, "
              "set frames, request pages, file create/delete/list/write/read, "
              "sync producer_consumer, exit")