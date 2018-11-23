from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from utils.send_email import send_register_email

# 并集运算
from django.db.models import Q

# 实现用户名或密码均可登录的类
# 继承自ModelBackend类,因为它有方法authenticate,可点进源码查看
from django.views.generic.base import View

from users.forms import LoginForm, RegisterForm, ActiveForm
from .models import UserProfile, EmailVerifyRecord


# 有关用户认证的方法
class CustomBackend(ModelBackend):
    # 重写这个方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个,get只能有一个.两个get失败.Q为使用并集查询,和and是交集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django的后台中密码加密:所以不能直接passwrod = passord,要先将明文密码通过转换,转换为加密之后的密码
            if user.check_password(password):
                return user

        except Exception as e:
            return None


# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        # 自己瞎输的验证码
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效", "active_form": active_form})


# 注册视图类
class RegisterView(View):
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 邮箱注册的逻辑
            user_name = request.POST.get("email", '')
            pass_word = request.POST.get("password", '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认激活状态是False
            user_profile.is_active = False
            # 使用auth模块对密码进行加密make_password
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送注册激活邮箱
            send_register_email(user_name, "register")

            return render(request, 'login.html')
        # 注册邮箱form验证失败
        else:
            return render(request, 'register.html', {"register_form": register_form})


# 登录视图类
class LoginView(View):
    def get(self, request):
        # render就是渲染html返回用户
        return render(request, 'login.html', {})

    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的usernamepassword，会对应到form中
        login_form = LoginForm(request.POST)
        # is_valid判断我们字段是否有执行我们的原有的逻辑,验证失败跳回到login页面
        if login_form.is_valid():
            # 取不到的时候为空,username,password为前端页面标签元素的name属性值.
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 使用auth模块的authenticate方法进行验证,成功返回user,失败返回null
            user = authenticate(username=username, password=password)

            # 如果不是null
            if user:
                # auth模块的login方法,两个参数request,user
                # 实际上是对request写了一部分东西进去,然后在render的时候:
                # request是要render回去的.这些信息也就随着返回给浏览器,完成登录
                login(request, user)
                # 跳转到首页 user,request会被带回到首页
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {"msg": '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 之前的基于函数的视图
def user_login(request):
    # POST请求
    if request.method == "POST":
        # 取不到的时候为空,username,password为前端页面标签元素的name属性值.
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 使用auth模块的authenticate方法进行验证,成功返回user,失败返回null
        user = authenticate(username=username, password=password)

        # 如果不是null
        if user:
            # auth模块的login方法,两个参数request,user
            # 实际上是对request写了一部分东西进去,然后在render的时候:
            # request是要render回去的.这些信息也就随着返回给浏览器,完成登录
            login(request, user)
            # 跳转到首页 user,request会被带回到首页
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {"msg": '用户名或密码错误'})

    # GET请求
    elif request.method == 'GET':
        return render(request, 'login.html', {})
