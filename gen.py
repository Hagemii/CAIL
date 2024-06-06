import random
import os

# 前提: ok.txt 文件存在，并且可以被访问。
file_path_ok = "ok.txt"

# 定义输出文件
file_path_train = "train.txt"
file_path_val = "val.txt"
file_path_test = "test.txt"

# 读取文件
with open(file_path_ok, 'r') as file:
    lines = file.readlines()

# 打乱行
random.shuffle(lines)

# 计算划分位置
total_lines = len(lines)
train_lines = total_lines * 6 // 10
val_lines = total_lines * 2 // 10
test_lines = total_lines - train_lines - val_lines

# 创建并写入 train.txt
with open(file_path_train, 'w') as file:
    file.writelines(lines[:train_lines])

# 创建并写入 val.txt
with open(file_path_val, 'w') as file:
    file.writelines(lines[train_lines:train_lines+val_lines])

# 创建并写入 test.txt
with open(file_path_test, 'w') as file:
    file.writelines(lines[train_lines+val_lines:])

print("Files successfully split.")
