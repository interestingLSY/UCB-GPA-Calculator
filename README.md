# UCB 申请系统绩点计算器

本程序能够根据输入的课程、成绩和学分，计算各种 GPA，包括：

- 总 GPA: Cumulative Undergraduate GPA
- 大三学年 GPA: Advanced GPA (all courses completed after the second year)
- 专业绩点：GPA for courses in the major field of study

## 使用方法

找个有 Python 的环境，clone 该仓库，修改 calculator.py 中的 raw_data 并运行 calculator.py 即可。

修改 calculator.py 的方式如下：

- 登录北京大学信息门户，点击“我的成绩”，并点击“本课程成绩”，将整个网页，从“23-24学年度2学期”开始，复制到结尾
- 删去表头那一行：“课程名称	英文名称	课程类别	学分	成绩	绩点”
- 在每个课程的前面加上 "+" 号或 "-" 号，后跟一个 tab。"+" 表示该门课程为专业课程，"-" 表示该门课程为非专业课程。在计算专业绩点的时候，只会计算那些 mark 了 "+" 的课程。

calculator.py 中有一个例子，可以参考。

## 注意事项

注意事项：
- 请检查该脚本计算的“总 GPA”与学校计算的是否一致
