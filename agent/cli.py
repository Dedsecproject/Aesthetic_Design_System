#!/usr/bin/env python3
"""Provider-neutral command line runner for the Aesthetic Design System."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parent.parent
AGENT_ROOT = ROOT / "agent"
SYSTEM_ROOT = ROOT / "design-system"

TASKS = {
    "analyze-brief": {
        "workflow": AGENT_ROOT / "workflows" / "analyze-brief.md",
        "schema": AGENT_ROOT / "schemas" / "brief-analysis.schema.json",
    },
    "generate-design": {
        "workflow": AGENT_ROOT / "workflows" / "generate-design.md",
        "schema": AGENT_ROOT / "schemas" / "design-spec.schema.json",
    },
    "audit-design": {
        "workflow": AGENT_ROOT / "workflows" / "audit-design.md",
        "schema": AGENT_ROOT / "schemas" / "audit-report.schema.json",
    },
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def token_catalog() -> str:
    files = sorted((SYSTEM_ROOT / "tokens").glob("*.json"))
    chunks = []
    for path in files:
        chunks.append(f"### {path.relative_to(ROOT)}\n```json\n{path.read_text(encoding='utf-8').strip()}\n```")
    return "\n\n".join(chunks)


def system_context() -> str:
    files = [
        SYSTEM_ROOT / "DESIGN_PRINCIPLES.md",
        SYSTEM_ROOT / "DESIGN_RULES.md",
        SYSTEM_ROOT / "components" / "buttons.md",
        SYSTEM_ROOT / "components" / "inputs.md",
        SYSTEM_ROOT / "components" / "cards.md",
        SYSTEM_ROOT / "components" / "navigation.md",
        SYSTEM_ROOT / "components" / "tables.md",
    ]
    chunks = []
    for path in files:
        chunks.append(f"### {path.relative_to(ROOT)}\n{path.read_text(encoding='utf-8').strip()}")
    chunks.append(f"### token catalog\n{token_catalog()}")
    return "\n\n".join(chunks)


def render_prompt(task: str, brief: Any, input_data: Any | None = None) -> str:
    metadata = TASKS[task]
    workflow = metadata["workflow"].read_text(encoding="utf-8").strip()
    schema = json_text(read_json(metadata["schema"]))
    prompt = [
        "# Aesthetic Design System Agent Request",
        f"Task: `{task}`",
        "",
        "## Design-system context",
        system_context(),
        "",
        "## Workflow",
        workflow,
        "",
        "## Project brief",
        json_text(brief),
        "",
        "## Additional input",
        json_text(input_data) if input_data is not None else "None.",
        "",
        "## Required output contract",
        "Return exactly one JSON object and no surrounding Markdown.",
        "The object must conform to this schema:",
        "```json",
        schema.strip(),
        "```",
    ]
    return "\n".join(prompt) + "\n"


def required_fields(value: Dict[str, Any], fields: Iterable[str], label: str) -> List[str]:
    return [f"{label} is missing required field `{field}`" for field in fields if field not in value]


def validate_response(task: str, value: Any) -> List[str]:
    if not isinstance(value, dict):
        return ["Response must be a JSON object"]

    errors: List[str] = []
    if task == "analyze-brief":
        errors.extend(required_fields(value, ["status", "assumptions", "missingInformation"], "Response"))
        if not isinstance(value.get("assumptions"), list):
            errors.append("`assumptions` must be an array")
        if not isinstance(value.get("missingInformation"), list):
            errors.append("`missingInformation` must be an array")
    elif task == "generate-design":
        errors.extend(required_fields(value, ["status", "assumptions", "screens", "components", "tokenMappings", "accessibility", "openQuestions"], "Response"))
        for field in ["assumptions", "screens", "components", "tokenMappings", "accessibility", "openQuestions"]:
            if field in value and not isinstance(value[field], list):
                errors.append(f"`{field}` must be an array")
        for index, screen in enumerate(value.get("screens", [])):
            if not isinstance(screen, dict):
                errors.append(f"screens[{index}] must be an object")
                continue
            errors.extend(required_fields(screen, ["name", "purpose", "layout", "states", "responsive"], f"screens[{index}]"))
    elif task == "audit-design":
        errors.extend(required_fields(value, ["status", "findings", "passedChecks", "priorities", "openQuestions", "verdict"], "Response"))
        if not isinstance(value.get("findings"), list):
            errors.append("`findings` must be an array")
        for index, finding in enumerate(value.get("findings", [])):
            if not isinstance(finding, dict):
                errors.append(f"findings[{index}] must be an object")
                continue
            errors.extend(required_fields(finding, ["severity", "location", "finding", "whyItMatters", "recommendedChange"], f"findings[{index}]"))
    return errors


def command_prompt(args: argparse.Namespace) -> int:
    brief = read_json(Path(args.brief))
    input_data = read_json(Path(args.input)) if args.input else None
    rendered = render_prompt(args.task, brief, input_data)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


def command_validate(args: argparse.Namespace) -> int:
    value = read_json(Path(args.input))
    errors = validate_response(args.task, value)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Valid {args.task} response: {args.input}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    if not args.provider:
        raise ValueError("A provider command is required after `--`, for example: -- opencode ...")
    brief = read_json(Path(args.brief))
    input_data = read_json(Path(args.input)) if args.input else None
    rendered = render_prompt(args.task, brief, input_data)
    completed = subprocess.run(args.provider, input=rendered, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr or f"Provider exited with code {completed.returncode}\n")
        return completed.returncode or 1
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        print(f"ERROR: provider output was not valid JSON: {exc}", file=sys.stderr)
        return 1
    errors = validate_response(args.task, result)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    Path(args.output).write_text(json_text(result), encoding="utf-8")
    print(f"Wrote validated {args.task} response to {args.output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ["prompt", "run"]:
        sub = subparsers.add_parser(command)
        sub.add_argument("--task", choices=sorted(TASKS), required=True)
        sub.add_argument("--brief", required=True, help="Path to a project brief JSON file")
        sub.add_argument("--input", help="Optional JSON input, such as an existing design spec")
        if command == "prompt":
            sub.add_argument("--output")
            sub.set_defaults(function=command_prompt)
        else:
            sub.add_argument("--output", required=True)
            sub.add_argument("provider", nargs=argparse.REMAINDER, help="Provider command after --")
            sub.set_defaults(function=command_run)

    sub = subparsers.add_parser("validate")
    sub.add_argument("--task", choices=sorted(TASKS), required=True)
    sub.add_argument("--input", required=True, help="Path to the provider JSON response")
    sub.set_defaults(function=command_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "provider"):
        args.provider = [item for item in args.provider if item != "--"]
    try:
        return args.function(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
