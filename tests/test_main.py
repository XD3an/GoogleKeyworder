"""主程式測試"""

import pytest
from pathlib import Path
from google_keyworder.main import GoogleSearchCapture


def test_google_search_capture_init():
    """測試 GoogleSearchCapture 初始化"""
    capturer = GoogleSearchCapture("測試關鍵字", "test_output")
    assert capturer.keyword == "測試關鍵字"
    assert capturer.output_dir == Path("test_output")


def test_filename_generation():
    """測試檔案名稱產生"""
    capturer = GoogleSearchCapture("Python 教學", "test_output")
    filename = capturer._get_filename("png")
    assert filename.suffix == ".png"
    assert "Python" in filename.stem or "python" in filename.stem.lower()


@pytest.mark.asyncio
async def test_search_and_screenshot():
    """測試搜尋和截圖功能（整合測試）

    注意: 此測試需要網路連線和 Playwright 瀏覽器
    """
    capturer = GoogleSearchCapture("test", "test_output")
    result = await capturer.search_and_screenshot(wait_time=1)
    assert result.exists()
    assert result.suffix == ".png"
    # 清理測試檔案
    result.unlink()
    capturer.output_dir.rmdir()
