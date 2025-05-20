# SPDX-License-Identifier: MIT OR Apache-2.0
# SPDX-FileCopyrightText: The Coding Guidelines Subcommittee Contributors

import re
from sphinx.errors import SphinxError
from sphinx_needs.data import SphinxNeedsData
import logging

logger = logging.getLogger('sphinx')

class ExecuteRustExamples(SphinxError):
    category = "Integrity Check Error"

def execute_tests(app, env):
    """
    Aggregate and test rust examples
    """
    logger.debug("Testing examples")
    data = SphinxNeedsData(env)
    needs = data.get_needs_view()

    required_fields = app.config.required_guideline_fields  # Access the configured values

    for key, value in needs.items():
        print("======++++++++")

        # print(key, " -- ", value)
        if key.startswith("non_compl_ex") or key.startswith("compl_ex"):

            text = value.get("content", "")
            match = re.search(
                r"\.\. code-block:: rust\s*\n\n((?: {2,}.*\n?)+)", text, re.DOTALL
            )
            if match:
                code_block = match.group(1)
                code_lines = [line[2:] if line.startswith("  ") else line for line in code_block.splitlines()]
                rust_code = "\n".join(code_lines)
                print("Extracted Rust code:\n")
                print(rust_code)
            else:
                print("No Rust code block found.")
