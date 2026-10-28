---
name: jupyter-notebooks
description: Jupyter notebooks in the owner's research projects. Use when presenting an analysis or results as an `.ipynb`, running a notebook, or opening one for the owner to run cells in T3.
---

# Jupyter notebooks

A notebook is a deliverable the owner opens in T3: Markdown stating the question, data sources, method and limits, then code cells that reproduce the result. T3's file viewer shows a notebook's **saved outputs**; it does not run cells yet (tannerpolley/t3code#208). So a notebook you hand over is always one you have already run.

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
