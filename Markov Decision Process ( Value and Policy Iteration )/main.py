import os
import sys
import json
import pandas as pd
from tests import LoadTests
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration


def execute_value_iteration_test(test, epsilon, output='console'):
    """
    Description
    -----------
    Function used to run the value_iteration for
    the given test.

    Parameters
    ----------
    test: Test() \\
        -- A Test() instance with the information
        needed to run the value_iteration.

    epsilon: float \\
        -- A floating point number, used to set
        the value_iteration's stopping decision.

    output: str \\
        -- A string that tells the function where
        its output is expected.

    Returns
    -------
    ValueIteration() \\
        -- If no recognizable outputs is informed,
        returns the instance of the value_iteration used.
    """

    value_iteration = ValueIteration(test, epsilon=epsilon)

    value_iteration.run()

    if output in ['console', 'file']:
        output_processing(output, test, value_iteration, 'ValueIteration')

    return value_iteration


def execute_policy_iteration_test(test, output='console'):
    """
    Description
    -----------
    Function used to run the policy_iteration for
    the given test.

    Parameters
    ----------
    test: Test() \\
        -- A Test() instance with the information
        needed to run the policy_iteration.

    output: str \\
        -- A string that tells the function where
        its output is expected.

    Returns
    -------
    PolicyIteration() \\
        -- If no recognizable outputs is informed,
        returns the instance of the policy_iteration used.
    """

    policy_iteration = PolicyIteration(test)

    policy_iteration.run()

    if output in ['console', 'file']:
        output_processing(output, test, policy_iteration, 'PolicyIteration')

    return policy_iteration


def output_processing(output, test, algorithm, algorithm_name):
    """
    Description
    -----------
    Function used to run the value_iteration for
    the given test.

    Parameters
    ----------
    output: str \\
        -- A string that tells the function where
        its output is expected.

    test: Test() \\
        -- A Test() instance with the information
        needed to run the value_iteration.

    algorithm: ValueIteration() or PolicyIteration() \\
        -- the instance of the algorithm with the information
        that is going to be processed.

    algorithm_name: str \\
        -- The name of the algorithm, used as folder name.
    """

    if output == 'file':
        folder = os.path.join(os.path.dirname(__file__), 'outputs')
        folder = os.path.join(folder, algorithm_name)
        folder = os.path.join(folder, test.folder_name)

        file_name = test.file_name + '.txt'

        output_file = open(
            f'{os.path.join(folder, file_name)}', 'a+', encoding='utf-8'
        )

        # Truncating files, so that it doesn't append on existing content
        output_file.truncate(0)

        output_file.write(str(algorithm))

        output_file.close()

    elif output == 'console':
        print(algorithm)


tests = LoadTests()

fixed_goal = tests.fixed_goal_tests
random_goal = tests.random_goal_tests

del tests

epsilon = 0.1

# file or console
output = 'file'

metrics_df = pd.DataFrame(columns=[
    'test_name', 'vi_time', 'vi_iter', 'pi_time', 'pi_iter'
])

for test in fixed_goal:
    value_iteration = execute_value_iteration_test(test, epsilon, output=output)
    policy_iteration = execute_policy_iteration_test(test, output=output)

    metrics_dict = {
        'test_name': str(os.path.join(test.folder_name, test.file_name)),
        'vi_time': value_iteration.time_elapsed,
        'vi_iter': value_iteration.iterations,
        'pi_time': policy_iteration.time_elapsed,
        'pi_iter': policy_iteration.iterations
    }

    metrics_df = metrics_df.append(metrics_dict, ignore_index=True)

for test in random_goal:
    value_iteration = execute_value_iteration_test(test, epsilon, output=output)
    policy_iteration = execute_policy_iteration_test(test, output=output)

    metrics_dict = {
        'test_name': str(os.path.join(test.folder_name, test.file_name)),
        'vi_time': value_iteration.time_elapsed,
        'vi_iter': value_iteration.iterations,
        'pi_time': policy_iteration.time_elapsed,
        'pi_iter': policy_iteration.iterations
    }

    metrics_df = metrics_df.append(metrics_dict, ignore_index=True)

metrics_df.to_csv(
    os.path.join(
        os.path.join(os.path.dirname(__file__), 'outputs'),
        'metrics.csv'
    ),
    index=False
)
