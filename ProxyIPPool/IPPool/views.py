from django.http import JsonResponse, HttpResponse

# Create your views here.
from IPPool.models import ProxyIP


def index(requests):
    """
    返回到说明页
    :param requests:
    :return:
    """
    context = '<h3>1.访问接口http://localhost/api/fetch/ 随机返回一个代理ip信息</h3> <br/>' \
              '<h3>2.访问接口http://localhost/api/random/{个数}, 随机返回指定个数</h3> <br/>'
    return HttpResponse(context)


def fetch(requests):
    """
    随机返回一个ip信息
    :param requests:
    :return:
    """
    proxy_info = ProxyIP.objects.order_by('?').first()
    if proxy_info:
        data = {
            'code': '200',
            'msg': 'success',
            'ip_info': {
                'protocol': proxy_info.get_protocol_display(),
                'types': proxy_info.get_types_display(),
                'ip': proxy_info.ip,
                'port': proxy_info.port,
                'speed': proxy_info.speed,
                'ip_address':proxy_info.ip_address,
                'verify_time': proxy_info.verify_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    else:
        data = {
            'code': '200',
            'msg': 'Data is empty',
            'ip_info': ''
        }
    return JsonResponse(data)


def random(requests, num):
    """
    随机返回num个数个ip
    :param requests:
    :param num:
    :return:
    """
    try:
        n = int(num)
    except ValueError:
        n = 1
    ip_info_list = ProxyIP.objects.order_by('?')[:n]
    ip_info = []
    for proxy_info in ip_info_list:
        ip_info.append({
            'protocol': proxy_info.get_protocol_display(),
            'types': proxy_info.get_types_display(),
            'ip': proxy_info.ip,
            'port': proxy_info.port,
            'speed': proxy_info.speed,
            'ip_address': proxy_info.ip_address,
            'verify_time': proxy_info.verify_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    data = {
        'code': '200',
        'msg': 'success',
        'ip_info': ip_info
    }
    return JsonResponse(data)