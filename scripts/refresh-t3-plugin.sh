#!/usr/bin/env bash
# Both agents install a copy of the plugin (Claude pins it to a commit, Codex copies the folder),
# so run this from the main checkout after merging any change under t3-code-plugin/.
set -euo pipefail
claude plugin marketplace update tannerpolley-skills
claude plugin update t3-code@tannerpolley-skills
codex plugin add t3-code@tannerpolley-skills
