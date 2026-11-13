---
name: notebooks
description: Jupyter notebooks in the owner's research projects. Use when presenting an analysis or results as an `.ipynb`, running a notebook, or opening one for the owner to run cells in T3.
---

# Jupyter notebooks

A notebook is a deliverable the owner opens in T3: Markdown stating the question, data sources, method and limits, then code cells that reproduce the result. T3's native notebook tools and viewer share one document and kernel owner when the project has notebook execution configured. Hand over saved, fresh outputs and state any execution limits.

## Native tools

Prefer the connected `notebook_*` tools when available. They use the authenticated thread's project and workspace, including scheduled agents; pass relative notebook paths.

1. Use `notebook_create` with a valid nbformat 4 document, or `notebook_open` for the current document, stable cell IDs, revision and disk hash.
2. Use `notebook_edit_cells` for ordered insert/update/delete/move operations with the expected revision. Preserve existing metadata and unrelated cells.
3. Execute only when the task authorizes code execution: `notebook_run` takes selected code-cell IDs or explicit `all=true`, the current revision and a unique request ID. Reuse that ID only for identical retries.
4. Read `notebook_read_outputs` for status, execution/source provenance and truncation. Follow output cursors within the byte limit; use `afterSequence` to await changes instead of busy polling. An unknown outcome requires explicit restart or shutdown before another run; never infer success or automatically replay code.
5. Save with `notebook_save`, passing current revision and base disk hash. A conflict preserves the draft: reconcile the external change before saving. Done means saved outputs are fresh for the intended code cells, warnings and truncation are reported, and the owner has the file link.

Use `notebook_list_kernels` to inspect available specs and owned kernels. Interrupt cancels the remaining run; wait for terminal status. Restart clears variables and preserves previous-generation outputs. Shutdown stops only the owned kernel and retains the draft for saving. Runtime permission refusals are limits to report, not a reason to bypass the tools through a shell.

## Interim fallback

When native tools are absent or execution is not configured, use the project's existing headless environment or JupyterLab script. Avoid a second writer while a native session or JupyterLab is editing or executing the notebook.

## Build and run one

1. Write a valid nbformat 4 `.ipynb` in the project's usual results or notebook location, with stable cell ids. When updating an existing notebook, keep its metadata and cells. Credentials and token URLs stay out of it.
2. From the project root, run the whole notebook in place with the project's own environment:

   ```sh
   uv run --no-sync --with jupyterlab jupyter nbconvert --to notebook --execute --inplace <file>
   ```

   `--no-sync` keeps the project environment exactly as it is. If an import fails, report the missing package rather than switching to another Python.
3. Done when the saved file holds fresh outputs for every code cell and you have read any warnings. On failure, report the failing cell and its error, and say whether the outputs on disk are stale.
4. Give the owner the file link. It opens in T3's file viewer with the saved outputs.

## Interactive work

Each research project has a **JupyterLab** project script that opens JupyterLab in T3's in-app browser, on loopback with its own token:

| Project | Port |
|---|---|
| Lithium_Extraction | 8891 |
| ePC-SAFT | 8892 |
| Amine-Thermodynamics | 8893 |
| MEA-Absorption-Column | 8894 |

Start it with that script and use its browser tab. It keeps the token, the `127.0.0.1` binding and the lifecycle; stopping the script's terminal stops the server. Run a notebook headless only while nobody has it open there, so two writers never touch the same file.
