################################################################################
# Author: Jesus Ramos Membrive
# E-Mail: ramos.membrive@gmail.com
################################################################################
from pygrabber.dshow_graph import FilterGraph


def get_camera_connected() -> dict:
    """
    Returns a dictionary of available cameras and their corresponding titles.

    The function uses the `FilterGraph` class to get a list of available cameras, and then creates a dictionary of enumerated
    camera titles. If no cameras are available, an empty dictionary is returned.

    :return: A dictionary of available cameras and their corresponding titles.
    """
    try:
        devices = FilterGraph().get_input_devices()
        available_cameras = dict(enumerate(devices))
        return available_cameras
    except Exception:
        return {}
