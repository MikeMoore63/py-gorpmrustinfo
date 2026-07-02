import glob
import json
import os
import sys

from . import get_go_build_info, get_go_mod, get_go_sum, get_rpm_db_info, get_rust_audit


def _default_mode_for_script(script_name):
    name = os.path.basename(script_name or "")
    if name == "get_rpm_info":
        return "rpm"
    if name == "get_rust_audit":
        return "rust"
    return "go-build"


def _dispatch(path, mode):
    if mode == "rpm":
        return get_rpm_db_info(path)
    if mode == "rust":
        return get_rust_audit(path)
    if mode == "go-mod":
        return get_go_mod(path)
    if mode == "go-sum":
        return get_go_sum(path)
    return get_go_build_info(path)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        argv = list(argv)

    script_name = argv[0] if argv else sys.argv[0]
    default_mode = _default_mode_for_script(script_name)
    mode = default_mode
    patterns = []
    args = argv[1:] if len(argv) > 1 else []
    index = 0
    while index < len(args):
        arg = args[index]
        if arg.startswith("--mode="):
            mode = arg.split("=", 1)[1]
        elif arg == "--mode":
            if index + 1 < len(args):
                mode = args[index + 1]
                index += 1
        else:
            patterns.append(arg)
        index += 1

    if not patterns:
        patterns = ["*"]

    for pattern in patterns:
        for file in glob.glob(pattern):
            result = _dispatch(file, mode)
            print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
