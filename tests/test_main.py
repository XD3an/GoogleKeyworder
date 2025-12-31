"""主程序测试"""

import pytest
from pathlib import Path
from google_keyworder.main import GoogleSearchCapture


def test_google_search_capture_init():
    """测试 GoogleSearchCapture 初始化"""
    capturer = GoogleSearchCapture("测试关键字", "test_output")
    assert capturer.keyword == "测试关键字"
    assert capturer.output_dir == Path("test_output")


def test_filename_generation():
    """测试文件名生成"""
    capturer = GoogleSearchCapture("Python 教程", "test_output")
    filename = capturer._get_filename("png")
    assert filename.suffix == ".png"
    assert "Python" in filename.stem or "python" in filename.stem.lower()


@pytest.mark.asyncio
async def test_search_and_screenshot():
    """测试搜索和截图功能（集成测试）

    注意: 此测试需要网络连接和 Playwright 浏览器
    """
    capturer = GoogleSearchCapture("test", "test_output")
    result = await capturer.search_and_screenshot(wait_time=1)
    assert result.exists()
    assert result.suffix == ".png"
    # 清理测试文件
    result.unlink()
    capturer.output_dir.rmdir()
