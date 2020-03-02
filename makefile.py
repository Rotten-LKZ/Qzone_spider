
import os


class MakeST:
    getQQ = ""

    def __init__(self, gqq):
        """

        Args:
            gqq: 需要获取的QQ
        """
        self.getQQ = str(gqq)
        self.make_main_dir()

    def make_dir(self, path):
        path = "{}/{}".format(self.getQQ, path)
        if os.path.isdir(path):
            self.output(0, path)
        else:
            os.makedirs(path)
            self.output(1, path)

    def make_file(self, path, name, file_type, content):
        """

        Args:
            path: 路径
            name: 文件名（请附上后缀）
            file_type: 文件类型（txt，jpg，png，mp4等）
            content: 内容
        """
        path = "{}/{}/{}".format(self.getQQ, path, name)
        if file_type == "txt":
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            f.close()
            self.output(3, path)
        elif file_type == "jpg":
            with open(path, 'wb') as f:
                f.write(content)
            f.close()
            self.output(3, path)
        # print(path)

    def make_main_dir(self):
        if os.path.isdir(self.getQQ):
            self.output(0, self.getQQ)
        else:
            os.makedirs(self.getQQ)
            self.output(1, self.getQQ)

    @staticmethod
    def output(sus, ex):
        """

        Args:
            sus:状态，0-1分别为目录已存在和已创建，2-3分别为文件已存在和已创建
            ex:目录或者文件的路径
        """
        if sus == 0:
            print("目录", ex, "已存在")
        elif sus == 1:
            print("目录", ex, "已创建")
        elif sus == 2:
            print("文件", ex, "已存在")
        elif sus == 3:
            print("文件", ex, "已创建")


if __name__ == "__main__":
    m = MakeST(24859235)
    m.make_file("TMD", "img.png", "png")
