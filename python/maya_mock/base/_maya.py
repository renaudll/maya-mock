"""Module for all of Maya entry point functions."""
from maya import cmds


def get_node_attributes_info(node_type):
    """
    Retrieve information about about a registered attribute as a dict.

    :param str node_type: The type of the node being inspect
    :param str attribute: The name of the attribute to inspect
    :return: An object dict
    :rtype: dict
    """
    result = {}

    attributes = cmds.attributeInfo(allAttributes=True, type=node_type)

    for attribute in attributes:
        # TODO: All these calls to cmds are slowing down generation! (26 seconds)
        attr_type = cmds.attributeQuery(attribute, type=node_type, attributeType=True)

        # Some attributes will return 'typed' as the type.
        # I don't know of any way of knowing in advance the type.
        # However for what we need, guessing might be enough.
        if attr_type == 'typed':
            if 'matrix' in attribute.lower():  # HACK
                attr_type = 'matrix'

        attr_name_short = cmds.attributeQuery(attribute, type=node_type, shortName=True)
        attr_name_nice = cmds.attributeQuery(attribute, type=node_type, niceName=True)
        attr_parents = cmds.attributeQuery(attribute, type=node_type, listParent=True)
        attr_parent = attr_parents[0] if attr_parents else None
        attr_readable = cmds.attributeQuery(attribute, type=node_type, readable=True)
        attr_writable = cmds.attributeQuery(attribute, type=node_type, writable=True)

        attr_data = {
            'port_type': attr_type,
            'short_name': attr_name_short,
            'nice_name': attr_name_nice,
            'parent': attr_parent,
            'readable': attr_readable,
            'writable': attr_writable,
        }
        result[attribute] = attr_data

    return result


def get_node_classification(node_type):
    """
    Return the classification string associated with a registered node in maya.
    This is cmds.getClassification

    :param str node_type: The type of the node to inspect.
    :return: The node classification string
    :rtype: str
    """
    classifications = cmds.getClassification(node_type)
    # Get the node identification tags
    if len(classifications) != 1:  # This should not happen, but we don't know why getClassification return a list.
        raise Exception("Unexpected classification return value for %r" % node_type)
    classification = classifications[0]
    return classification
