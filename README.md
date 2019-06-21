# proxy_ip_pool

说明：使用django框架和requests库搭建
可以访问http://47.102.205.85:9000/ 显示示例 渣渣云服务器，里面只有有测试数据，勿大量请求。

### 运行环境

- python3 和mysql数据库

### 下载使用

- 下载源码

```shell
git clone https://github.com/pangxiaobin/proxy_ip_pool.git

或者在https://github.com/pangxiaobin/proxy_ip_pool下载zip文件
```

- 安装依赖

```shell
pip install -i https://pypi.douban.com/simple/ -r requments.txt
```
-创建数据库
```shell
mysql -uroot -p
create database ippool charset=utf8;
```

- 配置项目

```python
# ProxyIPPool/settings.py 基本的配置文件
# Database 使用mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ippool', # db name
        'USER': 'root', # 用户名
        'PASSWORD': 'password', # 密码
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

```

```python
# uwsgi.ini
 uwsgi.ini
[uwsgi]
# 监听的ip地址和端口 这里修改访问端口
http=0.0.0.0:8000 
# 配置工程目录 项目所在的绝对路径
chdir=/path/to/proxy_ip_pool/ProxyIPPool/
# 配置项目的wsgi目录。相对于工程目录
wsgi-file=ProxyIPPool/wsgi.py
```
### 生成迁移文件和执行迁移文件
```shell
python manage.py makemigrations
python manage.py migrate
```

### 启动

- 方法一

  ```shell
  cd  ProxyIPPool  # 进入到manage.py这一级
  python manage.py runserver
  # 启动后访问http://127.0.0.1:8000
  ```

- 方式二

  ```shell
  # 使用uwgi 启动服务 这样可以后台启动
  uwsgi --ini uwsgi.ini
  ```

可以使用方式一进行调试运行，方式二进行稳定运行

- 启动爬取代理ip的脚本

  ```shell
  # 调试时运行
  python run.py
  # 在服务器中可以运行　
  nohup python -u run.py >> crawler.out 2>&1 & 
  ```

注意在项目下创建存储日志的文件

```
/ProxyIPPool/log/log.txt
```

### API接口

- 请求方式GET

  - ### http://{运行服务器的ip}/api/fetch/ 随机返回一个代理ip信息

  - ### http://{运行服务器的ip}/api/random/{个数}, 随机返回指定个数
- 首页展示的内容可以在这里IPPool/views.py中修改
```python
# IPPool/views.py

# 修改context 改变返回首页的内容


def index(requests):
    """
    返回到说明页
    :param requests:
    :return:
    """
    context = '<h3>1.访问接口http://{运行服务器的ip}/api/fetch/ 随机返回一个代理ip信息</h3> <br/>' \
              '<h3>2.访问接口http://{运行服务器的ip}/api/random/{个数}, 随机返回指定个数</h3> <br/>'
    return HttpResponse(context)
```
