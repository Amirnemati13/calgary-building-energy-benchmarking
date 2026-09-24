"""Check notebook syntax, language parity and saved execution state."""
import ast
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
programs = []
for language in ["en", "fa"]:
    notebook = json.loads((root / f"notebooks/analysis.{language}.ipynb").read_text(encoding="utf-8"))
    code = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            if isinstance(source, list):
                source = "".join(source)
            ast.parse(source)
            code.append(source)
            assert not any(o["output_type"] == "error" for o in cell["outputs"])
    programs.append(code)
assert programs[0] == programs[1], "Language editions must execute identical code"
print(f"Checked {len(programs[0])} code cells per language; code is identical.")
