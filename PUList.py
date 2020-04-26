from typing import List


def filter_check_element(string):
    """
    Return the function as a check.
    My crappy way of writing functional programming.
    :param string:
    :return:
    """

    def check_element(element_template):
        """
        Inner check function.
        :param element_template:
        :return:
        """
        return string.lower() in element_template.lower()

    return check_element


def filter_list_str(list_input: List[str], str_input: str) -> List[str]:
    """
    Filter a list using a string.
    :param list_input:
    :param str_input:
    :return:
    """
    filter_str_input = filter_check_element(str_input)

    return list(filter(filter_str_input, list_input))


if __name__ == "__main__":
    print(filter_list_str(["nic", "ice", "din", "sick"], "ic"))
