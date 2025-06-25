import json
import subprocess

def print_code_snippet(file_path, line_num, context=3):
    """
    Prints a code snippet from a file with context around a specific line.

    This function is typically used to display source code around an error line
    for better debugging and error reporting.

    Args:
        file_path (str): Path to the source file.
        line_num (int): The line number where the error occurred (1-based index).
        context (int, optional): The number of lines to display before and after
            the error line. Defaults to 3.

    Returns:
        None
    """
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
    """
    Parses the JSON diagnostics output from `rustc`.

    This function takes the standard error output (in JSON format) from the Rust compiler (`rustc`)
    and processes it, possibly filtering or reporting diagnostics relevant to the specified file.

    Args:
        stderr (str): The JSON-formatted stderr output from `rustc`.
        file: The file object or path that the diagnostics should relate to.

    Returns:
        Any
    """
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


def check_rust_test_errors(app, exception):
   """
    Sphinx 'build-finished' event handler that compiles the generated Rust file in test mode.

    This function is connected to the Sphinx build lifecycle and is executed after the build finishes.
    It invokes `rustc` in test mode on the generated Rust file and reports any compilation or test-related
    errors.

    Args:
        app: The Sphinx application object. Must have an `output_rust_file` attribute containing
             the path to the generated Rust source file.
        exception: Exception raised during the build process, or None if the build completed successfully.

    """
    rs_path = app.output_rust_file
    # Run the Rust compiler in test mode with JSON error output format.
    # capturing stdout and stderr as text.
    result = subprocess.run(
        ["rustc", "--test", "--edition=2024", "--error-format=json", rs_path],
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
