import bilibili as b

def main():
    while True:
        i = input("请输入BV号.quit退出.")
        if i == "quit":
            break
        video=b.Bilibili(b.Var.setting,i)
        content = str(video)
        if video.isYingXiaoHao():
            content += "疑似低质量视频！"
        else:
            content += "不是低质量视频！"
        print(content)
if __name__=="__main__":
    main()
