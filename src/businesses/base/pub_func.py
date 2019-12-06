# coding:utf-8
from __future__ import absolute_import
import re
import logging
import traceback
from xml.etree import ElementTree


def xml_parse(string):
    """
    解析 xml 数据
    :param string: xml 字符串
    :return: 对应的 dict 类型数据
    """
    def xml_content_parse(node):
        if len(node.getchildren()) == 0:
            return node.text if node.text is not None else ''
        else:
            node_array = {}
            for child in node.getchildren():
                if child.tag in node_array.keys():
                    if not isinstance(node_array[child.tag], list):
                        node_array[child.tag] = [node_array[child.tag]]
                    node_array[child.tag].append(xml_content_parse(child))
                else:
                    node_array[child.tag] = xml_content_parse(child)
            return node_array

    ret = dict()
    xml_str = re.sub(r"<\?.*\?>", "", string)
    element = ElementTree.fromstring(xml_str)
    try:
        ret[element.tag] = xml_content_parse(element)
        return ret
    except Exception:
        logging.error('parse xml failed, err: %s' % traceback.format_exc())
        return
