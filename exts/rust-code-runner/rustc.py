import json

def print_code_snippet(file_path, line_num, context=3):
    try:
        stripped_lines = []
        with open(file_path, "r") as f:
            lines = f.readlines()
            start = max(line_num - context - 1, 0)  
            end = min(line_num + context, len(lines))
            for i in range(start, end):
                prefix = ">" if i == line_num - 1 else " "
                stripped_lines.append(f"{prefix} {i+1:4}: {lines[i].rstrip()}")
            return "\n".join(stripped_lines)
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")

def parse_rustc_json(stderr: str, file):
    for line in stderr.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("$message_type") != "diagnostic":
            continue

        level = obj.get("level")
        msg = obj.get("message")
        spans = obj.get("spans", [])

        line_num = None
        for span in spans:
            if span.get("is_primary"):
                line_num = span.get("line_start")
                break

        if line_num is not None:
            print(f"{level}: line {line_num}: {msg}")
            diag_f = print_code_snippet(file, line_num) 
            if level == "error":
                print("=========================")
                print(f" {diag_f}")
                print("=========================\n\n")
        else:
            print(f"{level}: {msg}")

import subprocess
def check_rust_test_errors(app, exception):
    rs_path = app.output_rust_file
    result = subprocess.run(
        ["rustc", "--test", "--edition=2021", "--error-format=json", rs_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("--- rustc Errors/Warnings ---")
        parse_rustc_json(result.stderr, app.output_rust_file)
        print("--- rustc Output ---")
        print(result.stdout)

    else:
        print("--- rustc Output  ---")
        print(result.stdout)
        if result.stderr: 
            print("\n\n--- rustc Warnings---")
            print(result.stderr)
