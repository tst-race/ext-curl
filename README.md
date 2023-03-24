# curl for RACE

This repo provides scripts to custom-build the
[curl library](https://curl.se) for RACE.

## License

The curl library is licensed under a MIT/X derivative license.

Only the build scripts in this repo are licensed under Apache 2.0.

## Dependencies

Curl has no dependencies on any custom-built libraries.

## How To Build

The [ext-builder](https://github.com/tst-race/ext-builder) image is used to
build curl.

```
git clone https://github.com/tst-race/ext-builder.git
git clone https://github.com/tst-race/ext-curl.git
./ext-builder/build.py \
    --target linux-x86_64 \
    ./ext-curl
```

## Platforms

Curl is built for the following platforms:

* `android-x86_64`
* `android-arm64-v8a`

It is also used on Linux but can be installed via `apt`.

## How It Is Used

Curl is used by the exemplar C++ channel and artifact manager plugin.
