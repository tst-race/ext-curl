#!/usr/bin/env python3

#
# Copyright 2023 Two Six Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Script to build curl for RACE
"""

import logging
import os
import race_ext_builder as builder


def get_cli_arguments():
    """Parse command-line arguments to the script"""
    parser = builder.get_arg_parser(
        "curl",
        "7.58.0",
        1,
        __file__,
        [builder.TARGET_ANDROID_x86_64, builder.TARGET_ANDROID_arm64_v8a],
    )
    return builder.normalize_args(parser.parse_args())


if __name__ == "__main__":
    args = get_cli_arguments()
    builder.make_dirs(args)
    builder.setup_logger(args)

    builder.install_packages(
        args,
        [
            "automake=1:1.16.1*",
            "libtool=2.4.6*",
        ],
    )

    builder.fetch_source(
        args=args,
        source=f"https://github.com/curl/curl/archive/refs/tags/curl-{args.version.replace('.', '_')}.tar.gz",
        extract="tar.gz",
    )

    source_dir = os.path.join(
        args.source_dir, f"curl-curl-{args.version.replace('.', '_')}"
    )
    env = builder.create_standard_envvars(args)

    logging.root.info("Configuring build")
    builder.execute(
        args,
        [
            "autoreconf",
            "--install",
        ],
        cwd=source_dir,
        env=env,
    )

    target = "x86_64-linux-android" if "x86" in args.target else "aarch64-linux-android"
    builder.execute(
        args,
        [
            "./configure",
            "--prefix=/",
            f"--host={target}",
            f"--target={target}",
            "--disable-shared",
            "--without-zlib",
            "--without-idn",
        ],
        cwd=source_dir,
        env=env,
    )

    logging.root.info("Building")
    builder.execute(
        args,
        [
            "make",
            "-j",
            args.num_threads,
        ],
        cwd=source_dir,
        env=env,
    )
    builder.execute(
        args,
        [
            "make",
            f"DESTDIR={args.install_dir}",
            "install",
        ],
        cwd=source_dir,
        env=env,
    )

    builder.create_package(args)
