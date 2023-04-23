from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError


# Create your views here.

def depart_list(request):
    """部门列表"""

    # 获取数据(queryset)

    queryset = models.Department.objects.all()

    return render(request, "depart_list.html", {"queryset": queryset})


def depart_add(request):
    """添加部门"""
    if request.method == "POST":
        title = request.POST.get("title")
        models.Department.objects.create(title=title)
        return redirect("/depart/list/")
    else:
        return render(request, "depart_add.html")


def depart_delete(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


# nid为前端页面通过django正则传递过来的数据
def depart_edit(request, nid):
    """修改部门"""
    # 获取queryset的对象
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_object": row_object})
    title = request.POST.get("title")
    # 更新
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect("/depart/list/")


def user_list(request):
    """用户管理"""

    # 获取用户列表
    queryset = models.UserInfo.objects.all()

    # for obj in queryset:
    #     # get_字段_display()
    #     print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender,obj.get_gender_display())
    #     # print(obj.depart_id)
    #     # obj.depart 自动根据depart_id去外键约束关联的表中获取depart对象

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, "user_list.html", context)


def user_add(request):
    """添加用户"""
    return render(request, "user_add.html")


################################################# ModelFrom #######


from django import forms


# modelForm数据展示与校验,且刷新后保留之前输入的数据
class UserModelForm(BootStrapModelForm):
    # 若meta的字段需要更多的校验,可在UserModelForm的成员变量中重写字段,如
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "create_time", "gender"]
        # 利用插件定制modelform的input的class属性的方法
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password":forms.PasswordInput(attrs={"class": "form-control"}),
        # }

    # 基于Django源码得到的更加方便的添加插件(bootstrap)的方法:
    # 重写构造方法,首先调用父类构造方法,遍历内部类的fields,把每个字段加入插件,且插件attrs属性添加好样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """添加用户"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    # post请求
    form = UserModelForm(data=request.POST)
    # 数据校验,.is_valid()
    if form.is_valid():
        # print(form.cleaned_data)
        # 没有必要models.UserInfo.objects.create()了,直接用form.save()自动数据库存储
        form.save()
        return redirect("/user/list/")
    # 校验失败
    else:
        return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    # 获取前端传过来的id的行数据queryset
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})
    # 实例化modelForm以便于数据校验,加入instance可以使得form.save时用于更新数据而不是添加
    form = UserModelForm(data=request.POST, instance=row_object)
    # 数据校验
    if form.is_valid():
        # 数据更新
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def admin_list(request):
    queryset = models.Admin.objects.all()
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, "admin_list.html", context)


class AdminModelForm(BootStrapModelForm):
    # 添加密码样式
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            # 添加密码样式
            "password": forms.PasswordInput
        }

    # 钩子函数判断确认密码
    def clean_confirm_password(self):
        confirm = self.cleaned_data.get("confirm_password")
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("两次输入密码不一致!")

        # 字段保存到数据库的值
        return confirm


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    title = "编辑管理员"
    row_object = models.Admin.objects.filter(id=nid)
    if row_object:
        form = AdminModelForm()
        return render(request, "admin_edit.html", {"form": form, "title": title})
    return redirect("/admin/list/")


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def chart_list(request):
    row_object = models.Environment.objects.all()

    return render(request, "chart_list.html", {"queryset": row_object})


from django.http import JsonResponse


def chart_bar(request):
    objects = models.Environment.objects.all()
    time_list = []
    temp_list = []
    ph_list = []
    weather_list = []
    for i in objects:
        time_list.append(i.time)
        temp_list.append(i.temperature)
        # ph_list.append(i.ph)
        # weather_list.append(i.weather)
        # print(i.time, i.temperature, i.ph, i.weather)
    series_list = [
        {
            "data": temp_list,
            "type": 'line',
            "smooth": "true"
        }
    ]
    print(time_list,temp_list)
    result = {
        "status": True,
        "data": {
            "time_list": time_list,
            "temp_list": temp_list,
            "ph_list": ph_list,
            "weather_list": weather_list,
            "series_list": series_list,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    # 获取数据库数据
    objects = models.Environment.objects.all()
    weather_list = []

    # 统计数量,以及改造数据形式来符合echarts的series[0]中的data
    for i in objects:
        num=i.weather.count(i.weather)
        weather_list.append({"value":num,"name":i.weather})
    print(weather_list)
    result = {
        "status": True,
        "data":weather_list
    }
    return JsonResponse(result)

def chart_point(request):

    objects=models.Environment.objects.all()
    ph_list=[]
    time_list = []
    for i in objects:
        ph_list.append(i.ph)
        time_list.append(i.time)
    result={
        "xAxis":time_list,
        "status": True,
        "data":ph_list
    }

    return JsonResponse(result)

