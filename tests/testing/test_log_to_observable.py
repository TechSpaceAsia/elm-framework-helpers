import io
from elm_framework_helpers.testing import *
from elm_framework_helpers.testing.log_to_observable import log_to_observable
from unittest.mock import mock_open

def test_log_to_observable():
    # Define the log file content
    file_content = """1678600081 | {"message":"first"}
1678600092 | {"message":"second"}
1678600106 | {"message":"third"}
1678600119 | {"message":"fourth"}
1678600134 | {"message":"fifth"}
1678600153 | {"message":"sixth"}"""

    # Create a mock file object with the file content
    mock_file = io.StringIO(file_content)

    # Call the log_to_observable function with the mock file object
    messages = log_to_observable(mock_file)

    # Define the expected messages
    expected_messages = [
        on_next(0, {"message":"first"}),
        on_next(11, {"message":"second"}),
        on_next(25, {"message":"third"}),
        on_next(38, {"message":"fourth"}),
        on_next(53, {"message":"fifth"}),
        on_next(72, {"message":"sixth"}),
    ]

    # Assert that the actual messages match the expected messages
    assert_equal_messages(messages, expected_messages)

    # Test case: start_line > 0
    # Call the log_to_observable function with start_line = 2
    messages = log_to_observable(mock_file, start_line=2)

    # Define the expected messages
    expected_messages = [
        (0, {'message': 'second'}),
        (14, {'message': 'third'}),
        (27, {'message': 'fourth'}),
        (42, {'message': 'fifth'}),
        (61, {'message': 'sixth'})
    ]

    # Assert that the actual messages match the expected messages
    assert_equal_messages(messages, expected_messages)

    # Test case: end_line set
    # Call the log_to_observable function with end_line = 3
    messages = log_to_observable(mock_file, end_line=3)

    # Define the expected messages
    expected_messages = [
        (0, {'message': 'first'}),
        (11, {'message': 'second'}),
        (25, {'message': 'third'})
    ]

    # Assert that the actual messages match the expected messages
    assert_equal_messages(messages, expected_messages)

    # Test case: first_line_timestamp set
    # Call the log_to_observable function with first_line_timestamp = 1678600080
    messages = log_to_observable(mock_file, first_line_timestamp=1678600080, end_line=2)

    # Define the expected messages
    expected_messages = [
        (1, {'message': 'first'}),
        (12, {'message': 'second'}),
    ]

    # Assert that the actual messages match the expected messages
    assert_equal_messages(messages, expected_messages)