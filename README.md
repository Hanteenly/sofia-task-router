# SOFIA Task Router

## Overview

SOFIA Task Router is a small Python project that demonstrates a task router designed to route tasks between different execution backends. First, the Policy evaluates the task according to the safety rules. Then, the Router selects an available backend according to the routing priorities. The selected backend executes the task and returns the result. Finally, Audit records the router's actions and results.

## Architecture

### Task

A class designed to represent an incoming task. It contains the task ID,
intent, data sensitivity, risk class, allowed backends, approval requirements
and payload.

### Policy

Checks incoming tasks for risks and evaluates them according to the safety
rules. It can allow execution, block cloud execution or require human approval.

### Router

Provides the main routing functionality. It evaluates the policy result,
checks the available backends and selects a suitable backend according to
the routing priorities.

### Backends

Execute the task payload according to the task intent. Each backend provides
a common execution interface, allowing different backend implementations to
be used by the router.

### Audit

Records information about the router's operation. Each processed task
produces a structured audit record containing the routing decision, selected
backend, policy decision, execution status, errors or limitations and timestamp.

## Features

* Task.__init__() — holds the basic information about a task, such as its ID, safety levels, and input data.

* Policy.evaluate(task) — checks whether the task is safe to run or requires approval or cloud blocking.

* Backend.execute(task) — defines the base method that all backends must implement.

* LocalBackend.execute(task) — runs the task locally by splitting the text into sentences and selecting important words.

* CloudBackend.execute(task) — simulates cloud processing by finding the most frequently repeated words in the text.

* MockBackend.execute(task) — returns the input text unchanged as a simple test backend.

* Audit.__init__() — creates an empty list for storing router log records.

* Audit.log(self, task, routing_decision, selected_backend,
policy_decision, execution_status, error_or_limitation) — saves a detailed record of task processing, including the routing decision, backend, status, errors, and timestamp.

* Router.__init__() — initializes the router and creates an audit tracker instance.

* Router.route(task, available_backends) — checks safety rules, selects the best available backend with local-first priority, and logs the result.

* test_local_first() — verifies that the router prefers the local backend when it is available.

* test_restricted_blocks_cloud() — verifies that restricted and sealed tasks cannot be executed by the cloud backend.

* test_high_stakes_requires_approval() — verifies that write-risk and high-stakes tasks require human approval.

* test_local_failure_no_cloud_fallback() — verifies that a local execution failure returns fallback-required instead of silently switching to the cloud.

* test_backend_switching() — verifies that the router can switch between local, cloud, and mock backends according to the allowed backend rules.

## Project Structure
```text
sofia-task-router/
├── src/
│   └── sofia/
│       ├── __init__.py
│       ├── audit/
│       │   ├── __init__.py
│       │   └── Audit.py
│       ├── backends/
│       │   ├── __init__.py
│       │   ├── Backend.py
│       │   ├── CloudBackend.py
│       │   ├── LocalBackend.py
│       │   └── MockBackend.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py
│       ├── policy/
│       │   ├── __init__.py
│       │   └── evaluation.py
│       ├── router/
│       │   ├── __init__.py
│       │   └── router.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_router.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## How to Run

uv run python src/sofia/main.py

## Tests

* test_local_first() — verifies that the local backend has priority when it is available.

* test_restricted_blocks_cloud() — verifies that tasks with restricted or sealed data sensitivity cannot be routed to the cloud backend.

* test_high_stakes_requires_approval() — verifies that tasks with write-risk or high-stakes risk classes require human approval.

* test_local_failure_no_cloud_fallback() — verifies that a local backend failure does not trigger a silent cloud fallback.

* test_backend_switching() — verifies that the router can work with different backend implementations.

## Examples

### Example №1
task_id="task-001",
intent="summarize",
data_sensitivity="internal",
risk_class="read-safe",
allowed_backends=["local", "cloud"],
requires_human_approval=False,
payload={"text": "Example document content"}

Example document content

### Example №2
task_id="task-002",
intent="summarize",
data_sensitivity="internal",
risk_class="read-safe",
allowed_backends=["cloud"],
requires_human_approval=False,
payload={"text": "Example document content"}

no-backend

### Example №3
task_id="task-003",
intent="summarize",
data_sensitivity="restricted",
risk_class="read-safe",
allowed_backends=["cloud"],
requires_human_approval=False,
payload={"text": "Sensitive document"}

no-backend

## Trade-offs / Assumptions

- Backends use simple mock implementations for the prototype.
- Audit records are stored in memory.
- No real cloud API is used.
- No frontend or REST API was implemented because it was not required for the assignment.

## What I Would Change for Production

- Replace the simple backend implementations with real, configurable adapters.
- Replace string-based policy decisions with enums or structured result types.
- Add persistent storage for audit records.
- Add proper logging, monitoring and metrics.