"""
本模块用于数据预处理

This module is used for data preproccessing
"""
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['FangSong']
plt.rcParams['axes.unicode_minus'] = False
from io import BytesIO
from lxml import etree
import base64
import math

def _rc(arg):
    cov_mat = np.cov(arg)
    var_mat = np.diagonal(cov_mat) ** 0.5
    var_mat[var_mat == 0] = 1
    for i in range(cov_mat.shape[0]):
        cov_mat[i] /= var_mat[i]
        cov_mat[:, i] /= var_mat[i]
    return cov_mat

def _preview_process(data, value_round):
    """
    预览处理
    """
    data = np.array(data, dtype=float)
    name_list = ['平均值', '中位数', '方差', '标准差', '最大值', '最小值', '偏度', '峰度']
    value_list = []
    mean_ = data.mean(axis=0)
    value_list.append(np.round(mean_, value_round))
    value_list.append(np.round(np.median(data, axis=0), value_round))
    value_list.append(np.round(data.var(axis=0), value_round))
    value_list.append(np.round(data.std(axis=0), value_round))
    value_list.append(np.round(data.max(axis=0), value_round))
    value_list.append(np.round(data.min(axis=0), value_round))
    value_list.append(np.round(((data - mean_) ** 3).mean(axis=0), value_round))
    value_list.append(np.round(((data - mean_) ** 4).mean(axis=0), value_round))
    value_list = np.array(value_list).flatten()
    style = '\n    <style>\n    table{\n        border-collapse: collapse;\n    }\n    table, table tr td {\n        border:1px solid #ccc;\n    }\n    table tr td{\n        padding: 5px 10px;\n    }\n    </style>\n    '
    table = '<h2 style="padding-left:50px; border-top:1px solid #ccc">数值特征</h2>' + style + '<table align="center"><caption></caption>'
    for i in range(8):
        table += '<tr><td>' + name_list[i] + '</td>' + '<td>%s</td>' * data.shape[1] + '</tr>'
    table = '<h1 style="padding-left:50px;">数据信息</h1>' + table % tuple(value_list) + '</table>'
    data = np.ascontiguousarray(data.T)
    num = data.shape[0]
    plt.figure(figsize=(9, 3 * num))
    for i in range(num):
        (q1, q2, q3) = np.percentile(data[i], [25, 50, 75])
        plt.scatter(mean_[i], i + 1, marker='o', color='white', s=30, zorder=3)
        plt.hlines(i + 1, q1, q3, color='k', linestyle='-', lw=1)
    bx = plt.violinplot(data.tolist(), showextrema=False, vert=False)
    plt.title('分布图')
    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = 'data:image/png;base64,' + ims
    im1 = '<div align="center"><img src="%s"></div>' % imd
    im1 = '<br></br><h2 style="padding-left:50px; border-top:1px solid #ccc">密度分布</h2>' + im1
    cov_mat = _rc(data)
    matrix = '<table border="0"><caption></caption>'
    for i in range(num):
        matrix += '<tr>' + '<td>%s</td>' * num + '</tr>'
    matrix = matrix % tuple(np.round(cov_mat.flatten(), value_round)) + '</table>'
    plt.figure(figsize=(8, 8))
    plt.matshow(cov_mat, fignum=0, cmap='Blues')
    plt.colorbar()
    plt.title('相关系数图')
    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = 'data:image/png;base64,' + ims
    im2 = '<div style="display:flex;flex-direction:row;vertical-align:middle;justify-content:center;width:100%;height:80vh"><div style="margin:auto 0;white-space:pre-wrap;max-width:50%">'
    im2 = im2 + '相关矩阵：' + matrix + '</div><img style="object-fit:contain;max-width:45%;max-height:80vh" src="{}"/></div>'.format(imd)
    im2 = '<br></br><h2 style="padding-left:50px; border-top:1px solid #ccc">相关性</h2>' + im2
    plt.figure(figsize=(2.5 * num, 2.5 * num))
    for i in range(num * num):
        ax = plt.subplot(num, num, i + 1)
        ax.plot(data[i // num], data[i % num], 'o')
    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = 'data:image/png;base64,' + ims
    im3 = '<div align="center"><img src="%s"></div>' % imd
    im3 = '<br></br><h2 style="padding-left:50px; border-top:1px solid #ccc">散点关系</h2>' + im3
    return '<title>数据信息预览</title>' + table + im1 + im2 + im3

def preview_file(filename, data, value_round=3):
    """
    生成数据预览报告的html文件
    
    参数
    ----
    filename：字符串类型，文件名
    data：二维数组，数据
    value_round：整型，可选，数字特征保留的小数点后的位数，默认为3
    
    
    Generate preview report with html file
    
    Parameters
    ----------
    filename: str, file name
    data: 2D array, data
    value_round: int, callable, the number of digits after the decimal point retained by numeric features, default=3
    """
    root = _preview_process(data=data, value_round=value_round)
    html = etree.HTML(root)
    tree = etree.ElementTree(html)
    tree.write(filename)

def preview(data, value_round=3):
    """
    在jupyter中显示数据预览报告
    
    参数
    ----
    data：二维数组，数据
    value_round：整型，可选，数字特征保留的小数点后的位数，默认为3
    
    
    Display preview report in jupyter
    
    Parameters
    ----------
    data: 2D array, data
    value_round: int, callable, the number of digits after the decimal point retained by numeric features, defualt=3
    """
    root = _preview_process(data=data, value_round=value_round)
    from IPython.core.display import display, HTML
    display(HTML(root))

def length_pad(seq, maxlen=None, value=0, padding='pre', dtype=float):
    """
    填充二维列表，使得每行长度都为maxlen
    
    参数
    ----
    seq：二维列表，需要填充的对象
    maxlen：整型，可选，每行的最大长度，默认为原二维列表最大的长度
    value：数类型，可选，填充值，默认为0
    padding：字符串类型，可选，填充位置，'pre'代表从前面填充，'post'代表从后面填充，默认为'pre'
    dtype：可选，输出的元素类型，默认为float
    
    返回
    ----
    二维ndarray
    
    
    Pad the 2D list so that every row is 'maxlen' in length
    
    Parameters
    ----------
    seq: 2D list, objects that need to be padded
    maxlen: int, callable, the maximum length of each row, default = the maximum length of the original 2D list
    value: num, callable, padding value, default=0
    padding: str, callable, padding location, 'pre' means padding from the front and 'post' from the back, default='pre'
    dtype: callable, the element type of the output, default=float
    
    Return
    ------
    2D ndarray
    """
    seq = list(seq)
    if not maxlen:
        maxlen = 0
        for i in seq:
            if len(i) > maxlen:
                maxlen = len(i)
    if padding == 'pre':
        for i in range(len(seq)):
            if maxlen > len(seq[i]):
                seq[i] = [value] * (maxlen - len(seq[i])) + seq[i]
            elif maxlen < len(seq[i]):
                seq[i] = seq[i][-1 * maxlen:]
    elif padding == 'post':
        for i in range(len(seq)):
            if maxlen > len(seq[i]):
                seq[i] += [value] * (maxlen - len(seq[i]))
            elif maxlen < len(seq[i]):
                seq[i] = seq[i][:maxlen]
    return np.array(seq, dtype=dtype)

def sample_pad(data, index=0, padding=None):
    """
    对二维数据进行样本填充
    先对data中的每个二维数据进行遍历，以各个index列的值作为全集，再对data的每个二维数据进行填充
    如：data1 = [[0, 1],
                 [1, 2],
                 [2, 3]]
        data2 = [[2, 3],
                 [3, 4],
                 [4, 5]]
        data = (data1, data2)
        则得到输出：
        output = [array([[0, 1],
                        [1, 2],
                        [2, 3],
                        [3, nan],
                        [4, nan]]),
                  
                  array([[0, nan],
                         [1,nan],
                         [2, 3],
                         [3, 4],
                         [4, 5]])]
    
    参数
    ----
    data：元组或列表类型，数据
    index：整型，作为扩充全集的标准列的索引
    padding：填充值，可选，默认为None
    
    返回
    ----
    ndarray
    
    
    Sample filling for 2D data
    Values of each index column will be taken as the complete set, then each 2D data of data is padded
    e.g. data1 = [[0, 1],
                 [1, 2],
                 [2, 3]]
         data2 = [[2, 3],
                  [3, 4],
                  [4, 5]]
         data = (data1, data2)
         output = [array([[0, 1],
                          [1, 2],
                          [2, 3],
                          [3, nan],
                          [4, nan]]),
                    
                    array([[0, nan],
                           [1,nan],
                           [2, 3],
                           [3, 4],
                           [4, 5]])]
    
    Parameters
    ----------
    data: tuple or list, data
    index: int, the index of a standard column as an extended complete set
    padding: padding value, optional, default=None
    
    Return
    ------
    ndarray
    """
    time_set = set()
    result = []
    if not padding:
        padding = [np.nan] * (len(data[0][0]) - 1)
    else:
        padding = list([padding])
    for i in range(len(data)):
        data_part = np.array(data[i], dtype=np.object)
        result.append(data_part)
        time_set = time_set | set(data_part[:, index])
    for i in range(len(result)):
        different_set_list = np.array([list(time_set - set(result[i][:, index]))], dtype=np.object).T
        num = len(different_set_list)
        padding_new = np.array(padding * num, dtype=np.object).reshape(num, -1)
        different_set_list = np.hstack((padding_new[:, :index], different_set_list, padding_new[:, index:]))
        result[i] = np.vstack((result[i], different_set_list))
    return result

def shuffle(*arg):
    """
    打乱一个序列或以相同方法打乱多个序列
    
    返回
    ----
    None
    
    
    Shuffle a sequence or shuffle multiple sequences in the same way
    
    Return
    ------
    None
    """
    state = np.random.get_state()
    for li in arg:
        np.random.set_state(state)
        np.random.shuffle(li)

def data_split(data, targets, train_size=None, test_size=None, shuffle=True, random_state=None):
    """
    分离数据
    
    参数
    ----
    data：数据
    targets：指标
    train_size：浮点数类型，可选，训练集占总数据量的比，取值范围为(0, 1]，默认为0.75
    test_size：浮点数类型，可选，测试集占总数据量的比，取值范围为[0, 1)，当train_size被定义时，该参数无效
    shuffle：布尔类型，可选，True表示打乱数据，False表示不打乱数据，默认为True
    random_state：整型，可选，随机种子
    
    返回
    ----
    元组，(数据测试集, 指标测试集, 数据验证集, 指标验证集)，元组元素与输入数据类型相同
    
    
    split the data
    
    Parameters
    ----------
    data: data
    targets: targets
    train_size: float, callable, ratio of training set to total data, value range is (0, 1], default=0.75
    test_size: float, callable, ratio of test set to total data, value range is [0, 1)
    shuffle: bool, callable, 'True' will shuffle the data, 'False' will not, default = True
    random_state: int, callable, random seed
    
    Return
    ------
    tuple, (train_data, train_target, validation_data, validation_target), the tuple element is the same as the input data type
    """
    if not (train_size or test_size):
        train_size = 0.75
    elif test_size:
        train_size = 1 - test_size
    if train_size <= 0 or train_size > 1:
        raise Exception("'train_size' should be in (0, 1], 'test_size' should be in [0, 1)")
    if shuffle:
        np.random.seed(random_state)
        state = np.random.get_state()
        np.random.shuffle(data)
        np.random.set_state(state)
        np.random.shuffle(targets)
    num_of_data = len(data)
    train_data = data[:int(num_of_data * train_size)]
    train_target = targets[:int(num_of_data * train_size)]
    validation_data = data[int(num_of_data * train_size):]
    validation_target = targets[int(num_of_data * train_size):]
    return (train_data, train_target, validation_data, validation_target)

def kfold(data, targets, n, k=5):
    """
    参数
    ----
    data：数据
    targets：指标
    n：整型，表示将第n折作为验证集，从0开始
    k：整型，可选，k折验证的折叠数，默认k=5
    
    返回
    ----
    元组，(数据测试集, 指标测试集, 数据验证集, 指标验证集)，元组元素与输入数据类型相同
    
    
    Parameters
    ----------
    data: data
    targets: targets
    n: int, take the nth part as validation set, starting from 0
    k: int, callable, the number of k-fold, default = 5
    
    Return
    ------
    tuple, (train_data, train_target, validation_data, validation_target), the tuple element is the same as the input data type
    """
    num_validation_samples = len(data) // k
    validation_data = data[num_validation_samples * n:num_validation_samples * (n + 1)]
    validation_targets = targets[num_validation_samples * n:num_validation_samples * (n + 1)]
    if type(data) != list:
        loc = np.arange(0, len(data)).astype(int)
        loc = np.delete(loc, loc[num_validation_samples * n:num_validation_samples * (n + 1)])
        train_data = data[loc]
        train_targets = targets[loc]
    else:
        train_data = data[:num_validation_samples * n].copy()
        train_data.extend(data[num_validation_samples * (n + 1):])
        train_targets = targets[:num_validation_samples * n].copy()
        train_targets.extend(targets[num_validation_samples * (n + 1):])
    return (train_data, train_targets, validation_data, validation_targets)

def dataloader(data, targets, choose_rate=0.3, shuffle=True, random_state=None):
    """
    数据随机生成器
    
    参数
    ----
    data：数据
    targets：指标
    choose_rate：浮点数类型，可选，生成率，即一次生成数据量在原数据量的占比，范围为[0, 1]，默认为0.3
    shuffle：布尔类型，可选，True表示打乱数据，False表示不打乱数据，默认为True
    random_state：整型，可选，随机种子
    
    返回
    ----
    生成器，生成数据与输入数据类型相同
    
    
    Data Random Generator
    
    Parameters
    ----------
    data: data
    targets: targets
    choose_rate: float, callable, generation rate (the proportion of data generated at one time in the original data) whose range is [0, 1], default=0.3
    shuffle: bool, callable, 'True' will shuffle the data, 'False' will not, default = True
    random_state: int, callable, random seed
    
    Return
    ------
    generator, the generated data is of the same type as the input data
    """
    if shuffle:
        np.random.seed(random_state)
        state = np.random.get_state()
        np.random.shuffle(data)
        np.random.set_state(state)
        np.random.shuffle(targets)
    num = len(data)
    choose_rate = int(num * choose_rate)
    times = int(math.ceil(num / choose_rate))
    for i in range(times):
        loc_1 = i * choose_rate
        loc_2 = (i + 1) * choose_rate
        yield (data[loc_1:loc_2], targets[loc_1:loc_2])

def standard(data, mean=True, var=True, index=None):
    """
    标准化数据
    z = (x - u) / s
    z：新数据；  x：原数据；  u：均值；  s：方差
    如果某一列数据完全相同（即方差s=0），则该列数据全部归零
    
    参数
    ----
    data：二维ndarray数据
    mean：布尔类型或ndarray，可选，布尔类型决定是否将均值调整为0，ndarray用于设定不同的均值
    var：布尔类型或ndarray，可选，是否将方差调整为1，ndarray用于设定不同的方差
    index：列表类型，可选，需要进行标准化的列的索引，默认为全部
    
    返回
    ----
    tuple
    
    
    Standardize data
    z = (x - u) / s
    z: new data;  x: origin data;  u: mean value;  s: variance
    if data in one column are the same(s=0), data in this column will be turned to 0
    
    Parameters
    ----------
    data: 2D ndarray
    mean: bool or ndarray, callable, bool decides if adjust the mean value to 0, ndarray is used to set different means
    var: bool or ndarray, callable, bool decides if adjust the variance to 0, ndarray is used to set different variances
    index: list, callable, index of columns need to be standardized, defalut to all
    
    Return
    ------
    2D ndarray
    """
    data = np.array(data, dtype=float)
    if index:
        if mean is True:
            mean = data[:, index].mean(axis=0)
        elif mean is None or mean is False:
            mean = np.zeros(len(index))
        data[:, index] -= mean
        if not var is None and (not var is False):
            if var is True:
                var = data[:, index].std(axis=0)
            else:
                var = np.array(var)
            std_zero_indices = np.nonzero(var == 0)
            std = var.copy()
            std[std == 0] = 1.0
            data[:, index] /= std
            if list(std_zero_indices[0]):
                for i in std_zero_indices[0]:
                    data[:, index][:, i] *= 0
        else:
            std = 0
    else:
        if mean is True:
            mean = data.mean(axis=0)
        elif mean is None or mean is False:
            mean = np.zeros(data.shape[1])
        else:
            mean = np.array(mean)
        data -= mean
        if not var is None and (not var is False):
            if var is True:
                var = data.std(axis=0)
            else:
                var = np.array(var)
            std_zero_indices = np.nonzero(var == 0)
            std = var.copy()
            std[std == 0] = 1.0
            data /= std
            if list(std_zero_indices[0]):
                for i in std_zero_indices[0]:
                    data[:, i] *= 0
        else:
            std = 0
    return (data, mean, std)

def minmax(data, feature_range=(0, 1), min_max=None, index=None):
    """
    归一化数据
    X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    X_new = X_std * (feature_range[1] - feature_range[0]) + feature_range[0]
    
    参数
    ----
    data：二维ndarray数据
    feature_range：元组类型，可选，需要转换的范围，默认为(0, 1)
    min_max：元组类型，可选，用于设定最大最小值
    index：列表类型，可选，需要进行标准化的列的索引，默认为全部
    
    返回
    ----
    元组，(归一化后的数据, (最小值，最大值))
    
    
    Normalize data
    X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    X_new = X_std * (feature_range[1] - feature_range[0]) + feature_range[0]
    
    Parameters
    ----------
    data: 2D的ndarray数据
    feature_range: tuple, callabel, final range of transformed data
    min_max: tuple, callable, set min and max values
    index: list, callable, index of columns need to be standardized, defalut to all
    
    Return
    ------
    tuple, (Normalized data, (miniment, maximent))
    """
    data = np.array(data, dtype=float)
    if index:
        if not min_max:
            min_max = (data[:, index].min(axis=0), data[:, index].max(axis=0))
        length = min_max[1] - min_max[0]
        data[:, index] = (data[:, index] - min_max[0]) / length
        data[:, index] = data[:, index] * (feature_range[1] - feature_range[0]) + feature_range[0]
    else:
        if not min_max:
            min_max = (data.min(axis=0), data.max(axis=0))
        length = min_max[1] - min_max[0]
        data = (data - min_max[0]) / length
        data = data * (feature_range[1] - feature_range[0]) + feature_range[0]
    return (data, min_max)

def normalizer(data, index=None, norm=2):
    """
    正则化数据
    
    参数
    ----
    data：二维ndarray数据
    index：列表形式，可选，需要进行标准化的列的索引，默认为全部
    norm：整型或字符串类型，可选大于0的整数或'max'
        当norm为整数p时，表示进行lp正则化；
        当norm='max'时，表示使用最大范数进行正则化
    
    返回
    ----
    2D ndarray
    
    
    Normalize the data
    
    Parameters
    ----------
    data: 2D的ndarray数据
    index: list, callable, index of columns need to be standardized, defalut to all
    norm: int or str, callabel, an integer greater than 0 or 'max' are optional
        When norm is an integer p, it means lp normalization
        When norm='max', it means that the maximum norm is used for normalization
    
    Return
    ------
    2D ndarray
    """
    data = np.array(data, dtype=float)
    if norm != 'max':
        if index:
            distance_list = abs(data[:, index]) ** norm
            distance_list = distance_list.sum(axis=1)
            distance_list = distance_list ** (1 / norm)
            distance_list[distance_list == 0] = 1
            data[:, index] /= np.array([distance_list]).T
        else:
            distance_list = abs(data) ** norm
            distance_list = distance_list.sum(axis=1)
            distance_list = distance_list ** (1 / norm)
            distance_list[distance_list == 0] = 1
            data /= np.array([distance_list]).T
    elif norm == 'max':
        if index:
            data[:, index] /= np.array([abs(data[:, index]).max(axis=1)]).T
        else:
            data /= np.array([abs(data).max(axis=1)]).T
    else:
        raise Exception("Wrong type of paramter 'norm'.")
    return data

def onehot(data, index=None):
    """
    将数据转换为one-hot编码
    
    参数
    ----
    data：二维ndarray数据
    index：列表形式，可选，需要进行标准化的列的索引，默认为全部
    
    返回
    ----
    元组，(onehot编码数据, 名称列表)
    
    
    Transform data to one-hot encoding
    
    Parameters
    ----------
    data: 2D的ndarray数据
    index: list, callable, index of columns need to be standardized, defalut to all
    
    Return
    ------
    tuple, (one-hot data, name list)
    """
    if not index:
        index = np.arange(data.shape[1]).tolist()
    ls_all = []
    for i in index[::-1]:
        ls = list(set(data[:, i]))
        ls_all.append(ls)
        data_new = np.zeros((data.shape[0], len(ls)))
        for j in range(len(ls)):
            data_new[data[:, i] == ls[j], j] = 1
        data = np.hstack((data[:, :i], data_new, data[:, i + 1:]))
    return (data, ls_all[::-1])

def pca(data, n=None, eig_vector=None):
    """
    主成分分析
    
    参数
    ----
    data：二维数组，数据
    n：数类型，可选，当n >= 1时，表示降至n维，当0< n < 1时，表示降维至累计方差贡献率 >= n，默认不降维
    eig_vector：元组类型，可选，用于设定不同的特征向量，当设置该参数时，累计方差贡献率无意义，默认为None
    
    返回
    ----
    元组，(转换后的数据, (累计方差贡献率, 各主成分方差, 各主成分方差贡献率), 特征向量)
    
    
    Principal Component Analysis
    
    Parameters
    ----------
    data：2D array, data
    n: num, callable, when n > = 1, it means to reduce the dimension to n; when 0 < n < 1, it means to reduce the dimension to cumulative variance ratio > = n, and it is not reduced by default
    eig_value_vector: tuple, callable, set different eigenvectors, when this parameter is set, the cumulative variance ratio is meaningless, default=None
    
    Return
    ------
    tuple, (transformed data, (cumulative variance ratio, variance, variance ratio), eigenvectors)
    """
    data = np.array(data, dtype=float)
    if eig_vector is None or eig_vector is False:
        cov_mat = np.cov(data.T)
        (eig_value, eig_vector) = np.linalg.eig(cov_mat)
        sort_index = np.flipud(np.argsort(eig_value))
        eig_value = eig_value[sort_index]
        eig_vector = eig_vector[:, sort_index]
        eig_ratio = eig_value / eig_value.sum()
        contri = 0
        if not n is None and (not n is False):
            if n >= 1:
                n = int(n)
                contri = eig_ratio[:n].sum()
            elif n < 1:
                for i in range(eig_value.shape[0]):
                    contri += eig_ratio[i]
                    if contri >= n:
                        n = i + 1
                        break
            eig_value = eig_value[:n]
            eig_ratio = eig_ratio[:n]
            eig_vector = eig_vector[:, :n]
        else:
            contri = 1
    else:
        contri = None
        eig_value = None
        eig_ratio = None
    data = np.dot(data, eig_vector)
    return (data, (contri, eig_value, eig_ratio), eig_vector)

class RC:
    """
    相关系数
    
    参数
    ----
    *arg：列表类型
    
    属性
    ----
    rc_mat：相关系数矩阵
    
    
    correlation coefficient
    
    Parameter
    ---------
    *arg: list
    
    Attribute
    ---------
    rc_mat: correlation coefficient matrix
    """

    def __init__(self, *arg):
        arg = np.array(arg, dtype=float)
        if len(arg.shape) != 2:
            raise Exception('Input list should be 1D.')
        else:
            self.rc_mat = _rc(arg)

    def __img_process(self, index, cmap):
        plt.matshow(self.rc_mat, cmap=cmap)
        plt.colorbar()
        if index:
            n_list = range(len(index))
            plt.xticks(n_list, index)
            plt.yticks(n_list, index)

    def show(self, index=None, cmap='Blues'):
        """
        作图并显示
        
        参数
        ----
        index：列表形式，可选，各数组名称
        cmap：字符串形式，可选，颜色板，默认为'Blues'
        
        
        Display the image
        
        Parameters
        ----------
        index: list, callable, names of each array
        cmap: str, callable, color board, default='Blues'
        """
        self.__img_process(index=index, cmap=cmap)
        plt.show()

    def savefig(self, filename, index=None, cmap='Blues'):
        """
        作图并保存
        
        参数
        ----
        filename：字符串形式，文件名
        index：列表形式，可选，各数组名称
        cmap：字符串形式，可选，颜色板，默认为'Blues'
        
        
        Save the image
        
        Parameters
        ----------
        filename: str, file name
        index: list, callable, names of each array
        cmap: str, callable, color board, default='Blues'
        """
        self.__img_process(index=index, cmap=cmap)
        plt.savefig(filename)