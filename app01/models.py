from django.db import models


# Create your models here.


class Department(models.Model):
    """作物表"""
    # verbose_name是一个注解参数,可写可不写
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # 数字长度为10, 小数占2位 ,新来的账户默认为0
    # account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    # 下面的DateField不会包括秒
    create_time = models.DateField(verbose_name="创建时间")

    # 外键,需要添加外键约束,depart_id只能是部门表中目前存在的id
    # depart_id = models.BigIntegerField(verbose_name="部门id") 这样写没有约束,没有外键关联
    # Django会自动将外键字段加上_id,即depart_id
    # 部门被删除(一般两种情况)
    # 1.级联删除
    # 添加外键约束 ,to表示与哪张表关联,to_field表示与哪一个字段关联,on_delete=models.CASCADE表示级联删除
    # depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # 2.置空
    # 需要允许这一列为空,on_delete设models.SET_NULL
    # depart = models.ForeignKey(to="Department", to_fields="id", null=True, blank=True,on_delete=models.SET_NULL())

    # Django中的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="管理员", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


class Environment(models.Model):
    time=models.DateField(verbose_name="日期",primary_key=True)
    temperature = models.DecimalField(verbose_name="温度",max_digits=4,decimal_places=2,default=0)
    ph=models.DecimalField(verbose_name="ph值",max_digits=4,decimal_places=2,default=0)
    weather=models.CharField(verbose_name="天气",max_length=32)


