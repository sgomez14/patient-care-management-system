from concurrent_multithreading import old_multithreading_method, new_multithreading_method


def test_old_multithreading_method_uniform_loads() -> None:
    """"This tests the function old_multithreading_method using a list of uniform durations.
    Old method manually creates and joins the threads using the threading library."""

    # create list for 10 threads each running for 1 second
    uniform_load = [1 for _ in range(1, 11)]

    total_consecutive_runtime = sum(uniform_load)

    total_concurrent_runtime = old_multithreading_method(uniform_load)

    # assert that concurrent runtime is faster than consecutive runtime
    assert total_consecutive_runtime > total_concurrent_runtime


def test_old_multithreading_method_increasing_loads() -> None:
    """"This tests the function old_multithreading_method using a list of increasing durations.
    Old method manually creates and joins the threads using the threading library."""

    # create list for 10 threads each running for 1 second longer than the previous thread
    increasing_load = [num for num in range(1, 11)]

    total_consecutive_runtime = sum(increasing_load)

    total_concurrent_runtime = old_multithreading_method(increasing_load)

    # assert that concurrent runtime is faster than consecutive runtime
    assert total_consecutive_runtime > total_concurrent_runtime


def test_new_multithreading_method_uniform_loads() -> None:
    """"This tests the function new_multithreading_method using a list of uniform durations.
    New method automatically creates and joins the threads using the concurrent.futures library."""

    # create list for 10 threads each running for 1 second
    uniform_load = [1 for _ in range(1, 11)]

    total_consecutive_runtime = sum(uniform_load)

    total_concurrent_runtime = new_multithreading_method(uniform_load)

    # assert that concurrent runtime is faster than consecutive runtime
    assert total_consecutive_runtime > total_concurrent_runtime


def test_new_multithreading_method_increasing_loads() -> None:
    """"This tests the function new_multithreading_method using a list of increasing durations.
    New method automatically creates and joins the threads using the concurrent.futures library."""

    # create list for 10 threads each running for 1 second longer than the previous thread
    increasing_load = [num for num in range(1, 11)]

    total_consecutive_runtime = sum(increasing_load)

    total_concurrent_runtime = new_multithreading_method(increasing_load)

    # assert that concurrent runtime is faster than consecutive runtime
    assert total_consecutive_runtime > total_concurrent_runtime
