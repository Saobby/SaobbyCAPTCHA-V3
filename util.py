import random


def gen_random_str(lens: int = 64) -> str:
    """
    生成指定长度的随机字符串
    :param lens: 随机字符串的长度
    :return: 随机字符串
    """
    ret = ""
    for i in range(lens):
        ret += random.choice("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return ret


def check_pos(pos: tuple, pos_list: list[tuple], min_distance: float) -> bool:
    """
    检查指定坐标是否靠近指定列表中的某个坐标
    :param pos: 要检查的坐标
    :param pos_list: 指定坐标列表
    :param min_distance: 会被判定为“靠近”的最小距离
    :return: 结果: bool 列表中存在一个靠近指定坐标的坐标时返回 True，否则返回 False
    """
    cur_x, cur_y = pos
    for position in pos_list:
        chr_x, chr_y = position[1], position[2]
        distance = ((cur_x-chr_x)**2 + (cur_y-chr_y)**2) ** 0.5
        if distance < min_distance:
            return True
    return False
