from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import SchemaError
from jsonschema.validators import validator_for

from .jsonio import load_json


def check_schema_documents(repository_root: Path) -> list[str]:
	errors: list[str] = []
	for path in sorted((repository_root / "schemas").glob("*.schema.json")):
		schema = load_json(path)
		validator_class = validator_for(schema)
		try:
			validator_class.check_schema(schema)
		except SchemaError as error:
			errors.append(f"{path.relative_to(repository_root).as_posix()} $: invalid JSON Schema: {error.message}")
	return errors


def validate_against_schema(instance: Any, schema_path: Path, label: str) -> list[str]:
	schema = load_json(schema_path)
	validator_class = validator_for(schema)
	validator = validator_class(schema)
	errors: list[str] = []
	for error in sorted(validator.iter_errors(instance), key=lambda item: (list(item.absolute_path), item.message)):
		path = "$"
		for component in error.absolute_path:
			path += f"[{component}]" if isinstance(component, int) else f".{component}"
		errors.append(f"{label} {path}: {error.message}")
	return errors
