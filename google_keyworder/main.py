import asyncio
import time
from datetime import datetime
from pathlib import Path

import click
from playwright.async_api import async_playwright


class GoogleSearchCapture:
    """Google 搜尋截圖和錄影類別"""

    def __init__(self, keyword: str, output_dir: str = "output"):
        self.keyword = keyword
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_filename(self, extension: str) -> Path:
        """產生輸出檔案名稱"""
        safe_keyword = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in self.keyword)
        safe_keyword = safe_keyword.replace(' ', '_')[:50]
        return self.output_dir / f"{safe_keyword}_{self.timestamp}.{extension}"

    async def _smooth_scroll(self, page) -> None:
        """平滑滾動頁面以載入所有內容"""
        # 取得頁面總高度
        scroll_height = await page.evaluate("document.body.scrollHeight")
        viewport_height = await page.evaluate("window.innerHeight")

        # 計算需要滾動的次數
        current_position = 0
        scroll_step = viewport_height * 0.5  # 每次滾動 50% 的視窗高度(減少步進距離)

        while current_position < scroll_height:
            # 滾動到下一個位置
            current_position += scroll_step
            await page.evaluate(f"window.scrollTo({{top: {current_position}, behavior: 'smooth'}})")

            # 等待更久讓內容載入和動畫完成
            await asyncio.sleep(1.5)

            # 更新總高度(因為可能有動態載入的內容)
            new_scroll_height = await page.evaluate("document.body.scrollHeight")
            if new_scroll_height > scroll_height:
                scroll_height = new_scroll_height

        # 滾動回頂部
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(1)

    async def search_and_screenshot(self, wait_time: int = 10) -> Path:
        """執行 Google 搜尋並截圖

        Args:
            wait_time: 等待頁面載入的時間(秒)

        Returns:
            截圖檔案路徑
        """
        screenshot_path = self._get_filename("png")

        async with async_playwright() as p:
            # 使用更真實的瀏覽器設定
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )

            # 設定 context 以模擬真實瀏覽器
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            page = await context.new_page()

            # 隱藏 webdriver 特徵
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # 訪問 Google 搜尋
            search_url = f"https://www.google.com/search?q={self.keyword}"
            await page.goto(search_url, wait_until='networkidle')

            # 檢查是否有 CAPTCHA
            captcha_exists = await page.locator('iframe[src*="recaptcha"]').count() > 0
            if captcha_exists:
                click.echo("⚠️  偵測到 CAPTCHA 驗證，請手動完成驗證...")
                click.echo(f"等待 {wait_time} 秒供您完成驗證...")

            # 等待頁面載入
            await asyncio.sleep(2)

            # 自動向下滾動以載入所有內容
            click.echo("正在滾動頁面載入完整內容...")
            await self._smooth_scroll(page)

            # 額外等待確保內容完全載入
            await asyncio.sleep(wait_time)

            # 截圖
            await page.screenshot(path=str(screenshot_path), full_page=True)

            await context.close()
            await browser.close()

        return screenshot_path

    async def search_and_record(self, duration: int = 10) -> Path:
        """執行 Google 搜尋並錄影

        Args:
            duration: 錄影時長(秒)

        Returns:
            錄影檔案路徑
        """
        video_path = self._get_filename("webm")

        async with async_playwright() as p:
            # 使用更真實的瀏覽器設定
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )

            context = await browser.new_context(
                record_video_dir=str(self.output_dir),
                record_video_size={"width": 1920, "height": 1080},
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            page = await context.new_page()

            # 隱藏 webdriver 特徵
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # 訪問 Google 搜尋
            search_url = f"https://www.google.com/search?q={self.keyword}"
            await page.goto(search_url, wait_until='networkidle')

            # 檢查是否有 CAPTCHA
            captcha_exists = await page.locator('iframe[src*="recaptcha"]').count() > 0
            if captcha_exists:
                click.echo("⚠️  偵測到 CAPTCHA 驗證,請手動完成驗證...")
                click.echo(f"錄影將持續 {duration} 秒...")

            # 等待頁面初始載入
            await asyncio.sleep(2)

            # 自動向下滾動
            click.echo("正在滾動頁面...")
            await self._smooth_scroll(page)

            # 繼續等待剩餘時間
            remaining_time = max(0, duration - 4)  # 減去已使用的時間
            await asyncio.sleep(remaining_time)

            # 關閉頁面和上下文以儲存影片
            await page.close()
            await context.close()
            await browser.close()

            # 取得產生的影片檔案
            video_files = list(self.output_dir.glob("*.webm"))
            if video_files:
                # 重新命名為我們想要的檔案名稱
                latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                latest_video.rename(video_path)

        return video_path


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Google 關鍵字搜尋截圖和錄影工具

    支援將輸入的關鍵字透過 Google 引擎搜尋並截圖結果，或使用錄影儲存過程。
    """
    pass


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', default='output', help='輸出目錄（預設: output）')
@click.option('--wait', '-w', default=3, help='等待頁面載入時間（秒，預設: 3）')
def screenshot(keyword: str, output: str, wait: int):
    """對 Google 搜尋結果進行截圖

    範例:
        google-keyworder screenshot "Python 教學"
        google-keyworder screenshot "機器學習" -o screenshots -w 5
    """
    click.echo(f"正在搜尋關鍵字: {keyword}")

    capturer = GoogleSearchCapture(keyword, output)
    result_path = asyncio.run(capturer.search_and_screenshot(wait))

    click.echo(f"✓ 截圖已儲存到: {result_path}")


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', default='output', help='輸出目錄（預設: output）')
@click.option('--duration', '-d', default=10, help='錄影時長（秒，預設: 10）')
def record(keyword: str, output: str, duration: int):
    """對 Google 搜尋過程進行錄影

    範例:
        google-keyworder record "Python 教學"
        google-keyworder record "機器學習" -o videos -d 15
    """
    click.echo(f"正在搜尋關鍵字: {keyword}")
    click.echo(f"錄影時長: {duration} 秒")

    capturer = GoogleSearchCapture(keyword, output)
    result_path = asyncio.run(capturer.search_and_record(duration))

    click.echo(f"✓ 錄影已儲存到: {result_path}")


@cli.command()
@click.argument('keyword')
@click.option('--output', '-o', default='output', help='輸出目錄（預設: output）')
@click.option('--wait', '-w', default=3, help='截圖等待時間（秒，預設: 3）')
@click.option('--duration', '-d', default=10, help='錄影時長（秒，預設: 10）')
def both(keyword: str, output: str, wait: int, duration: int):
    """同時進行截圖和錄影

    範例:
        google-keyworder both "Python 教學"
        google-keyworder both "機器學習" -o results -w 5 -d 15
    """
    click.echo(f"正在搜尋關鍵字: {keyword}")

    capturer = GoogleSearchCapture(keyword, output)

    # 先截圖
    click.echo("正在截圖...")
    screenshot_path = asyncio.run(capturer.search_and_screenshot(wait))
    click.echo(f"✓ 截圖已儲存到: {screenshot_path}")

    # 再錄影
    click.echo(f"正在錄影 ({duration} 秒)...")
    video_path = asyncio.run(capturer.search_and_record(duration))
    click.echo(f"✓ 錄影已儲存到: {video_path}")


if __name__ == '__main__':
    cli()
