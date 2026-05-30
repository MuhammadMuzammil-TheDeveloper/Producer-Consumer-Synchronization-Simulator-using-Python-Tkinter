# Producer-Consumer Synchronization Simulator

## Overview

The Producer-Consumer Synchronization Simulator is an Operating System project developed in Python using Tkinter. It demonstrates one of the most important synchronization problems in OS: the Producer-Consumer Problem.

This simulator visualizes how producers generate items and place them into a shared buffer while consumers remove items from the buffer. Synchronization is achieved using Semaphores and Mutual Exclusion (Mutex) to avoid race conditions and ensure safe access to shared resources.

---

## Features

### Real-Time Synchronization Visualization
- Visual representation of shared buffer.
- Producer and Consumer status updates.
- Dynamic buffer state monitoring.

### Semaphore-Based Synchronization
- Uses:
  - Mutex Semaphore
  - Empty Semaphore
  - Full Semaphore
- Demonstrates critical section management.

### Interactive Controls
- Start Simulation
- Stop Simulation
- Reset Simulation

### Adjustable Speeds
- Producer Speed Control
- Consumer Speed Control

### Event Logging System
- Timestamped logs.
- Producer activity logs.
- Consumer activity logs.
- System event notifications.

### Modern GUI
- Built with Python Tkinter.
- User-friendly interface.
- Color-coded status indicators.

---

## Operating System Concepts Demonstrated

- Process Synchronization
- Producer-Consumer Problem
- Critical Section
- Mutual Exclusion
- Thread Management
- Counting Semaphores
- Shared Buffer Management
- Race Condition Prevention

---

## Technologies Used

- Python 3
- Tkinter
- Threading Module
- Semaphore Synchronization
- Random Module
- Time Module

---

## Buffer Structure

Buffer Size: 6 Slots

States:
- EMPTY
- FILLED
- FULL

---

## Synchronization Mechanism

### Semaphores Used

#### Mutex
Ensures only one thread accesses the critical section at a time.

```python
mutex = threading.Semaphore(1)
