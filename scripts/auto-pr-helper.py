import json
import re
import random 
import string

import sys, os

scriptpath = "../"
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(parent_dir)

from generate_guideline_templates import generate_id, guideline_rst_template, issue_header_map


def extract_form_fields(issue_body: str) -> dict:
    """
    This function parses issues json into a dict of important fields
    """

    fields = {v: "" for v in issue_header_map.values()}

    lines = issue_body.splitlines()
    current_key = None
    current_value_lines = []

    lines.append("### END")  # Sentinel to process last field

    # Look for '###' in every line, ### represent a sections/field in a guideline
    for line in lines:
        header_match = re.match(r'^### (.+)$', line.strip())
        if header_match:
            # Save previous field value if any
            if current_key is not None:
                value = "\n".join(current_value_lines).strip()
                # `_No response_` represents an empty field
                if value == "_No response_":
                    value = ""
                if current_key in fields:
                    fields[current_key] = value

            header = header_match.group(1).strip()
            current_key = issue_header_map.get(header)  # Map to dict key or None if unknown
            current_value_lines = []
        else:
            current_value_lines.append(line)

    return fields

def save_guideline_file(content: str, chapter: str):
    """
    Appends a guideline to a chapter
    """
    filename = f"src/coding-guidelines/{chapter.lower().replace(' ', '-')}.rst"

    # for testing in the GA summary 
    print("=====CONTENT=====")
    print(content)
    print("=====CONTENT=END=====")

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved guideline to {filename}")

def guideline_template(fields: dict) -> str:
    """
    This function turns a dictionary that contains the guideline fields 
    into a proper .rst guideline format
    """
    

    # generate random ids
    guideline_id = generate_id("gui")
    rationale_id = generate_id("rat")
    non_compliant_example_id = generate_id("non_compl_ex")
    compliant_example_id = generate_id("compl_ex")

    def get(key):
        return fields.get(key, "").strip()

    def format_code_block(code: str, lang: str = "rust") -> str:
        lines = code.strip().splitlines()
        if lines and lines[0].strip().startswith("```"):
            # Strip the ```rust and ``` lines
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
        indented_code = "\n".join(f"         {line}" for line in lines)  # indentation 
        return f"\n\n{indented_code}\n"

    guideline_text = guideline_rst_template(
        guideline_title=get("guideline_title"),
        category=get("category"),
        status=get("status"),
        release_begin=get("release_begin"),
        release_end=get("release_end"),
        fls_id=get("fls_id"),
        decidability=get("decidability"),
        scope=get("scope"),
        tags=get("tags"),
        amplification=get("amplification"),
        rationale=get("rationale"),
        non_compliant_ex_prose=get("non_compliant_ex_prose"),
        non_compliant_ex=format_code_block(get("non_compliant_ex")),
        compliant_example_prose=get("compliant_example_prose"),
        compliant_example=format_code_block(get("compliant_example"))
    )

    return guideline_text

import sys
if __name__ == "__main__":

    ## locally test with `cat scripts/test_issue_sample.json | python3 scripts/auto-pr-helper.py`
    ## or use `curl https://api.github.com/repos/rustfoundation/safety-critical-rust-coding-guidelines/issues/135 | uv run python scripts/auto-pr-helper.py`


    # Read json from stdin
    stdin_issue_json = sys.stdin.read()
    json_issue = json.loads(stdin_issue_json)

    issue_number = json_issue['number']
    issue_title = json_issue['title']
    issue_body = json_issue['body']
    fields = extract_form_fields(issue_body)
    chapter = fields["chapter"]
    content = guideline_template(fields)
    save_guideline_file(content, chapter)
