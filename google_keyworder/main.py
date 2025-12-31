"""Google 关键字搜索截图和录影工具 - 主程序"""

import asyncio
import time
from pathlib import Path
from datetime import datetime
import click
from playwright.async_api import async_playwright


class GoogleSearchCapture:
    """Google 搜索截图和录影类"""

    def __init__(self, keyword: str, output_dir: str = "output"):
        self.keyword = keyword
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_filename(self, extension: str) -> Path:
        """生成输出文件名"""
        safe_keyword = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in self.keyword)
        safe_keyword = safe_keyword.replace(' ', '_')[:50]
        return self.output_dir / f"{safe_keyword}_{self.timestamp}.{extension}"

    async def search_and_screenshot(self, wait_time: int = 3) -> Path:
        """执行 Google 搜索并截图

        Args:
            wait_time: 等待页面加载的时间（秒）

        Returns:
            截图文件路径
        """
        screenshot_path = self._get_filename("png")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 访问 Google 搜索
            search_url = f"https://www.google.com/search?q={self.keyword}"
            await page.goto(search_url)

            # 等待页面加载
            await asyncio.sleep(wait_time)

            # 截图
            await page.screenshot(path=str(screenshot_path), full_page=True)

            await browser.close()

        return screenshot_path

    async def search_and_record(self, duration: int = 10) -> Path:
        """执行 Google 搜索并录影

        Args:
            duration: 录影时长（秒）

        Returns:
            录影文件路径
        """
        video_path = self._get_filename("webm")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                record_video_dir=str(self.output_dir),
                record_video_size={"width": 1920, "height": 1080}
            )
            page = await context.new_page()

            # 访问 Google 搜索
            search_url = f"https://www.google.com/search?q={self.keyword}"
            await page.goto(search_url)

            # 等待指定时长
            await asyncio.sleep(duration)

            # 关闭页面和上下文以保存视频
            await page.close()
            await context.close()
            await browser.close()

            # 获取生成的视频文件
            video_files = list(self.output_dir.glob("*.webm"))
            if video_files:
                # 重命名为我们想要的文件名
                latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                latest_video.rename(video_path)

        return video_path


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Google 关键字搜索截图和录影工具

    支持将输入的关键字通过 Google 引擎搜索并截图结果，或使用录影储存过程。
    """
    pass


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', default='output', help='输出目录（默认: output）')
@click.option('--wait', '-w', default=3, help='等待页面加载时间（秒，默认: 3）')
def screenshot(keyword: str, output: str, wait: int):
    """对 Google 搜索结果进行截图

    示例:
        google-keyworder screenshot "Python 教程"
        google-keyworder screenshot "机器学习" -o screenshots -w 5
    """
    click.echo(f"正在搜索关键字: {keyword}")

    capturer = GoogleSearchCapture(keyword, output)
    result_path = asyncio.run(capturer.search_and_screenshot(wait))

    click.echo(f"✓ 截图已保存到: {result_path}")


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', default='output', help='输出目录（默认: output）')
@click.option('--duration', '-d', default=10, help='录影时长（秒，默认: 10）')
def record(keyword: str, output: str, duration: int):
    """对 Google 搜索过程进行录影

    示例:
        google-keyworder record "Python 教程"
        google-keyworder record "机器学习" -o videos -d 15
    """
    click.echo(f"正在搜索关键字: {keyword}")
    click.echo(f"录影时长: {duration} 秒")

    capturer = GoogleSearchCapture(keyword, output)
    result_path = asyncio.run(capturer.search_and_record(duration))

    click.echo(f"✓ 录影已保存到: {result_path}")


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', default='output', help='输出目录（默认: output）')
@click.option('--wait', '-w', default=3, help='截图等待时间（秒，默认: 3）')
@click.option('--duration', '-d', default=10, help='录影时长（秒，默认: 10）')
def both(keyword: str, output: str, wait: int, duration: int):
    """同时进行截图和录影

    示例:
        google-keyworder both "Python 教程"
        google-keyworder both "机器学习" -o results -w 5 -d 15
    """
    click.echo(f"正在搜索关键字: {keyword}")

    capturer = GoogleSearchCapture(keyword, output)

    # 先截图
    click.echo("正在截图...")
    screenshot_path = asyncio.run(capturer.search_and_screenshot(wait))
    click.echo(f"✓ 截图已保存到: {screenshot_path}")

    # 再录影
    click.echo(f"正在录影 ({duration} 秒)...")
    video_path = asyncio.run(capturer.search_and_record(duration))
    click.echo(f"✓ 录影已保存到: {video_path}")


if __name__ == '__main__':
    cli()
