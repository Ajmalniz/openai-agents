# Detailed Notes: Agents SDK Core Files

This document provides detailed explanations for the core files in the Agents SDK, focusing on their purpose, main classes/functions, and key implementation details.

---

## 1. `__init__.py`
**Purpose:**
- Acts as the main entry point for the `agents` package.
- Exposes all major classes, functions, and utilities for external use.

**Key Features:**
- Imports and re-exports core abstractions: `Agent`, `Runner`, `Model`, `Tool`, `Guardrail`, etc.
- Provides utility functions for setting default OpenAI API keys, clients, and logging.
- Defines `__all__` to control what is exported when importing `*` from the package.

**Notable Functions:**
- `set_default_openai_key`, `set_default_openai_client`, `set_default_openai_api`: Configure OpenAI API usage.
- `enable_verbose_stdout_logging`: Enables debug logging to stdout.

---

## 2. `_config.py`
**Purpose:**
- Handles configuration for OpenAI API keys, clients, and API selection.

**Key Features:**
- Functions to set the default OpenAI key/client, optionally for tracing as well.
- Allows switching between OpenAI's chat completions and responses APIs.
- Delegates actual storage to `_openai_shared` and tracing setup to `set_tracing_export_api_key`.

---

## 3. `_debug.py`
**Purpose:**
- Provides debug flag utilities for controlling logging of sensitive data.

**Key Features:**
- Reads environment variables to determine if model/tool data should be logged.
- Flags: `DONT_LOG_MODEL_DATA`, `DONT_LOG_TOOL_DATA` (default: do not log sensitive data).

---

## 4. `_run_impl.py`
**Purpose:**
- Contains the core implementation for running agents, handling tool calls, handoffs, guardrails, and output processing.

**Key Classes/Functions:**
- `RunImpl`: Main class with classmethods for each step of agent execution.
  - `execute_tools_and_side_effects`: Runs tools, computer actions, MCP approvals, and handoffs.
  - `execute_handoffs`: Handles agent handoff logic, including input filtering.
  - `execute_function_tool_calls`, `execute_computer_actions`, `execute_local_shell_calls`: Run respective tool types.
  - `run_single_input_guardrail`, `run_single_output_guardrail`: Run guardrails and return results.
  - `_check_for_final_output_from_tools`: Determines if tool results should be treated as final output.
- Data classes for tracking tool use, handoffs, and step results.
- Handles streaming, tracing, and error management.

**Notable Details:**
- Orchestrates multi-agent workflows, tool execution, and guardrail enforcement.
- Input guardrails are only run for the first agent in a chain.

---

## 5. `agent_output.py`
**Purpose:**
- Defines schemas and validation logic for agent outputs.

**Key Classes:**
- `AgentOutputSchemaBase`: Abstract base for output schemas (plain text or JSON).
- `AgentOutputSchema`: Concrete implementation using Pydantic for type validation and JSON schema generation.

**Notable Details:**
- Supports strict and non-strict JSON schemas.
- Provides methods to validate and parse LLM outputs.

---

## 6. `computer.py`
**Purpose:**
- Defines interfaces for controlling a computer or browser, both synchronously and asynchronously.

**Key Classes:**
- `Computer`: Abstract base for sync operations (click, type, screenshot, etc.).
- `AsyncComputer`: Abstract base for async operations (same API as `Computer`).

**Notable Details:**
- Used for implementing tools that interact with a real or virtual computer environment.

---

## 7. `exceptions.py`
**Purpose:**
- Defines custom exception classes for the Agents SDK.

**Key Classes:**
- `AgentsException`: Base class for all SDK exceptions.
- `MaxTurnsExceeded`, `ModelBehaviorError`, `UserError`: For specific error scenarios.
- `InputGuardrailTripwireTriggered`, `OutputGuardrailTripwireTriggered`: Raised when guardrail tripwires are triggered, carrying result data.

---

## 8. `function_schema.py`
**Purpose:**
- Extracts and builds schemas for Python functions to be used as tools by agents.

**Key Classes/Functions:**
- `FuncSchema`: Captures function name, description, parameter schema, and signature.
- `function_schema`: Main function to generate a `FuncSchema` from a Python function, using docstrings and type hints.
- `generate_func_documentation`: Parses docstrings to extract descriptions and parameter info.

**Notable Details:**
- Supports Google, Numpy, and Sphinx docstring styles.
- Uses Pydantic to generate parameter schemas for LLM tool calls.

---

## 9. `guardrail.py`
**Purpose:**
- Implements input and output guardrails for agent validation and control.

**Key Classes/Functions:**
- `InputGuardrail`, `OutputGuardrail`: Classes for defining guardrail logic (with async `run` methods).
- `GuardrailFunctionOutput`, `InputGuardrailResult`, `OutputGuardrailResult`: Data classes for guardrail results.
- Decorators: `@input_guardrail`, `@output_guardrail` to easily create guardrails from functions.

**Notable Details:**
- Input guardrails can halt agent execution if a "tripwire" is triggered.
- Output guardrails validate or filter the agent's final output.
- Guardrails can be synchronous or asynchronous.

---

If you need further breakdowns, code samples, or diagrams for any of these files, let me know! 