import argparse
import json
import platform
import shlex
import subprocess
import os


def _section_match(s1, s2):
    return str(s1) == str(s2) or (s1 is None and s2 is None)


def _row_match(r1, r2):
    return str(r1) == str(r2) or (r1 is None and r2 is None)


def grade_match(match, verbose=False):
    e_sid = match["expected"]["section_id"]
    e_rid = match["expected"]["row_id"]
    e_valid = match["expected"]["valid"]

    o_sid = match["output"]["section_id"]
    o_rid = match["output"]["row_id"]
    o_valid = match["output"]["valid"]

    i_s = match["input"]["section"]
    i_r = match["input"]["row"]

    # if expected is valid...
    sm = _section_match(e_sid, o_sid)
    rm = _row_match(e_rid, o_rid)
    vm = e_valid == o_valid
    pts = 0

    if e_valid:
        if sm and rm and vm:
            if verbose:
                print(".. ok")
            pts = 1

        if not vm:
            if verbose:
                print(f".. {i_s}:{i_r} marked invalid, should be {e_sid}:{e_rid}")
            pts = 0

        if vm and (not sm or not rm):
            if verbose:
                print(f".. {i_s}:{i_r} WRONG!, marked {o_sid}:{o_rid}, should be {e_sid}:{e_rid}")
            pts = -5

    if not e_valid:
        if not o_valid:
            if verbose:
                print(".. ok")
            pts = 1

        else:
            if verbose:
                print(f".. {i_s}:{i_r} WRONG! Marked valid, should be invalid")
            pts = -5
    return pts


def parse_output(k):
    stdout_output = k[0]

    lines = stdout_output.splitlines()
    valid_lines = []
    for line in lines:
        try:
            data = json.loads(line.strip())
            if "expected" in data and "output" in data and "input" in data:
                valid_lines.append(data)
        except:
            pass
    return valid_lines


def escape(filepath):
    return filepath.replace(" ", "\\ ")


def grade(path_to_manifest, path_to_input, path_to_executable, verbose=False, is_windows=False):
    _manifest = os.path.abspath(path_to_manifest)
    _input = os.path.abspath(path_to_input)
    _executable = os.path.abspath(path_to_executable)

    cmd = "{} --manifest {} --input {}".format(escape(_executable), escape(_manifest), escape(_input))

    if is_windows:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        args = shlex.split(cmd)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    k = p.communicate()
    valid_lines = parse_output(k)

    total_pts = 0
    max_pts = 0
    for match in valid_lines:
        pts = grade_match(match, verbose=verbose)
        max_pts += 1
        total_pts += pts

    print(f"{total_pts} / {max_pts}")
    return total_pts, max_pts


def grade_python(path_to_manifest, path_to_input, verbose=False, is_windows=False):
    executable = "python/normalize.cmd" if is_windows else "python/normalize"
    grade(path_to_manifest, path_to_input, executable, verbose=verbose, is_windows=is_windows)


def grade_ruby(path_to_manifest, path_to_input, verbose=False, is_windows=False):
    executable = "ruby/normalize.cmd" if is_windows else "ruby/normalize"
    grade(path_to_manifest, path_to_input, executable, verbose=verbose, is_windows=is_windows)


def grade_csharp(path_to_manifest, path_to_input, verbose=False, is_windows=False):
    executable = "csharp/normalize.cmd" if is_windows else "csharp/normalize"
    grade(path_to_manifest, path_to_input, executable, verbose=verbose, is_windows=is_windows)


def grade_java(path_to_manifest, path_to_input, verbose=False, is_windows=False):
    executable = "java/normalize.cmd" if is_windows else "java/normalize"
    grade(path_to_manifest, path_to_input, executable, verbose=verbose, is_windows=is_windows)


def grade_php(path_to_manifest, path_to_input, verbose=False, is_windows=False):
    executable = "php/normalize.cmd" if is_windows else "php/normalize"
    grade(path_to_manifest, path_to_input, executable, verbose=verbose, is_windows=is_windows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="grader for SeatGeek SectionNormalization code test")
    parser.add_argument("--manifest", default=None, help="path to manifest file")
    parser.add_argument("--input", default=None, help="path to input file")
    parser.add_argument("--lang", default="python")
    parser.add_argument("--verbose", action="store_true", default=False)

    args = parser.parse_args()
    is_windows = platform.system() == "Windows"

    assert args.lang in ("python", "ruby", "c#", "java", "php")
    assert args.manifest and args.input

    if args.lang == "python":
        grade_python(args.manifest, args.input, args.verbose, is_windows)

    if args.lang == "ruby":
        grade_ruby(args.manifest, args.input, args.verbose, is_windows)

    if args.lang == "c#":
        grade_csharp(args.manifest, args.input, args.verbose, is_windows)

    if args.lang == "java":
        grade_java(args.manifest, args.input, args.verbose, is_windows)

    if args.lang == "php":
        grade_php(args.manifest, args.input, args.verbose, is_windows)
