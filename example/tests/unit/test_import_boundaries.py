"""Static import boundary checks for domain and ports layers."""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = REPO_ROOT / "src" / "llm_wiki"
FORBIDDEN_PREFIXES = (
    "llm_wiki.adapters",
    "httpx",
    "openai",
    "anthropic",
    "typer",
)


def _iter_core_modules() -> list[Path]:
    modules: list[Path] = []
    for layer in ("domain", "ports"):
        root = CORE_ROOT / layer
        modules.extend(sorted(root.rglob("*.py")))
    return modules


def _imports_in_module(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    return imported


def _find_forbidden_imports() -> list[str]:
    violations: list[str] = []
    for module_path in _iter_core_modules():
        rel = module_path.relative_to(REPO_ROOT)
        for imported in _imports_in_module(module_path):
            for prefix in FORBIDDEN_PREFIXES:
                if imported == prefix or imported.startswith(f"{prefix}."):
                    violations.append(f"{rel}: {imported}")
    return violations


def no_adapter_imports_in_core_D1() -> None:
    """Domain and ports do not import adapters or I/O libraries."""
    violations = _find_forbidden_imports()
    assert violations == [], f"forbidden imports: {violations}"


def domain_ports_no_adapters_F1() -> None:
    """F1 — domain/ and ports/ never import llm_wiki.adapters."""
    violations = [
        entry
        for entry in _find_forbidden_imports()
        if entry.startswith(("src/llm_wiki/domain/", "src/llm_wiki/ports/"))
        and "llm_wiki.adapters" in entry
    ]
    assert violations == [], f"adapter imports in core layers: {violations}"


def core_isolation_Y6() -> None:
    """Section 4 Y6 — core layers remain adapter-free."""
    assert _find_forbidden_imports() == []


def use_cases_no_adapters_E1() -> None:
    """Use case modules do not import adapters or read os.environ."""
    use_cases_root = CORE_ROOT / "domain" / "use_cases"
    violations: list[str] = []
    for module_path in sorted(use_cases_root.rglob("*.py")):
        rel = module_path.relative_to(REPO_ROOT)
        source = module_path.read_text(encoding="utf-8")
        if "os.environ" in source:
            violations.append(f"{rel}: os.environ")
        for imported in _imports_in_module(module_path):
            if imported == "llm_wiki.adapters" or imported.startswith("llm_wiki.adapters."):
                violations.append(f"{rel}: {imported}")
    assert violations == [], f"forbidden use case imports: {violations}"


def ingest_use_case_no_adapters_E1() -> None:
    """IngestUseCase module does not import adapters or read os.environ."""
    ingest_module = CORE_ROOT / "domain" / "use_cases" / "ingest.py"
    source = ingest_module.read_text(encoding="utf-8")
    violations: list[str] = []
    if "os.environ" in source:
        violations.append(f"{ingest_module.relative_to(REPO_ROOT)}: os.environ")
    for imported in _imports_in_module(ingest_module):
        if imported == "llm_wiki.adapters" or imported.startswith("llm_wiki.adapters."):
            violations.append(f"{ingest_module.relative_to(REPO_ROOT)}: {imported}")
    assert violations == [], f"forbidden ingest use case imports: {violations}"


def query_use_case_no_adapters_E1() -> None:
    """QueryUseCase module does not import adapters or read os.environ."""
    query_module = CORE_ROOT / "domain" / "use_cases" / "query.py"
    source = query_module.read_text(encoding="utf-8")
    violations: list[str] = []
    if "os.environ" in source:
        violations.append(f"{query_module.relative_to(REPO_ROOT)}: os.environ")
    for imported in _imports_in_module(query_module):
        if imported == "llm_wiki.adapters" or imported.startswith("llm_wiki.adapters."):
            violations.append(f"{query_module.relative_to(REPO_ROOT)}: {imported}")
    assert violations == [], f"forbidden query use case imports: {violations}"


_RAG_FORBIDDEN = (
    "chromadb",
    "faiss",
    "langchain",
    "numpy",
    "openai",
    "pinecone",
    "sentence_transformers",
    "sklearn",
    "torch",
    "transformers",
    "vector",
)


def lint_use_case_no_adapters_E1() -> None:
    """LintUseCase module does not import adapters or read os.environ."""
    lint_module = CORE_ROOT / "domain" / "use_cases" / "lint.py"
    source = lint_module.read_text(encoding="utf-8")
    violations: list[str] = []
    if "os.environ" in source:
        violations.append(f"{lint_module.relative_to(REPO_ROOT)}: os.environ")
    for imported in _imports_in_module(lint_module):
        if imported == "llm_wiki.adapters" or imported.startswith("llm_wiki.adapters."):
            violations.append(f"{lint_module.relative_to(REPO_ROOT)}: {imported}")
    assert violations == [], f"forbidden lint use case imports: {violations}"


def query_no_rag_imports_Y3() -> None:
    """Query use case and prompts modules do not import RAG/vector dependencies."""
    modules = [
        CORE_ROOT / "domain" / "use_cases" / "query.py",
        CORE_ROOT / "domain" / "prompts" / "query.py",
    ]
    violations: list[str] = []
    for module_path in modules:
        rel = module_path.relative_to(REPO_ROOT)
        for imported in _imports_in_module(module_path):
            base = imported.split(".", 1)[0]
            if base in _RAG_FORBIDDEN or any(token in imported for token in _RAG_FORBIDDEN):
                violations.append(f"{rel}: {imported}")
    assert violations == [], f"forbidden RAG imports: {violations}"
