from entities.entity import Entity
from enum import Enum
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import os


class Match(Enum):
    exact = 1
    bleu = 2


def response_assertions(expected, actual, test_results, options={}):
    default_options = {"fail": bool(eval(os.environ.get("TEST_FAIL", "False")))}
    options = {**default_options, **options}

    # this method works with lists
    actual = actual if isinstance(actual, list) else [actual]
    expected = expected if isinstance(expected, list) else [expected]

    expected = expected or []
    result = assert_equal(len(expected), len(actual), test_results) and assert_true(
        all(any(is_equal(e, a) for a in actual) for e in expected),
        test_results,
    )

    return result


def entity_assertions(expected, actual, test_results, options={}):
    default_options = {"fail": bool(eval(os.environ.get("TEST_FAIL", "False")))}
    options = {**default_options, **options}

    # assert that actual is not None and that expected and actual have the same length
    result = assert_true(len(expected) == len(actual), test_results)

    # score match rate between expected entities and actual entities
    if expected and actual:
        scores = {}
        for i, e in enumerate(expected):
            scores[i] = {}
            for j, a in enumerate(actual):
                scores[i][j] = 0
                for attr, value in e.items():
                    if hasattr(a, attr) and is_equal(getattr(a, attr), value):
                        scores[i][j] += 1

        # find max score for each expected entity
        for i in scores.keys():
            max_index = np.argmax(list(scores[i].values()))
            j = list(scores[i].keys())[max_index]
            e = expected[i]
            a = actual[j]
            result = (
                all(
                    assert_equal(
                        getattr(a, attr) if hasattr(a, attr) else None,
                        value,
                        test_results,
                    )
                    for attr, value in e.items()
                )
                and result
            )

    return result


def is_equal(actual, expected):
    result = actual == expected
    return result


def is_match(actual, expected):
    hypothesis = word_tokenize(expected.text)
    reference = word_tokenize(actual.text)
    weights = (1.0, 0.0)
    bleu_score = nltk.translate.bleu_score.sentence_bleu(
        [reference], hypothesis, weights
    )
    return bleu_score


def is_not_none(actual):
    return actual is not None


def assert_equal(actual, expected, test_results, options={}):
    default_options = {
        "fail": bool(eval(os.environ.get("TEST_FAIL", "False"))),
        "match": Match.bleu,
    }
    options = {**default_options, **options}

    result = is_equal(actual, expected)

    _handle_result(result, actual, expected, test_results, options)

    return result


def assert_match(actual, expected, test_results, options={}):
    default_options = {
        "fail": bool(eval(os.environ.get("TEST_FAIL", "False"))),
        "match": Match.bleu,
    }
    options = {**default_options, **options}

    if options.get("match") == Match.bleu:
        result = is_match(actual, expected)
    elif options.get("match") == Match.exact:
        result = is_equal(actual, expected)
    else:
        result = is_equal(actual, expected)

    _handle_result(result, actual, expected, test_results, options)

    return result


def assert_not_none(actual, test_results, options={}):
    default_options = {"fail": bool(eval(os.environ.get("TEST_FAIL", "False")))}
    options = {**default_options, **options}

    result = is_not_none(actual)

    # if the test has already failed, don't bother
    if not result:
        # increment the failure count
        total_failures = test_results.get("total_failures", 0)
        total_failures += 1
        test_results["total_failures"] = failures

        failures = test_results.get("failures", 0)
        failures += 1
        test_results["failures"] = failures

        # document the failure
        result = {
            "message": f"{actual} is None",
            "unique_failure": True,
            "test": actual,
        }
        results = test_results.get("results", [])
        results.append(result)
        test_results["results"] = results

        if options.get("fail"):
            raise AssertionError(result)

    return result


def assert_test(test_results):
    if test_results.get("failures", 0) > 0:
        message = f"""
            {test_results.get("failures")} failures (total failures: {test_results.get("total_failures")})): 
            {[result.get("message", "Test failed") for result in test_results.get("results", [])]}
        """
        raise AssertionError(message)


def assert_true(actual, test_results, options={}):
    return assert_equal(actual, True, test_results, options)


def _handle_result(result, actual, expected, test_results, options={}):
    if result:
        test_results["correct"] = test_results.get("correct", 0)
        test_results["correct"] += 1
    else:
        test_results["incorrect"] = test_results.get("incorrect", 0)
        test_results["incorrect"] += 1

        # document the failure
        result = {
            "message": f"Assertion failed",
            "actual": actual,
            "expected": expected,
        }
        results = test_results.get("results", [])
        results.append(result)
        test_results["results"] = results

        if options.get("fail"):
            raise AssertionError(result)


def _handle_result2(result, actual, expected, test_results, options={}):
    if result:
        total_failures = test_results.get("total_", 0)
        total_failures += 1
        test_results["total_failures"] = failures
    # if the test has already failed, don't bother
    else:
        # # map bad result to the expected value
        # if actual and actual.value:
        #     recovery_results = test_results.get("recovered_results", {})
        #     recovery_results[actual.value] = expected
        #     test_results["recovered_results"] = recovery_results
        #     failed_items = test_results.get("failed_items", set())
        #     failed_items.add(expected.value)
        #     test_results["failed_items"] = failed_items

        # increment the failure count
        total_failures = test_results.get("total_failures", 0)
        total_failures += 1
        test_results["total_failures"] = failures

        unique_failure = not (
            expected is not None
            and isinstance(expected, Entity)
            and expected.value in test_results.get("failed_items", {})
        )
        if unique_failure:
            failures = test_results.get("failures", 0)
            failures += 1
            test_results["failures"] = failures

        # document the failure
        result = {
            "message": f"{actual} != {expected}",
            "unique_failure": unique_failure,
            "actual": actual,
            "expected": expected,
        }
        results = test_results.get("results", [])
        results.append(result)
        test_results["results"] = results

        if options.get("fail"):
            raise AssertionError(result)
