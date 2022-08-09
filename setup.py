'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-06-16 22:44:15
Description: 
'''
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    # 项目名称
    name = "elirobots",
    # 版本号
    version = "0.0.4",
    # 作者
    author = "Elite",
    # 邮箱
    author_email = "zhangjunjie@elibot.cn",
    # url地址
    url= "https://github.com/JunJie-zhang-o/eliterobot.git",
    # 描述
    description = "a SDK library for Elite EC Series Robot ",
    # 长描述
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # 安装依赖
    install_requires = ["loguru>=0.6.0"],
    # 自动发现根目录中所有的子包,find_packages()只能打包python包，python包中只有.py而不包括这个文件夹下 其他的数据文件。并且根目录下的.py文件不会被打包进去
    packages = setuptools.find_packages(
        # where=".",
        # include=["elite*"],
        # exclude=["elite.EliteJson_3_0_2",
        #          "elite.ElitePoseCali",
        #          "elite.pose.py"]
        ),

    # 附加信息
    classifiers = [],
    # python版本要求
    python_requites=">3.5",
    # 关键字
    keywords = ["elite","elibot","eliterobot","robot","Robot","robotSDK"]
)