/**
 * static/js/main.js
 * 負責處理倒數計時、影像更新、雙螢幕切換與後端 API 溝通
 */

// 全域狀態變數
let isCountingDown = false; // 是否正在倒數中
let timer = 15;             // 倒數秒數

/**
 * 核心循環：每 100ms 向後端請求最新狀態
 * 負責更新：即時分數、左側 Live 影像
 */
setInterval(function() {
    // 發送請求給 Flask 後端
    fetch('/get_status')
    .then(response => response.json())
    .then(data => {
        // 1. 更新分數顯示 (更新左邊的即時評分)
        const scoreEl = document.getElementById('score-val');
        if (scoreEl) {
            let scoreNum = Number(data.score);
            scoreEl.innerText = scoreNum.toFixed(2);
        }
        
        // 2. 更新左側 Live Stream 影像
        // 只有當後端有傳來有效的圖片資料時才更新
        if (data.image && data.image.length > 100) {
            let liveImg = document.getElementById('live-image');
            let waitingText = document.getElementById('waiting-text');
            
            // 設定 Base64 圖片來源
            liveImg.src = "data:image/jpeg;base64," + data.image;
            liveImg.style.display = "block"; // 確保圖片顯示
            
            // 隱藏「等待訊號中...」的文字 (如果有)
            if (waitingText) waitingText.style.display = "none";
        }
    })
    .catch(err => console.error("Error fetching status:", err));
}, 100); // 頻率：100毫秒 (每秒 10 張)

/**
 * 啟動倒數計時功能
 * 當使用者按下「開始 15秒倒數」按鈕時觸發
 */
function startCountdown() {
    if (isCountingDown) return; // 避免重複點擊
    
    // 重置狀態
    isCountingDown = true;
    timer = 15;
    
    // 取得 DOM 元素
    const btnStart = document.getElementById('btn-start');
    const adviceContent = document.getElementById('advice-content');
    const overlay = document.getElementById('countdown-overlay');

    // 重置右邊的分數顯示為 "..."
    document.getElementById('snapshot-score-val').innerText = "--";

    // 更新 UI 狀態
    btnStart.disabled = true; // 鎖定按鈕
    btnStart.innerText = "倒數中...";
    adviceContent.innerText = "👀 調整姿勢中...請看著畫面修正！"; // 提示使用者
    
    // 顯示倒數遮罩 (Overlay)
    overlay.style.display = "flex";
    overlay.innerText = timer;

    // 啟動計時器 (每秒扣 1)
    let interval = setInterval(() => {
        timer--;
        overlay.innerText = timer;
        
        // 倒數結束
        if (timer <= 0) {
            clearInterval(interval);
            finishCountdown();
        }
    }, 1000);
}

/**
 * 倒數結束處理函式
 * 負責：定格畫面、定格分數、觸發 AI 分析、更新按鈕狀態
 */
function finishCountdown() {
    isCountingDown = false;
    
    // 1. 隱藏倒數遮罩
    document.getElementById('countdown-overlay').style.display = "none";
    
    // 2. 更新按鈕狀態
    document.getElementById('btn-start').innerText = "🤔 分析中...";
    document.getElementById('advice-content').innerHTML = "<span class='loading'>🔄 正在分析你的定格動作，請稍候...</span>";

    // 3. 【關鍵功能】畫面定格 (Snapshot)
    // 將左邊 Live 螢幕當下的畫面，複製到右邊 Snapshot 螢幕
    let liveImg = document.getElementById('live-image');
    let snapImg = document.getElementById('snapshot-image');
    
    if (liveImg.src && liveImg.src.startsWith('data:image')) {
        snapImg.src = liveImg.src; // 瞬間複製圖片
    }

    // 4. 【關鍵功能】分數定格
    // 抓取當下的即時分數，填入右邊，這樣就不會再變動了
    let currentScore = document.getElementById('score-val').innerText;
    document.getElementById('snapshot-score-val').innerText = currentScore;

    // 5. 呼叫後端 API 觸發 Gemini 分析
    fetch('/trigger_analysis', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        // 6. 顯示 AI 建議結果
        // 這裡會將後端回傳的 Markdown 或文字直接填入建議框
        document.getElementById('advice-content').innerText = data.advice;
        
        // 7. 恢復按鈕功能，允許下一次拍攝
        const btnStart = document.getElementById('btn-start');
        btnStart.innerText = "📸 再拍一次";
        btnStart.disabled = false;
    })
    .catch(err => {
        console.error("Analysis failed:", err);
        document.getElementById('advice-content').innerText = "⚠️ 分析失敗，請檢查網路連線。";
        document.getElementById('btn-start').disabled = false;
    });
}