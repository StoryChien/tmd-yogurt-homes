# 天母的優格｜精選待售案件

靜態銷售網站，給批踢踢售屋文當「照片連結」用。

- 首頁：https://storychien.github.io/tmd-yogurt-homes/
- 健安新城（首發，批踢踢用這個）：https://storychien.github.io/tmd-yogurt-homes/jianan/

## 加入新案件

1. 在 `listings/` 新增一份 JSON，檔名用網址代稱，例如 `listings/tianmu-xx.json`，可先複製 `listings/jianan.json`
2. 把照片放到 `assets/img/<代稱>/`，主視覺檔名寫進 JSON 的 `hero`
3. 在專案根目錄執行：

```bash
python3 build.py
```

4. 把更新推上 GitHub 的 `main` 分支，GitHub Pages 會自動更新

JSON 必填欄位：`slug`（要跟資料夾和檔名一致）、`name`、`price`、`priceNum`、`priceUnit`、`hero`、`photos`、`specs`。`video` 可先留空。

## 填入影片連結

打開該案的 JSON，例如 `listings/jianan.json`，把 `video` 從空字串改成網址：

```json
"video": "https://www.youtube.com/watch?v=xxxxxxxxxxx"
```

或 IG Reels：

```json
"video": "https://www.instagram.com/reel/xxxxxxxxxxx/"
```

然後再跑一次 `python3 build.py` 並推上 GitHub。頁面瀏覽時也會讀取 `listings/` 裡的 JSON，所以只改 JSON 再推上，影片也會出現。沒填的時候，影片區會顯示「影片即將上線」。

## 本地預覽

```bash
python3 -m http.server 8080
```

打開 http://127.0.0.1:8080/
