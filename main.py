# encoding: utf-8
import os
import re

import pandas as pd
import xlwt
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import Select

login_url = 'http://aqzsxx.nuaa.edu.cn/sjd/index.aspx'  #移动端

def merge_excel_files(dir, merge_to):
    """
    读取目录 dir 下的所有 excel 文件, 合并成一个 excel, 写入 merge_to 文件中. 暴力合并, 不考虑字段.
    :param dir: 需要合并的 excel 所在目录
    :param merge_to: 写入文件
    :return: None
    """
    filename_list = os.listdir(dir)
    # read them in
    excels = [pd.ExcelFile(os.path.join(dir, filename)) for filename in filename_list if
              len(filename) > 4 and filename[-4:] in ['.xls', 'xlsx']]
    # turn them into dataframes
    frames = [x.parse(x.sheet_names[0], header=None, index_col=None)
              for x in excels]
    combined = pd.concat(frames)
    combined.to_excel(merge_to, header=False, index=False)


def write2excel(data, write_to, datatype=list):
    """
    将字典/列表 data 中的数据写入到 excel 文件 (specified by write_to) 中.
    使用字典的好处在于方便去重～
    :param data: 类型为 dict/list.
        如果类型为字典，例如 data = {'a':['b', 'c', 'd'],
                         '0':['1', '2', '3']}
        则在 excel 中为:
            a   b   c   d
            0   1   2   3
        如果类型为列表, 例如 data = [['a', 'b', 'c', 'd'],
                         [ 0,   1,   2,  3]]
        则在 excel 中为:
            a 0
            b 1
            c 2
            d 3
    :param write_to: 写入的文件名
    :datatype: 传入的 data 类型, list or dict
    :return: None
    """
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(
        'sheet1', cell_overwrite_ok=True)

    if datatype == dict and type(data) == dict:
        curr_row = 0
        for key in data.keys():
            worksheet.write(curr_row, 0, key)  # 第 0 列写入key
            for col in range(len(data[key])):  # 写入其他列
                worksheet.write(curr_row, col + 1, data[key][col])
            curr_row += 1
    elif datatype == list and type(data) == list:
        # 例如 data = [['A', 'B', 'C'], ['1', '2', '3'], ['AI', 'ML', 'DL']]
        # 则 ['A', 'B', 'C'] 写入 excel 的第一列, 以此类推
        for col in range(len(data)):
            for row in range(len(data[col])):
                worksheet.write(row, col, data[col][row])
    else:
        print("type must be either dict or list.")
        return

    print("文件已保存为 " + write_to)
    workbook.save(write_to)


def get_answer(user_id='sx1801001', password='123456', write_to='key.xls'):
    """
    获得所有考试试题的答案
    """
    ques_list = []
    ans_list = []

    if user_id[:2].lower() == 'sx':
        # select_list = [117, 118, 119, 120, 121, 122, 123] #每个学院，以及专硕学硕需要了解的知识都不同
        select_list = [ 118, 119, 120, 121, 122, 123] #每个学院，以及专硕学硕需要了解的知识都不同
        # select_list = [ 118, 119, 120, 123] #每个学院，以及专硕学硕需要了解的知识都不同
        # select_list = [ 117] #每个学院，以及专硕学硕需要了解的知识都不同

    else:
        # select_list = [117, 121, 122, 123]
        select_list = [117, 118, 119, 120, 121, 122, 123] #每个学院，以及专硕学硕需要了解的知识都不同
        

    driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application/chromedriver.exe')
    # login
    driver.get(login_url)
    driver.find_element_by_id('TextBox1').send_keys(user_id)
    driver.find_element_by_id('TextBox2').send_keys(password)
    driver.find_element_by_id('Button1').click()
    for x in select_list:
        #将每个序号x单独存放为一个exl表格
        str_list=list(write_to)
        nPos=str_list.index('.')
        str_list.insert(nPos,str(x))
        str_2="".join(str_list)
        # print(str_2)
        # input()
        driver.get('http://aqzsxx.nuaa.edu.cn/sjd/StartExercise_Mobile.aspx?Start=yes')
        select = Select(driver.find_element_by_name('drpSubject'))
        select.select_by_value(str(x))

        while driver.find_element_by_name('nextbtn').is_enabled():
            driver.find_element_by_name('nextbtn').click()
            page_code = driver.page_source
            html = etree.HTML(page_code)
            ques_list.append(html.xpath('//*[@id="trTestTypeContent1"]/tbody/tr[1]/td/text()')[0])
            ans_list.append(re.findall(r'答案：(.*?)<', page_code)[0])
        
        write2excel([ques_list, ans_list], write_to=str_2, datatype=list)
        ques_list.clear()
        ans_list.clear()

    
    driver.close()
    



    

   


def take_exam(user_id='sx1801001', password='123456', ans_file='key.xls',
              exam_url='http://aqzsxx.nuaa.edu.cn/PersonInfo/StartJobOne.aspx?PaperID=273&UserID=24326&Start=yes'):
    """
    开始模拟或考试
    :param user_id: 学号
    :param password: 密码
    :param ans_file: get_answer() 中获取的答案文件
    :param exam_url: 模拟考试或者正式考试页面的链接
    """

    
    driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application/chromedriver.exe')
    # login
    driver.get(login_url)
    driver.find_element_by_id('TextBox1').send_keys(user_id)
    driver.find_element_by_id('TextBox2').send_keys(password)
    driver.find_element_by_id('Button1').click()

    excel = pd.read_excel(ans_file, header=None)
    ques_list = list(excel.iloc[:, 0])
    ans_list = list(excel.iloc[:, 1])

    driver.get(exam_url)

    break_flag = False
    que_num = 0

    while True:
        page_code = driver.page_source
        html = etree.HTML(page_code)
        question = html.xpath('/html/body/form/table/tbody/tr[5]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/text()')[0]
        # 搜索答案
        i = 0
        for i in range(len(ques_list)):
            if ques_list[i] in question:
                if '判断题' in page_code:
                    driver.find_element_by_xpath('//tbody/tr/td/input[@value="' + ans_list[i] + '"]').click()
                    break

                elif '单选题' in page_code:
                    if len(ans_list[i]) == 1:
                        # driver.find_element_by_xpath('//*[@value="' + ans_list[i] + '"]').click()
                        driver.find_element_by_xpath('//tbody/tr/td/input[@value="' + ans_list[i] + '"]').click()
                        break

                else:
                    if len(ans_list[i]) > 1:
                        try:
                            for j in range(len(ans_list[i])):
                                driver.find_element_by_xpath(
                                    '//tbody/tr/td/input[@value="' + ans_list[i][j] + '"]').click()
                            break
                        except:
                            print("题库中没有找到该题答案，开启猜题模式！")
        
        que_num = que_num + 1
        if break_flag:
            break
        if i == len(ques_list) - 1 :            
            print("未找到题目："+str(que_num)+"---"+question)
            print("请自己答题")
            os.system("pause")

        driver.find_element_by_name('nextbtn').click()  # 下一题
        if not driver.find_element_by_id('nextbtn').is_enabled():  # 检测是否做完
            break_flag = True

    # driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[4]/td/input[5]').click()  # 点击提交答卷
    driver.find_element_by_name('submitbtn3').click()
    driver.find_element_by_xpath('//*[@id="yes"]').click()  # 点击确定
    print("考试已完成!")
    driver.close()


if __name__ == '__main__':
    # 爬取题库的答案
    # get_answer('SX2016140', 'SX2016140', write_to='D:\GitHub\Pass-Nuaa-Lab-Exam_1\key_.xls')
    # merge_excel_files("D:\GitHub\Pass-Nuaa-Lab-Exam_1", "D:\GitHub\Pass-Nuaa-Lab-Exam_1\key.xls")

    exam_url='http://aqzsxx.nuaa.edu.cn/sjd/StartJobMobile.aspx?PaperID=91&Start=yes'
              
    take_exam(user_id='SX2016140',  # 学号
              password='SX2016140',  # 密码
              ans_file='D:\GitHub\Pass-Nuaa-Lab-Exam_1\key.xls',  # 答案文件
              exam_url=exam_url)

              
