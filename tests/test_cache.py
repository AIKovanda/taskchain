import numpy as np
import pandas as pd
import pytest

from taskchain.cache import InMemoryCache, cached, NumpyArrayCache, JsonCache, DataFrameCache


def test_cache_decorator():
    external_cache = InMemoryCache()
    external_cache2 = InMemoryCache()

    class CachedClass:
        def __init__(self):
            self.cache = InMemoryCache()

        @cached()
        def cached_method(self, parameter_1, parameter_2, key_parameter_1=10, key_parameter_2=20):
            return parameter_1 + parameter_2 + key_parameter_1 + key_parameter_2

        @cached(external_cache)
        def cached_method2(self, parameter_1, parameter_2, key_parameter_1=10, key_parameter_2=20):
            return parameter_1 + parameter_2 + key_parameter_1 + key_parameter_2

        @cached(external_cache2)
        def cached_method3(self, parameter_1, parameter_2, key_parameter_1=10, key_parameter_2=20):
            return parameter_1 + parameter_2 + key_parameter_1 + key_parameter_2

    obj = CachedClass()

    for cache, method in [
        (obj.cache, obj.cached_method),
        (external_cache, obj.cached_method2),
        (external_cache2, obj.cached_method3),
    ]:
        assert len(cache._memory) == 0
        assert method(1, 2) == 33
        memory = next(iter(cache._memory.values()))
        assert len(memory) == 1

        assert method(1, 2) == 33
        assert len(memory) == 1

        assert method(1, 2, 10, 20) == 33
        assert len(memory) == 1

        assert method(1, 2, 10, parameter_2=20) == 33
        assert len(memory) == 1

        assert method(1, 2, 20, 10) == 33
        assert len(memory) == 2


@pytest.mark.parametrize('cache_class,value,test', [
    (JsonCache, lambda: 'value', lambda v: v == 'value'),
    (JsonCache, lambda: {'a': 3}, lambda v: v['a'] == 3),
    (JsonCache, lambda: None, lambda v: v is None),
    (NumpyArrayCache, lambda: np.zeros(10), lambda v: v.shape == (10,)),
    (DataFrameCache, lambda: pd.DataFrame(np.zeros((10, 10))), lambda v: v.values.shape == (10, 10)),
])
def test_cache(tmp_path, cache_class, value, test):
    class Example:
        counter = 0
        def fce(self):
            self.counter += 1
            return value()

    example = Example()
    cache = cache_class(tmp_path)
    assert test(cache.get_or_compute('key', example.fce))
    assert example.counter == 1
    assert test(cache.get_or_compute('key', example.fce))
    assert example.counter == 1
