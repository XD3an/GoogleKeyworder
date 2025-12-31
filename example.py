"""使用範例

這個檔案展示了如何在 Python 程式碼中直接使用 GoogleSearchCapture 類別
"""

import asyncio
from google_keyworder.main import GoogleSearchCapture


async def main():
    """範例主函式"""

    # 範例 1: 截圖
    print("範例 1: 對 'Python 教學' 進行截圖")
    capturer1 = GoogleSearchCapture("Python 教學", "output")
    screenshot_path = await capturer1.search_and_screenshot(wait_time=3)
    print(f"截圖已儲存: {screenshot_path}")

    # 範例 2: 錄影
    print("\n範例 2: 對 '機器學習' 搜尋過程進行錄影")
    capturer2 = GoogleSearchCapture("機器學習", "output")
    video_path = await capturer2.search_and_record(duration=10)
    print(f"錄影已儲存: {video_path}")


if __name__ == "__main__":
    asyncio.run(main())
