# Djangotest
农业种植数据可视化系统

本项目使用Django,Echarts,BootStrap等框架编写

本项目的运作流程如下:
1.用户访问url,返回urls所索引的视图函数
2.视图函数处理好前端发送的请求,根据请求是get还是post方式来返回特定页
3.数据库上通过models,即django自带的orm框架管理,但是在视图函数中需要编写modelform来进行数据的校验,可能需要编写正则表达式与钩子函数
4.在modelform中若需要添加bootstrap样式,则需要添加widget插件或者重写modelform的构造方法
5.视图函数中实例化modelform后就可以进行数据的检验了
6.最后返回可能被数据替换占位符后的html,用户浏览器再进行数据遍历渲染

插件上:在utils中封装了BootStrap在ModelForm中使用的类,以及一个分页类,而echarts以及jquery都存放在static中
模板可以通过继承layout基类来进行导入渲染

echarts上:
其中后端传向前端的数据,后端从model实例中取出且构造好的echarts格式再发送
前端通过Ajax接收,在fucntion init()中统一进行初始化
