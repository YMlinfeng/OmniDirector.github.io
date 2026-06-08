#!/usr/bin/env python3
import os
import shutil

# ===== 配置区 =====
BASE_DIR = "/Users/mengzijie/Downloads/project/KlingCameraControl.github.io/camera"
DEST_DIR = "/Users/mengzijie/Downloads/project/KlingCameraControl.github.io/camera_wo"
SUFFIX = "_labeled"

# 支持的扩展名（图片 + 视频），小写
EXTS = {".jpg", ".jpeg", ".png", ".mp4", ".mov", ".avi", ".mkv", ".webm"}


def collect_files():
    """遍历 BASE_DIR 下所有符合扩展名的文件，返回完整路径列表"""
    result = []
    for root, _, files in os.walk(BASE_DIR):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXTS:
                result.append(os.path.join(root, f))
    return result


def main():
    # ===== 第一步：把不含 _labeled 的原文件移动到 camera_wo（保留目录结构）=====
    print("===== 开始移动原始文件到 camera_wo =====")
    move_count = 0
    for file in collect_files():
        name, ext = os.path.splitext(os.path.basename(file))
        # 跳过带后缀的（这些是处理后的，要留下）
        if name.endswith(SUFFIX):
            continue

        # 计算相对路径，保持子目录结构
        rel = os.path.relpath(file, BASE_DIR)
        target = os.path.join(DEST_DIR, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)

        shutil.move(file, target)
        print(f"移动: {rel}")
        move_count += 1

    # ===== 第二步：把 _labeled 文件去掉后缀，恢复原始名字 =====
    print("\n===== 开始去除 _labeled 后缀 =====")
    rename_count = 0
    for file in collect_files():
        dir_ = os.path.dirname(file)
        base = os.path.basename(file)
        name, ext = os.path.splitext(base)
        # 只处理带后缀的
        if not name.endswith(SUFFIX):
            continue

        newname = name[: -len(SUFFIX)]
        newfile = os.path.join(dir_, newname + ext)

        shutil.move(file, newfile)
        print(f"重命名: {base}  ->  {newname}{ext}")
        rename_count += 1

    print(f"\n全部完成！移动 {move_count} 个文件，重命名 {rename_count} 个文件。")


if __name__ == "__main__":
    main()