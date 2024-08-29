import os
import requests
import threading
import time
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# 图片下载函数
def download_image(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"图片下载成功：{path}")
    except Exception as e:
        print(f"下载图片失败：{url}, 错误信息：{e}")

# 线程工作函数
def worker(url, directory, num_images, pause_time):
    for _ in range(num_images):
        # 暂停指定的时间
        time.sleep(pause_time)

        # 使用时间戳和随机数生成唯一的文件名
        timestamp = int(time.time())
        random_number = random.randint(0, 1000)
        image_name = f"image_{timestamp}_{random_number}.jpg"
        image_path = os.path.join(directory, image_name)

        # 下载图片
        download_image(url, image_path)

# 启动下载的函数
def start_download():
    # 内置的URL
    builtin_url = "https://api.lolimi.cn/API/tup/xjj.php"
    use_builtin_url = messagebox.askyesno("使用内置URL", "是否使用内置的URL进行下载？\n点击'是'使用内置URL，点击'否'输入新URL。")

    url = builtin_url if use_builtin_url else simpledialog.askstring("Input", "请输入随机图片网站的URL:")

    if not url:
        return

    num_threads = simpledialog.askinteger("Input", "请输入线程数:", minvalue=1, maxvalue=100)
    num_images_per_thread = simpledialog.askinteger("Input", "请输入每个线程的任务数:", minvalue=1, maxvalue=100)
    pause_time = simpledialog.askfloat("Input", "请输入每次访问暂停的时间（秒）:", minvalue=0.1, maxvalue=10)

    save_directory = 'downloaded_images'  # 图片保存的目录

    # 创建保存图片的目录
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # 创建线程列表
    threads = []

    # 启动线程
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(url, save_directory, num_images_per_thread, pause_time))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()
    print('任务已完成！！')

# 创建主窗口
root = tk.Tk()
root.title("图片下载器")

# 创建按钮，点击后启动下载
start_button = tk.Button(root, text="开始下载", command=start_download)
start_button.pack(pady=20)

# 启动事件循环
root.mainloop()
