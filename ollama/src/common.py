import os
import yaml


def load_parameters() -> dict:
    """ Laadt parameters uit config file

    Returns:
        dict: dictionary with parameters from file
    """
    with open('config/config.yaml', encoding = 'utf8', mode = "r") as infile:
        parameters = yaml.safe_load(infile)

    return parameters

### load_parameters ###


def split_filename(filename: str):
    """ Splits filename into dir, filename and .extension 

    Args:
        filename (str): filename to split

        returns:
            directory, filename without extension, .extension (including period)
    """

    fn, extension = os.path.splitext(filename)
    pad = os.path.dirname(fn)
    base = os.path.basename(fn)

    return pad, base, extension

### split_filename ###


