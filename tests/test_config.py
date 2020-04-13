import json

import pytest
import yaml

from taskchain.task import Config


def test_name(tmp_path):
    data = {}
    json.dump(data, (tmp_path / 'json_test.json').open('w'))
    yaml.dump(data, (tmp_path / 'yaml.test.yaml').open('w'))

    with pytest.raises(ValueError):
        _ = Config(tmp_path)

    c = Config(tmp_path, name='test')
    assert c.name == 'test'

    c = Config(tmp_path, name='test2')
    assert c.name == 'test2'

    c = Config(tmp_path, tmp_path / 'json_test.json')
    assert c.name == 'json_test'

    c = Config(tmp_path, tmp_path / 'yaml.test.yaml')
    assert c.name == 'yaml.test'

    c = Config(tmp_path, tmp_path / 'yaml.test.yaml', name='name_test')
    assert c.name == 'name_test'


def test_data(tmp_path):
    with pytest.raises(ValueError):
        _ = Config(tmp_path, name='test').data

    data = """{"a": 1, "b": 2, "c": {"d": 3}}"""
    with (tmp_path / 'json_test.json').open('w') as f:
        f.write(data)

    data = """
    a: 1
    b: 2
    c: 
        d: 3
    """
    with (tmp_path / 'yaml.test.yaml').open('w') as f:
        f.write(data)

    json_c = Config(tmp_path, tmp_path / 'json_test.json')
    yaml_c = Config(tmp_path, tmp_path / 'yaml.test.yaml')
    data_c = Config(tmp_path, data={"a": 1, "b": 2, "c": {"d": 3}}, name='test')

    for c in [json_c, yaml_c, data_c]:
        assert c.data['a'] == 1
        assert c.data['b'] == 2
        assert c.data['c']['d'] == 3

        assert c['a'] == 1
        assert c['b'] == 2
        assert c['c']['d'] == 3

        assert c.a == 1
        assert c.b == 2
        assert c.c['d'] == 3

        assert c.get('a') == 1
        assert c.get('x', 9) == 9

        with pytest.raises(KeyError):
            _ = c['x']

        with pytest.raises(KeyError):
            _ = c.data['x']

        with pytest.raises(KeyError):
            _ = c.x


def test_context(tmp_path):
    config = Config(tmp_path, data={'a': '{A}/{B}.{B}', 'b': '{B}'}, context={'B': 2}, name='config')
    assert config['a'] == '{A}/2.2'
    assert config['b'] == '2'

    config = Config(tmp_path, data={'a': '{A}/{B}.{B}', 'b': '{B}'}, context={'A': '1', 'B': '2'}, name='config')
    assert config['a'] == '1/2.2'
    assert config['b'] == '2'


class MyObject:
    def __init__(self, a, b=1):
        self.a = a
        self.b = b


def test_config_objects(tmp_path):

    data = {
        'my_object': {
            'class': 'tests.test_config.MyObject',
            'args': [7],
            'kwargs': {'b': 13},
        }
    }

    config = Config(tmp_path, data=data, name='config')
    assert 'my_object' in config
    assert 'my_object' in config.objects
    assert config['my_object'] == config.objects['my_object']
    assert type(config['my_object']) == MyObject
    assert config['my_object'].a == 7
    assert config['my_object'].b == 13
