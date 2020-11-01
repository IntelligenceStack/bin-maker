# Bin-Maker

> Bin-Maker only suppory Python3

bin-maker is a Python compile tools,which can help us protect and speed up python code

## Benefits of using Bin-Maker

* cythonize source code：protect python source code.on windows,bin-maker will compile code to `.pyd`, on linux,bin-maker will compile code to `.so`
* Get performance improvement: be able to improve the performance of Python code without any code level optimization

## Quick Start

```
pip3 install bin-maker
```

## Compile Source Coude

```
bin-maker-build build_ext
```
when compile finish,will generate `.so` or `.pyd` file in `./build/lib*`

## Release Application

```
bin-maker-release
```
when code build finish,we can use `bin-maker-release` to release our application,source code will be `remove` and copy the `.so` or `.pyd` file to source code path,only use in production enviremont

## Package with PyInstaller
```
bin-maker-package
```

# Config

When there are custom parameters, you can create a new configuration file in the project root directory

`bin_maker.json`
```
{
  "exclude_modules": [],
  "exclude_files": [],
  "with_scikit": "false",
  "with_statics_model": "false"
}
```

Name|Description
-------|------|
exclude_modules|Modules not involved in compilation
exclude_files|Files not involved in compilation (regular expressions)
with_scikit|Is sklearn's package implicitly imported when pyinstaller is packaged
with_statics_model|Whether to import statics package implicitly when pyinstaller is packaged

# Performance comparison

```
import time

def run():
    time_start = time.time()
    import sys

    def make_tree(depth):
        if not depth: return None, None
        depth -= 1
        return make_tree(depth), make_tree(depth)

    def check_tree(node):
        (left, right) = node
        if not left: return 1
        return 1 + check_tree(left) + check_tree(right)

    min_depth = 4
    max_depth = max(min_depth + 2, 17)
    stretch_depth = max_depth + 1

    print("stretch tree of depth %d\t check:" %
          stretch_depth, check_tree(make_tree(stretch_depth)))

    long_lived_tree = make_tree(max_depth)

    iterations = 2 ** max_depth

    for depth in range(min_depth, stretch_depth, 2):

        check = 0
        for i in range(1, iterations + 1):
            check += check_tree(make_tree(depth))

        print("%d\t trees of depth %d\t check:" % (iterations, depth), check)
        iterations //= 4

    print("long lived tree of depth %d\t check:" %
          max_depth, check_tree(long_lived_tree))

    time_end = time.time()
    print('time cost', time_end - time_start, 's')
```

## Pure Python
```
stretch tree of depth 18	 check: 524287
131072	 trees of depth 4	 check: 4063232
32768	 trees of depth 6	 check: 4161536
8192	 trees of depth 8	 check: 4186112
2048	 trees of depth 10	 check: 4192256
512	 trees of depth 12	 check: 4193792
128	 trees of depth 14	 check: 4194176
32	 trees of depth 16	 check: 4194272
long lived tree of depth 17	 check: 262143
time cost 11.279994249343872 s
```

## Compile after Bin-Maker
```
stretch tree of depth 18	 check: 524287
131072	 trees of depth 4	 check: 4063232
32768	 trees of depth 6	 check: 4161536
8192	 trees of depth 8	 check: 4186112
2048	 trees of depth 10	 check: 4192256
512	 trees of depth 12	 check: 4193792
128	 trees of depth 14	 check: 4194176
32	 trees of depth 16	 check: 4194272
long lived tree of depth 17	 check: 262143
time cost 1.9600331783294678 s
```

After compilation, the performance is improved nearly 6 times