# 1.导入模块
import socket
import threading
from collections import Counter
from common import get_host_ip

caiminglist = ['牛油火锅', '鸳鸯火锅', '菌汤锅底', '番茄锅底', '三鲜锅底', '虾滑', '毛肚', '火锅牛排', '精品小肥羊', '秘制羊肉', '土豆', '娃娃菜', '金针菇', '藕片',
               '甜玉米']
lock = threading.Lock()


# 处理菜名数据
def bao_cai(recv_text):
    # 桌号
    zhuohao = recv_text[1:recv_text.find("!")]
    print("桌号为：", zhuohao)
    # 人数
    renshu = recv_text[recv_text.find("!") + 1:recv_text.find("&")]
    print("人数为：", renshu)
    # 菜名代号
    caimingdaihao = recv_text[recv_text.find("&") + 1:recv_text.find("#")]
    print("菜名代号：", caimingdaihao)
    # 价格
    jiage = recv_text[recv_text.find("#") + 1:]
    print("价格：", jiage)
    d1 = []
    d2 = []
    caiming = ""
    n = len(caimingdaihao)
    l = [caimingdaihao[i - 1] + caimingdaihao[i] for i in range(n) if i % 2 != 0]
    for i in l:
        d1.append(caiminglist[int(i)])
        if i[0] == "0":
            d2.append(int(i))
    print(d1)
    daihao = ''.join(str(i) for i in d2)
    print(daihao)
    count = Counter(list(d1))
    for key, value in count.items():
        caiming += (key + "*" + str(value) + "\n")
    print("菜名：", caiming)
    # print(time.time()," ---  recv --> ", recv)  # 打印一下子
    lock.acquire(True)
    lock.release()


# 接收APP数据
def recv_msg(new_tcp_socket, ip_port):
    recv_data = new_tcp_socket.recv(1024)
    while recv_data:
        # 8.解码数据并输出
        recv_text = recv_data.decode('gbk')
        print('来自[%s]的信息：%s' % (str(ip_port), recv_text))
        if recv_text[0] == "A":  # 接收菜名
            bao_cai(recv_text)
        elif recv_text[0] == "B":  # 呼叫服务员
            lock.acquire(True)
            print("呼叫服务员")
            lock.release()
        elif recv_text[0] == "C":  # 转到支付宝 并添加到历史订单
            lock.acquire(True)
            print("结账支付")
            lock.release()
        recv_data = new_tcp_socket.recv(1024)
    # 关闭客户端连接
    new_tcp_socket.close()

# 获取ip并打印
print("ip地址为:", get_host_ip())
# 2.创建套接字
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 3.设置地址可以重用
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
# 4.绑定端口
tcp_server_socket.bind((get_host_ip(), 8080))

# 5.设置监听，套接字由主动变为被动
tcp_server_socket.listen(10)

# 用一个while True来接受多个客户端连接
while True:
    # 6.接收客户端连接
    new_tcp_socket, ip_port = tcp_server_socket.accept()
    print('新用户[%s]连接' % str(ip_port))

    # 创建线程
    thread_msg = threading.Thread(target=recv_msg, args=(new_tcp_socket, ip_port))
    # 子线程守护主线程
    thread_msg.setDaemon(True)
    # 启动线程
    thread_msg.start()

# tcp_server_socket.close()
