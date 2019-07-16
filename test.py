import pytest
from nest import make_nested_dicts, dictify, DictifyError


@pytest.fixture(scope='function')
def input_list():
    return [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9
        }
    ]


@pytest.fixture(scope='function')
def input_list_bad():
    return [
        {
            "country": "US",
            "city": "Boston",
            "amount": 100
        },
        {
            "country": "FR",
            "city": "Paris",
            "amount": 20
        },
        {
            "country": "FR",
            "city": "Lyon",
            "amount": 11.4
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9
        }
    ]


expected_result = {
    "EUR": {
      "ES": {
          "Madrid": [
              {
                "amount": 8.9
              }
          ]
      },
      "FR": {
          "Lyon": [
              {
                "amount": 11.4
              }
          ],
          "Paris": [
              {
                "amount": 20
              }
          ]
        }
    },
    "FBP": {
        "UK": {
          "London": [
              {
                "amount": 10.9
              }
          ]
        }
    },
    "GBP": {
        "UK": {
          "London": [
              {
                "amount": 12.2
              }
          ]
        }
    },
    "USD": {
      "US": {
          "Boston": [
              {
                "amount": 100
              }
          ]
        }
    }
}


def test_grouping(input_list):
    target_key = 'country'
    result_keys = set((o[target_key] for o in input_list))

    result = dictify(input_list, 'country')

    assert set(result.keys()) == result_keys

    first_key = next(iter(result.keys()))
    assert target_key not in result[first_key]


def test_tree_build(input_list):
    result = make_nested_dicts(input_list, ['currency', 'country', 'city'])
    assert expected_result == result


def test_tree_build_fail(input_list_bad):
    with pytest.raises(DictifyError):
        make_nested_dicts(input_list_bad, ['currency', 'country', 'city'])

