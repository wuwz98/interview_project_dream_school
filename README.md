# interview_project_dream_school

## 第一题

看到附件中说“将py文件放在一个公开repo中”，没太get到这个py文件是指什么

代码编写过程尽量符合生产规范（不频繁修改py文件，通过命令行或者shell启动）

题目中仅说了提交py文件，不考虑部署，因此：
1. 没有添加requirements.txt
2. 没有做任何操作确保chromedriver和本地浏览器版本相同
3. 没有考虑跨平台，本项目在win10下运行

## 第二题

使用一个stack做简单的()匹配

题目要求)未匹配标记?，遍历到)只要检查stack是否为空

但是题目还要求在对应的(位置标记，这里取巧记录一下入栈(的下标，最后再扫一遍即可

假设字符串长度n

最坏情况下扫描两次字符串，因此时间复杂度O(n)

使用两个数组记录相关信息，因此空间复杂度O(n)
