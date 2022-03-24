import threading
import concurrent.futures as cf
import queue
import time
from statistics import mean

# Based on tutorial: Python Threading Tutorial: Run Code Concurrently Using the Threading Module
# https://www.youtube.com/watch?v=IEEhzQoKtQU

# Global queue
q = queue.Queue()


def worker(seconds: int):
    # print(f"Sleeping for {seconds} seconds...")
    q.get()
    time.sleep(seconds)
    q.task_done()
    # msg = f"Done Sleeping...{seconds}"
    # print(msg)
    # return msg


def run_many_concurrent_threads(list_runtimes):
    threads_list = []
    for runtime in list_runtimes:
        thread = threading.Thread(target=worker, args=[runtime], daemon=True)
        thread.start()
        threads_list.append(thread)

        # add to queue
        q.put(runtime)

    # block until all tasks done
    q.join()

    # previous code when created threads were added to a list
    # for thread in threads_list:
    #     thread.join()


def run_consecutively(list_runtimes):

    for runtime in list_runtimes:
        worker(runtime)

    duration = time.perf_counter()
    num_threads = len(list_runtimes)
    runtime_sum = sum(list_runtimes)
    print(f"Running {num_threads} consecutive threads with total runtime of {runtime_sum} secs took {duration} secs.")

    return duration


def print_multithreading_duration(list_runtimes, duration, method_version):
    num_threads = len(list_runtimes)
    runtime_sum = sum(list_runtimes)
    print(f"{method_version} method of running {num_threads} concurrent threads with"
          f" total runtime of {runtime_sum} secs took {duration} secs.")


def old_multithreading_method(list_runtimes):

    start = time.time()
    run_many_concurrent_threads(list_runtimes)
    end = time.time()
    duration = end - start
    # print_multithreading_duration(list_runtimes, round(duration, 3), "OLD")

    return duration


def new_multithreading_method(list_runtimes):

    # the context manager using the keyword "with" automatically joins the threads at the end
    start = time.time()
    with cf.ThreadPoolExecutor() as executor:
        # using map() method is more compact than list comprehension
        results = executor.map(worker, list_runtimes)

        # add tasks to queue
        for item in range(len(list_runtimes)):
            q.put(item)

        # previous code below about using list comprehensions and pairing with it the as_completed() method
        # list is needed when invoking the submit() method
        # can use a list comprehension
        # results = [executor.submit(worker, runtime) for runtime in list_runtimes]

        # executes code within for loop in the order of the completed threads
        # as_completed() method returns a future object
        # for thread in cf.as_completed(results):
        #     print(thread.result())

    end = time.time()
    duration = end - start
    # print_multithreading_duration(list_runtimes, round(duration, 3), "NEW")
    return duration


def compare_old_vs_new_threading_methods(test_iterations, list_len):
    """This function runs a runtime comparison between the old and new methods of doing multithreading.
    Old method used the threading library and the new method uses the concurrent.futures library"""

    # print("Comparing the old and new methods for multithreading.")

    uniform_times = [1 for _ in range(list_len)]
    increasing_times = [num for num in range(1, list_len+1)]

    lists_to_run = [uniform_times, increasing_times]

    old_method_results_uniform_times = []
    old_method_results_increasing_times = []
    new_method_results_uniform_times = []
    new_method_results_increasing_times = []

    for test in range(1, test_iterations+1):
        # print(f"Test Iteration: {test}")
        # for runtime_list in lists_to_run:
        result = old_multithreading_method(uniform_times)
        old_method_results_uniform_times.append(result)

        result = new_multithreading_method(uniform_times)
        new_method_results_uniform_times.append(result)

        result = old_multithreading_method(increasing_times)
        old_method_results_increasing_times.append(result)

        result = new_multithreading_method(increasing_times)
        new_method_results_increasing_times.append(result)

    print(f"Old Method Uniform Loads Average Time --> Threads: {list_len},"
          f" {round(mean(old_method_results_uniform_times), 2)}")
    print(f"New Method Uniform Loads Average Time --> Threads: {list_len},"
          f" {round(mean(new_method_results_uniform_times), 2)}")
    print(f"Old Method Increas Loads Average Time --> Threads: {list_len},"
          f" {round(mean(old_method_results_increasing_times), 2)}")
    print(f"New Method Increas Loads Average Time --> Threads: {list_len},"
          f" {round(mean(new_method_results_increasing_times), 2)}")


if __name__ == '__main__':
    print("Hello, this is the concurrent module")
    number_of_tests = 3

    # stress testing the two methods
    number_runtimes_per_list = [5, 10, 12, 13, 14, 15, 18, 20, 50]

    for runtimes in number_runtimes_per_list:
        compare_old_vs_new_threading_methods(number_of_tests, runtimes)


