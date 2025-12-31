# Google Keyworder

Google 關鍵字搜尋截圖和錄影工具，可以將輸入的關鍵字透過 Google 引擎搜尋並截圖結果，或使用錄影儲存過程。

## 功能特性

- 🔍 自動執行 Google 關鍵字搜尋
- 📸 對搜尋結果進行全頁截圖
- 🎥 錄製搜尋過程影片
- 🚀 使用 uv 作為套件管理工具
- 💻 簡單的命令列介面

## 系統要求

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) 套件管理工具

## 安裝

### 1. 安裝 uv（如果尚未安裝）

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 複製專案

```bash
git clone <repository-url>
cd GoogleKeyworder
```

### 3. 使用 uv 安裝相依套件

```bash
# 同步相依套件
uv sync

# 安裝 Playwright 瀏覽器
uv run playwright install chromium
```

## 使用方法

### 截圖模式

對 Google 搜尋結果進行截圖：

```bash
# 基本使用
uv run google-keyworder screenshot "Python 教學"

# 指定輸出目錄和等待時間
uv run google-keyworder screenshot "機器學習" -o screenshots -w 5
```

參數說明：
- `keyword`: 搜尋關鍵字（必需）
- `-o, --output`: 輸出目錄（預設: output）
- `-w, --wait`: 等待頁面載入時間，單位秒（預設: 3）

### 錄影模式

對 Google 搜尋過程進行錄影：

```bash
# 基本使用
uv run google-keyworder record "Python 教學"

# 指定輸出目錄和錄影時長
uv run google-keyworder record "機器學習" -o videos -d 15
```

參數說明：
- `keyword`: 搜尋關鍵字（必需）
- `-o, --output`: 輸出目錄（預設: output）
- `-d, --duration`: 錄影時長，單位秒（預設: 10）

### 同時截圖和錄影

```bash
# 基本使用
uv run google-keyworder both "Python 教學"

# 完整參數
uv run google-keyworder both "機器學習" -o results -w 5 -d 15
```

參數說明：
- `keyword`: 搜尋關鍵字（必需）
- `-o, --output`: 輸出目錄（預設: output）
- `-w, --wait`: 截圖等待時間，單位秒（預設: 3）
- `-d, --duration`: 錄影時長，單位秒（預設: 10）

## 輸出檔案

### 檔案命名規則

輸出檔案會自動根據關鍵字和時間戳記命名：

```
<關鍵字>_<時間戳記>.<副檔名>
```

範例：
- `Python_教學_20250131_143022.png`（截圖）
- `機器學習_20250131_143022.webm`（錄影）

### 輸出格式

- **截圖**: PNG 格式，全頁截圖
- **錄影**: WebM 格式，1920x1080 解析度

## 專案結構

```
GoogleKeyworder/
├── google_keyworder/
│   ├── __init__.py       # 套件初始化檔案
│   └── main.py           # 主程式
├── pyproject.toml        # 專案配置（uv 管理）
├── README.md             # 說明文件
└── output/               # 預設輸出目錄（自動建立）
```

## 技術棧

- **套件管理**: [uv](https://github.com/astral-sh/uv) - 快速的 Python 套件管理工具
- **瀏覽器自動化**: [Playwright](https://playwright.dev/) - 現代化的瀏覽器自動化工具
- **命令列介面**: [Click](https://click.palletsprojects.com/) - Python 命令列框架

## 開發

### 執行測試

```bash
uv run pytest
```

### 新增相依套件

```bash
uv add <package-name>
```

### 更新相依套件

```bash
uv sync --upgrade
```

## 常見問題

### Q: 為什麼需要安裝 Playwright 瀏覽器？

A: Playwright 需要下載瀏覽器二進制檔案才能執行。使用 `uv run playwright install chromium` 命令安裝。

### Q: 可以自訂瀏覽器視窗大小嗎？

A: 可以。在 `main.py` 的 `search_and_record` 方法中修改 `record_video_size` 參數。

### Q: 支援其他搜尋引擎嗎？

A: 目前僅支援 Google。如需支援其他搜尋引擎，可以修改 `main.py` 中的 `search_url`。

## 授權條款

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！
