#!/usr/bin/env python3

from argparse import ArgumentParser
import json
from statistics import mode

def parse_opts():
    parser = ArgumentParser(prog="image-meta")

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="The path to specific dockerfile",
    )

    parser.add_argument(
        "-r",
        "--repo",
        type=str,
        help="The image repo (such as `apache/spark`)",
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="tag",
        help="The mode of print image meta. (tag/manifest)",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="versions.json",
        help="The version json of image meta.",
    )

    args, unknown = parser.parse_known_args()
    if unknown:
        parser.error("Unsupported arguments: %s" % " ".join(unknown))
    return args

def main():
    opts = parse_opts()
    filepath = opts.path
    repo = opts.repo
    mode = opts.mode
    version_file = opts.file

    if mode == "tag":
        tags = []
        with open(version_file, "r") as f:
            versions = json.load(f).get("versions")
            for v in versions:
                if v.get("path") == filepath:
                    tags = v.get("tags")
        print(",".join([ "%s:%s" % (repo, t) for t in tags]))
    elif mode == "manifest":
        with open(version_file, "r") as f:
            versions = json.load(f).get("versions")
            for v in versions:
                print(v)


if __name__ == "__main__":
    main()
