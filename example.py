"""使用示例

这个文件展示了如何在 Python 代码中直接使用 GoogleSearchCapture 类
"""

import asyncio
from google_keyworder.main import GoogleSearchCapture


async def main():
    """示例主函数"""

    # 示例 1: 截图
    print("示例 1: 对 'Python 教程' 进行截图")
    capturer1 = GoogleSearchCapture("Python 教程", "output")
    screenshot_path = await capturer1.search_and_screenshot(wait_time=3)
    print(f"截图已保存: {screenshot_path}")

    # 示例 2: 录影
    print("\n示例 2: 对 '机器学习' 搜索过程进行录影")
    capturer2 = GoogleSearchCapture("机器学习", "output")
    video_path = await capturer2.search_and_record(duration=10)
    print(f"录影已保存: {video_path}")


if __name__ == "__main__":
    asyncio.run(main())
