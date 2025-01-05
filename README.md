# YTDownloaderServer

## Docker 執行
這個項目提供了一個簡單的 Docker 映像，允許你運行 `YTDownloaderServer` 服務。這個服務可以幫助你從 YouTube 下載影片。

## 預備條件

- 已安裝 [Docker](https://www.docker.com/get-started)
- 已經可以運行 Docker 命令

## 使用方式

### 1. 拉取 Docker 映像

首先，拉取最新的 Docker 映像：

```bash
docker pull ghcr.io/kenchou2006/ytdownloaderserver:latest
```

### 2. 啟動 Docker 容器

啟動容器並將容器內的 `8000` 端口映射到主機的 `8080` 端口。這樣，容器將在背景運行，並在 Docker 服務啟動時自動重啟：

```bash
docker run -d -p 8080:8000 --name ytdownloaderserver --restart unless-stopped --platform linux/amd64 ghcr.io/kenchou2006/ytdownloaderserver:latest
```

### 3. 訪問服務

啟動容器後，你可以通過以下 URL 訪問 `YTDownloaderServer` 服務：

- **Web 介面**: `http://127.0.0.1:8080`

### 4. 停止和刪除容器

如果你想停止並刪除正在運行的容器，可以使用以下命令：

```bash
docker stop ytdownloaderserver
docker rm ytdownloaderserver
```

### 5. 重啟容器

若要重啟容器，可以使用以下命令：

```bash
docker restart ytdownloaderserver
```

### 6. 查看容器日誌

你可以查看容器的運行日誌，以檢查服務的狀態或錯誤消息：

```bash
docker logs ytdownloaderserver
```

### 7. 容器自動重啟

容器設定為在 Docker 服務啟動或容器崩潰後自動重啟。這是通過 `--restart unless-stopped` 設置實現的。這意味著除非你手動停止容器，否則它將持續運行。