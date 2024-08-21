import re
import os


# 底层读取ini文件内容
def readfile(filepath):
    with open(filepath, 'r') as f:
        file = f.readlines()
        return file


# 基础查询ini文件函数（当前目录下）-->控制函数
def findini():
    filepath = []
    filename = []
    # 第一部分，筛选ini文件，获取路径
    for root, paths, files in os.walk(os.getcwd()):
        for file in files:
            # 此处需要修改为正则表达式匹配以ini结尾的文件，而不能简单地包含ini
            # 又或者完全不用管，后面的匹配标签会自动过滤，只有需要获取MOD文件名称时才需要在这里匹配
            if '.ini' in file and 'disable' not in file:
                filepath.append(os.path.join(root, file))
                filename.append(file)
    # 第二部分，获取文件内容，供取值函数使用
    for i in range(len(filepath)):
        filecontent = readfile(filepath[i])
        if filecontent is not None:
            listfile = gettarget(filecontent)
            diclist.append(listfile)
    # 第三部分，比较新旧文件，输出结果
    for i in range(len(diclist)):
        if i + 1 < len(diclist):
            if compare(diclist[i], diclist[i + 1]) is not None:
                opt = input("请自行辨别以上结果是否需要反转，输入1反转结果：")
                if opt == '1':
                    os.system('cls')
                    compare(diclist[i + 1], diclist[i])
                    break
                else:
                    break


# 获取所有可变化标签和hash值-->主要功能实现
def gettarget(filecontent):
    ovclist = {}
    # 定义正则表达式范围
    tg_ovc = re.compile(r'(\[TextureOverrideComponent)?[0-9]{1,2}]?')  # 模型重绘标签
    tg_ovt = re.compile(r'(\[TextureOverrideTexture)?[0-9]{1,2}]?')  # 贴图重绘标签
    tg_ovs_t = re.compile(r'(\[TextureOverrideShapeKey).*')  # 形态键重绘标签
    tg_rst = re.compile(r'(\[ResourceTexture)?[0-9]{1,2}]?')  # 贴图资源标签
    for i in range(len(filecontent)):
        a = tg_ovc.match(filecontent[i])
        b = tg_ovt.match(filecontent[i])
        c = tg_rst.match(filecontent[i])
        d = tg_ovs_t.match(filecontent[i])
        if a:
            # print(a.group())
            # 该步骤用于提取纯hash值并且保证内容不含空格等特殊字符
            # 格式：标签名：hash
            ovclist[filecontent[i].strip('\n''\t'';'' ')] = filecontent[i + 1].strip('\n''\t'';'' ')
        if b:
            # print(b.group())
            ovclist[filecontent[i].strip('\n''\t'';'' ')] = filecontent[i + 1].strip('\n''\t'';'' ')
        if c:
            # print(c.group())
            ovclist[filecontent[i].strip('\n''\t'';'' ')] = filecontent[i + 1].strip('\n''\t'';'' ')
        if d:
            # print(d.group())
            ovclist[filecontent[i].strip('\n''\t'';'' ')] = filecontent[i + 1].strip('\n''\t'';'' ')
    return ovclist


# 文件对比，获取信息
def compare(list1, list2):
    """
    :list1：一号文件;
    :list2：二号文件;
    :return：返回结果;
    :others：传入的两文件以行读取，通过正则表达式筛选后将经过第一次筛选的信息存入同一字典，
             因为按行读取且进行了对比，所以其标签顺序一定遵循文件内顺序，不会混乱，所以粗
             处的list1和list2分别是字典列表的i和第i+1项目-->mod.ini文件内容特点,部分
             标签下存hash。
             通过对比标签，读取标签一致的hash值数值（防止错位读取），并且删除多余字符，仅
             保留变换前后的hash。
    """
    # 定义一次结果列表，用于存放
    result = []
    # 功能入口，主要过滤
    for key1, value1 in list1.items():
        for key2, value2 in list2.items():
            if key1 == key2:
                if value1 != value2:
                    if 'hash' in value1 and value2:
                        result.append('"{}":"{}",'.format(value1, value2).replace('hash = ', '').strip('\n''\t'';'' '))
    # 定义二次结果列表，用于存放
    test = []
    # 最终筛选入口，过滤重复项
    for i in range(len(result)):
        if i + 1 < len(result):
            if result[i] != result[i + 1]:
                test.append(result[i])
    # 输出
    for i in test:
        print(i)
    return test


if __name__ == '__main__':
    '''
        属性:{
                哈希值列表:hashlist
                
             }
    '''
    diclist = []
    findini()
    input('Done!')
