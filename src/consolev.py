import bilibili as b

def main():
    while True:
        i = input("请输入BV号.quit退出.")
        if i == "quit":
            break
        video=b.Bilibili(b.Var.setting,i)
        content = str(video)
        if video.isYingXiaoHao():
            content += "疑似营销号！"
        else:
            content += "不是营销号！"
        print(content)
if __name__=="__main__":
    main()
