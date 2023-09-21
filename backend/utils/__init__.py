"""
Contain reusable helper functions that are not belong to a service
"""
from flask import render_template
from interfaces import ViewBaseInterface, HTMXBaseInterface
from typing import Optional, Union
from os import makedirs, path

def render_view(view_path, props: Optional[Union[ViewBaseInterface, HTMXBaseInterface]] = None, *args, **kwargs):
    """
    Inject a pseudo `result` dictionary if the `controller` produce no results
    """
    if props is None:
        props = {}
    return render_template(view_path, props=props, *args, **kwargs)


def ensure_path_exist(path_name):
    if not path.exists(path_name):
        makedirs(path_name)












# def filter_dict_list(li, key, filter_value, inclusion=True):
#     """
#     Filter list of dictionaries based on its key

#     @ Parameters:

#     - inclusion (`bool`): If set to `True`, find the dict that match `key`. 
#     If `False`, filter the items that not match key

#     @ Return: Copied (Tham trị) of the original list with filtered key 

#     """
#     index_list = []
#     for index, value in enumerate(li):
#         if inclusion:
#             if value[key] == filter_value:
#                 index_list.append(index)
#         else:
#             if value[key] != filter_value:
#                 index_list.append(index)

#     return [li[i] for i in index_list]
