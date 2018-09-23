# 一分钟通过南航的实验室考试

## 简介 

南航的[实验室考试系统](http://aqzsxx.nuaa.edu.cn/)给研究生同学们带来了极大的困扰。尤其是要牺牲自己宝贵的学习和恋爱的时间去完成这种没有意义的考试。

因此，这个项目为解决这一问题而诞生。让大家能够在1分钟之内获得考试的合格证。

## 运行脚本的需求

- Python version >= 3.4
- selenium
- lxml
- xlwt
- xlrd

上述软件包可通过 pip 安装，例如安装 selenium 的命令如下：
```
pip install selenium
```


## 使用方法

修改 [main.py](./main.py)下面的登录信息。填入学号，登录密码，以及考试页面的链接，即可在一分钟之内，以95分以上的成绩完成一次模拟考试。

```python
if __name__ == '__main__':
    
    take_exam(user_id='sx1801001',  # 学号
              password='123456',  # 密码
              ans_file='key.xls',  # 答案文件
              exam_url='http://aqzsxx.nuaa.edu.cn/PersonInfo/StartJobOne.aspx?PaperID=267&UserID=24424&Start=yes')  # 模拟考试或正式考试页面的链接
```

其中 exam_url 填入下图所示红色区域内容：
![](./img/img1.png)

## 常见问题

1. chromedriver 的安装问题，需要把 executable_path 修改为安装chromedriver.exe的路径。详细见[stackoverflow](https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver')的解答。

```python
driver.Chrome(executable_path=r"C:\path\to\chromedriver.exe")
```


## 其他说明

由于不同学院的题库不同，所以项目中提供的题库`key.xls`并非能够总能够让你及格。

因此建议先爬取题库的试题，然后使用爬取的题库进行考试，而不是本项目中默认提供的题库。
```python
if __name__ == '__main__':
    # 爬取题库的答案
    get_answer('sx1801001', '123456', write_to='my_key.xls')

    # 模式考试
    take_exam(user_id='sf180001',  # 学号
              password='123456',  # 密码
              ans_file='my_key.xls',  # 答案文件
              exam_url='http://aqzsxx.nuaa.edu.cn/PersonInfo/StartExamOne.aspx?PaperID=69&UserID=28409&Start=yes')  # 模拟考试或正式考试页面的链接
```

当然，你也可以使用`get_answer`先取得题库，然后手动做题。

另外，如果不放心本脚本的做题效果，你可以在`main.py`的第170行设置断点，自动做完题之后会停止提交试卷，这时候你可以手动检查脚本没有做的题。