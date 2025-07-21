## Maintainer : Nova_Cao

import tkinter as tk
import tkinter.messagebox
import random
from math import sin, cos, pi, log
from tkinter.constants import *

width = 888
height = 500
heartx = width / 2
hearty = height / 2
side = 11
heartcolor = "pink"  # 爱心颜色
word = "I Love You!"  # 想要写的字

# 爱心类
class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # 生成爱心的原始坐标点
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        
        # 边缘扩散效果
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        
        # 中心扩散效果
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        # 计算点的位置，实现跳动效果
        force = 1 / (((x - heartx) ** 2 + (y - hearty) ** 2) ** 0.520)  # 魔法参数
        dx = ratio * force * (x - heartx) + random.randint(-1, 1)
        dy = ratio * force * (y - hearty) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        # 计算每一帧的点坐标
        ratio = 10 * curve(generate_frame / 10 * pi)  # 圆滑的周期的缩放比例
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        
        all_points = []
        
        # 生成光晕点
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # 处理原始爱心点
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # 处理边缘扩散点
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # 处理中心扩散点
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        # 渲染爱心到画布
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=heartcolor)


def heart_function(t, shrink_ratio: float = side):
    """
    爱心函数，根据参数t生成爱心形状的坐标
    """
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    
    # 缩放和偏移
    x *= shrink_ratio
    y *= shrink_ratio
    x += heartx
    y += hearty
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """
    随机散点函数，在指定点周围生成随机偏移
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
    
    dx = ratio_x * (x - heartx)
    dy = ratio_y * (y - hearty)
    
    return x - dx, y - dy


def shrink(x, y, ratio):
    """
    收缩函数，用于生成光晕效果
    """
    force = -1 / (((x - heartx) ** 2 + (y - hearty) ** 2) ** 0.6)  # 这个参数...
    dx = ratio * force * (x - heartx)
    dy = ratio * force * (y - hearty)
    return x - dx, y - dy


def curve(p):
    """
    周期曲线函数，用于生成平滑的动画效果
    """
    return 2 * (2 * sin(4 * p)) / (2 * pi)


def draw(main: tk.Tk, render_canvas: tk.Canvas, render_heart: Heart, render_frame=0):
    """
    绘制函数，实现动画效果
    """
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)


def love():
    """
    爱心动画主函数
    """
    root = tk.Tk()
    
    # 获取屏幕尺寸
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    
    # 计算窗口居中位置
    x = (screenwidth - width) // 2
    y = (screenheight - height) // 2
    
    # 设置窗口
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.title('跳动的爱心')
    root.resizable(0, 0)
    root.configure(bg='black')
    
    # 创建画布
    canvas = tk.Canvas(root, bg='black', height=height, width=width)
    canvas.pack()
    
    # 添加文字
    label = tk.Label(root, text=word, bg="black", fg="#FF99CC", font="Helvetic 25 bold")
    label.place(relx=.5, rely=.5, anchor=CENTER)
    
    # 创建爱心对象并开始动画
    heart = Heart()
    draw(root, canvas, heart)
    
    root.mainloop()


def OK():
    """
    同意按钮回调函数
    """
    root.destroy()
    love()


def NO():
    """
    拒绝按钮回调函数
    """
    tk.messagebox.showinfo('提示', '真的要拒绝吗TuT')


def closeWindow():
    """
    关闭窗口回调函数
    """
    tk.messagebox.showinfo('提示', '逃避是解决不了问题的owo')


if __name__ == '__main__':
    # 创建初始交互界面
    root = tk.Tk()
    root.title('❤')
    root.resizable(0, 0)
    # Linux环境下移除不支持的属性
    # root.wm_attributes("-toolwindow", 1)
    
    # 获取屏幕尺寸并居中显示
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    x = (screenwidth - 400) // 2
    y = (screenheight - 300) // 2
    root.geometry("400x300+%d+%d" % (x, y))
    root.configure(bg='#FFB6C1')
    
    # 创建标题
    title_label = tk.Label(root, text='💕 浪漫时刻 💕', 
                          bg='#FFB6C1', fg='#FF1493', 
                          font=('Arial', 20, 'bold'))
    title_label.pack(pady=30)
    
    # 创建问题文本
    question_label = tk.Label(root, text='你愿意看我为你准备的\n跳动爱心吗？', 
                             bg='#FFB6C1', fg='#8B008B', 
                             font=('Arial', 14))
    question_label.pack(pady=20)
    
    # 创建按钮框架
    button_frame = tk.Frame(root, bg='#FFB6C1')
    button_frame.pack(pady=30)
    
    # 同意按钮
    yes_button = tk.Button(button_frame, text='好呀好呀 💖', 
                          command=OK, bg='#FF69B4', fg='white',
                          font=('Arial', 12, 'bold'), 
                          width=10, height=2)
    yes_button.pack(side=tk.LEFT, padx=20)
    
    # 拒绝按钮
    no_button = tk.Button(button_frame, text='我很抱歉 💔', 
                         command=NO, bg='#DC143C', fg='white',
                         font=('Arial', 12, 'bold'), 
                         width=10, height=2)
    no_button.pack(side=tk.RIGHT, padx=20)
    
    # 绑定关闭事件
    root.protocol("WM_DELETE_WINDOW", closeWindow)
    
    # 启动主循环
    root.mainloop()
