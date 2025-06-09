from pyecharts.faker import Faker
from railwaymap.railway_map import normal_map, heat_signal_color_map, single_bureau_map

def gen_fake_data():
    """
    产生18个路局对应的假数据，用于地图显示
    :return: 包括18个路局名称和数量的list，格式：[['沈阳局', 77], ...]
    """
    num_list = []
    for i in range(3):
        num_list += Faker.values()
    name = ['沈阳局', '哈尔滨局', '乌鲁木齐局', '青藏公司', '昆明局', '广州局', '南宁局', '南昌局', '上海局', '济南局', '北京局', '呼和浩特局', '兰州局', '西安局', '成都局', '太原局', '郑州局', '武汉局']
    data = [list(z) for z in zip(name, num_list[:18])]
    return data

def normal_map_example():
    """
    全国路局区域图示例
    :return: 生成html文件，无返回值
    """
    normal_map(gen_fake_data())

def heat_map_example():
    """
    全国路局热力图示例
    :return: 生成html文件，无返回值
    """
    heat_signal_color_map(gen_fake_data())

def single_bureau_map_example():
    """
    上海局地图示例
    :return: 生成html文件，无返回值
    """
    num_list = []
    for i in range(2):
        num_list += Faker.values()
    coordinate_data = {'徐州东站': {'coord': [117.306674, 34.267711], 'num': num_list[0]}, '阜阳站': {'coord': [115.86825, 32.914512], 'num': num_list[1]}, '温州站': {'coord': [120.691, 27.986], 'num': num_list[2]}, '上海南站': {'coord': [121.429462, 31.153127], 'num': num_list[3]}, '上海站': {'coord': [121.455708, 31.249574], 'num': num_list[4]}, '南京站': {'coord': [118.797499, 32.087104], 'num': num_list[5]}, '杭州站': {'coord': [120.182882, 30.243486], 'num': num_list[6]}, '宁波站': {'coord': [121.536807, 29.861967], 'num': num_list[7]}, '金华站': {'coord': [119.635857, 29.110764], 'num': num_list[8]}, '苍南站': {'coord': [120.412049, 27.527901], 'num': num_list[9]}, '衢州站': {'coord': [118.881604, 28.92349], 'num': num_list[10]}, '六安站': {'coord': [116.499665, 31.714959], 'num': num_list[11]}, '连云港站': {'coord': [119.162619, 34.609091], 'num': num_list[12]}, '苏州站': {'coord': [120.610868, 31.329679], 'num': num_list[13]}}
    single_bureau_map('shanghaiju', coordinate_data)