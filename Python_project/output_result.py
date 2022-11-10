"""Main class is defined here."""

from output_helper import (
    load_json,
    get_result_data
)


class Output(object):
    """Returns output for the input payload."""

    def final_output(self):
        """Display final data."""
        payload = load_json("input.json")
        data = load_json(payload['input_file_path'])
        final_data = get_result_data(payload, data)
        print(str(final_data))
        print("*************************")
        print(len(final_data))
