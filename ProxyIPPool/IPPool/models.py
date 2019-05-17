from django.db import models

# Create your models here.

"""
"ip": proxy_ip,
        "port": proxy_port,
        "protocol": protocol,
        "types": types,
        "speed": speed,
        'ip_address': ip_address
"""
# types = 0  # 1高匿 2普匿 3透明
# protocol = 0  # 0无 1http 2https 3http+https


class ProxyIP(models.Model):
    """
    可用代理ip信息
    """
    PROTOCOL = (
        (0, '未知'),
        (1, 'http'),
        (2, 'https'),
        (3, 'http + https')
    )
    TYPES = (
        (0, '未知'),
        (1, '高匿'),
        (2, '普匿'),
        (3, '透明')
    )
    protocol = models.SmallIntegerField(choices=PROTOCOL, default=0, verbose_name='代理类型')
    types = models.SmallIntegerField(choices=TYPES, default=0, verbose_name='匿名程度')
    ip = models.CharField(max_length=16, null=True, verbose_name='ip')
    port = models.CharField(max_length=12, null=True, verbose_name='端口号')
    speed = models.CharField(max_length=12, null=True, verbose_name='响应速度')
    ip_address = models.CharField(max_length=64, null=True, verbose_name='ip地址')
    verify_time = models.DateTimeField(auto_now=True, verbose_name='最后验证时间')

    class Meta:
        db_table = 'proxy_ip'

