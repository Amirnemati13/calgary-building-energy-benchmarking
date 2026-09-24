"""Execute the analysis notebook and preserve its tables and figures.

This runner executes local notebook code in order. Run only notebooks you trust.
It avoids a separate Jupyter server; JupyterLab remains suitable for interactive use.
"""

import argparse
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import traceback


def run(path):
    path = Path(path).resolve()
    root = Path(__file__).resolve().parents[1]
    os.environ.setdefault("MPLCONFIGDIR", str(root / ".cache/matplotlib"))
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.chdir(root)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__"}
    count = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        count += 1
        outputs, stream = [], io.StringIO()

        def flush():
            if stream.tell():
                outputs.append({"output_type": "stream", "name": "stdout", "text": stream.getvalue()})
                stream.seek(0)
                stream.truncate(0)

        def display(obj):
            flush()
            from matplotlib.figure import Figure
            if isinstance(obj, Figure):
                buffer = io.BytesIO()
                obj.savefig(buffer, format="png", dpi=110, bbox_inches="tight")
                data = {"image/png": base64.b64encode(buffer.getvalue()).decode(), "text/plain": "<Matplotlib figure>"}
            else:
                data = {"text/plain": str(obj)}
                if hasattr(obj, "_repr_html_"):
                    html = obj._repr_html_()
                    if html is not None:
                        data["text/html"] = html
            outputs.append({"output_type": "display_data", "data": data, "metadata": {}})

        namespace["display"] = display
        print(f"Executing cell {count}", flush=True)
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)
        try:
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                exec(compile(source, f"notebook_cell_{count}", "exec"), namespace)
        except Exception as error:
            flush()
            outputs.append({"output_type": "error", "ename": type(error).__name__,
                            "evalue": str(error), "traceback": traceback.format_exc().splitlines()})
            cell.update(outputs=outputs, execution_count=count)
            path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        flush()
        cell.update(outputs=outputs, execution_count=count)
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Executed {count} code cells successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    run(parser.parse_args().notebook)
