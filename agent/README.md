# Provider-Neutral Design Agent

This is the executable workflow layer for the Aesthetic Design System. It keeps design decisions provider-neutral so the same process can be used with OpenCode, Pi, hosted APIs, local models, or another model runner.

The agent does not hard-code a model SDK. It prepares a complete prompt package, accepts the provider's JSON response, and validates the result against a shared contract.

## Architecture

```text
Project brief + design system
            ↓
       workflow prompt
            ↓
  provider adapter / command
            ↓
    structured JSON result
            ↓
      contract validator
```

The model is replaceable. The design system, workflow, schemas, and validators are the stable parts.

## Install

No package installation is required. Python 3.9+ is sufficient.

## Quick start

Create a project brief from the template, then render a provider-neutral prompt:

```bash
python3 agent/cli.py prompt \
  --task generate-design \
  --brief path/to/project-brief.json \
  --output agent/runs/generate-design.prompt.md
```

Send that prompt to any model provider using its own command, then validate the JSON response:

```bash
python3 agent/cli.py validate \
  --task design-spec \
  --input agent/runs/design-spec.json
```

You can also pipe the rendered prompt directly into a provider command. The command must read the prompt from stdin and write one JSON object to stdout:

```bash
python3 agent/cli.py run \
  --task generate-design \
  --brief path/to/project-brief.json \
  --output agent/runs/design-spec.json \
  -- opencode YOUR_PROVIDER_ARGUMENTS
```

The `--` separator keeps provider-specific arguments outside the design agent. For Pi or another runner, replace the command after `--` without changing the brief, workflow, or schema.

## Tasks

- `analyze-brief`: identify missing information and assumptions.
- `generate-design`: create an implementation-ready design specification.
- `audit-design`: review a design specification against the system.

Each task has a workflow file in `agent/workflows/` and an output schema in `agent/schemas/`.

## Provider adapter contract

An adapter only needs to do three things:

1. Read the prompt from stdin.
2. Send it to the selected model.
3. Write exactly one JSON object to stdout.

Provider-specific setup, authentication, model selection, and tool permissions stay outside this repository. This means switching providers does not change the project brief or design rules.

## Quality gates

The runner performs deterministic checks before accepting a response:

- JSON is syntactically valid.
- The top-level response has the required fields.
- Screen, component, token, accessibility, and open-question sections have the expected types.
- Audit reports contain severity, location, finding, rationale, and recommendation fields.

Model judgment remains useful for visual and UX decisions, while the validator catches malformed or incomplete handoffs.
