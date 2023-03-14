import os
origin_path = "./origin_data"
processed_path = "./processed_data"
files = os.listdir(origin_path)

for file in files:
    if not os.path.isdir(file):  # 是否是文件夹，不是文件夹才打开
        fr = open(origin_path + "/" + file, "r", encoding="utf-8")
        lines = fr.readlines()
        num = len(lines)
        # 首先是根据这个file名创建一个新的文件夹
        dir_name = file[0: file.find('.')]
        if not os.path.exists(processed_path + "/" + dir_name):
            os.makedirs(processed_path + "/" + dir_name)
            file_num = 0
            file_path_name = processed_path + "/" + dir_name + "/" + dir_name + str(file_num) + ".txt"
            # 开始遍历每行
            for i in range(0, num):
                if i % 10 == 0 and i != 0:
                    file_num += 1
                    file_path_name = processed_path + "/" + dir_name + "/" + dir_name + str(file_num) + ".txt"
                with open(file_path_name, "a+", encoding='utf-8') as fw:
                    fw.write(lines[i])
                    fw.close()









