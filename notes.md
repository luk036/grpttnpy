## View Profile and Call Tree

```
> sudo apt install kcachegrind
> sudo apt install kcachegrind-converters
> easy_install pyprof2calltree
> python -m cProfile -o profile_data.pyprof grpttnpy/tests/test_FDBiPartMgr.py
> pyprof2calltree -i profile_data.pyprof -k
```
