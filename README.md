# [cite_start]居家健美教練 (AI Bodybuilding Coach) [cite: 1, 2]

## [cite_start]專案背景與動機 [cite: 5]
在傳統健美訓練與備賽過程中，選手與健身愛好者常面臨以下痛點：
* [cite_start]**教練成本高昂**：聘請專業健美教練調整 Posing 的費用極高，且無法隨時在側。 [cite: 7]
* [cite_start]**缺乏量化標準**：傳統自我訓練缺乏客觀數據（角度、對稱性），僅憑感覺容易練偏。 [cite: 10]
* [cite_start]**姿勢盲點**：健美運動極度強調「定格動作 (Posing)」，但自己照鏡子難以觀察背部或側面細節。 [cite: 11, 12]
* [cite_start]**市場缺口**：市面上有許多居家健身相關產品，多數為「健身」產品，沒有針對「健美備賽」與「Posing 矯正」這塊市場去做開發。 [cite: 24, 25, 26]

---

## [cite_start]解決方案與系統特色 [cite: 14]
[cite_start]本專案結合 EDGE AI（邊緣運算）的即時性與 GENERATIVE AI（生成式 AI）的分析能力，打造一個「24小時待命的 AI 數位教練」。 [cite: 15]

* [cite_start]**即時引導**：透過 Kneo Pi 進行骨架偵測與評分。 [cite: 16, 17]
* [cite_start]**視覺化反饋**：雙螢幕儀表板，同時呈現 Live 影像與定格分析。 [cite: 20]
* [cite_start]**AI 教練級建議**：整合 Google Gemini，根據分數與身體數值（身高/體重/年紀）給出個人化指導。 [cite: 21]

---

## [cite_start]系統架構 [cite: 29]
系統主要分為以下三個核心部分：

1. [cite_start]**Edge Device (Kneo Pi)** [cite: 33]
   * [cite_start]接收 USB Webcam 的 Video Stream。 [cite: 31, 32]
   * [cite_start]負責執行 HRNet 模型。 [cite: 44]
   * [cite_start]透過 HTTP POST (JSON-Img) 將資料回傳至伺服器。 [cite: 42]
2. [cite_start]**Application Server (Laptop)** [cite: 38]
   * [cite_start]運行 Flask App (`app.py`)。 [cite: 39]
   * [cite_start]管理 User Profile、State Manager 與 Pose Library。 [cite: 38, 40, 41]
   * [cite_start]負責 Render / SSE 給前端 (Browser) 顯示 Dashboard UI 與 Dual Monitor。 [cite: 53, 55, 56, 57]
3. [cite_start]**Cloud Service** [cite: 48]
   * [cite_start]透過 Prompt 呼叫 Google Gemini API (Generative AI) 並獲取 Advice。 [cite: 49, 50, 51, 52]

---

## [cite_start]核心演算法流程 [cite: 60]

1. [cite_start]**特徵提取**：HRNet 從影像中提取 17 個身體關鍵點 (Keypoints)。 [cite: 61, 62, 63]
2. [cite_start]**信心過濾**：剔除 confidence < 0.2 的低信賴點，防止雜訊干擾評分。 [cite: 64, 65]
3. [cite_start]**規則映射**：根據選擇的動作（如 Front Lat Spread），從 `pose_rules.py` 載入對應的向量權重。 [cite: 66, 67]
   * [cite_start]*範例 (正面擴背肌)*：上臂展開 (Shoulder → Elbow): *3、手部固定 (Elbow → Wrist): *3、肩膀水平 (L_Shoulder → R_Shoulder): *3、下肢站姿 (Hip → Knee): *1.5。 [cite: 68, 69, 70, 71, 72]
4. [cite_start]**相似度計算**：捨棄易受身高影響的「歐幾里得距離 (Euclidean Distance)」，改使用餘弦相似度 (Cosine Similarity) 計算使用者向量與標準向量的夾角。 [cite: 73, 74]
5. [cite_start]**AI 講評生成**：倒數計時結束後觸發，將 Score、Pose Name、User Profile 與 Prompt Template 輸入給 Gemini，生成簡明扼要、具備教練語氣的繁體中文建議。 [cite: 75, 76, 77, 78, 79, 80]

---

## [cite_start]軟體模組設計 [cite: 82]

### [cite_start]Client Side (Kneo Pi) [cite: 83]
* [cite_start]**`client_pose_stream.py`** (感知層 - 模型推理)：作為軟體與 KL730 AI 晶片間的驅動介面。負責載入高精度的 HRNet 模型、處理影像前後處理，並輸出 17 個關鍵點。同時負責影像串流與 HTTP POST。 [cite: 84, 87, 89, 92, 93, 94, 95]
* [cite_start]**`pose_rules.py`**：核心資產，數位化的健美規則書（七個動作）。 [cite: 85, 90]
* **`compare_pose.py`** (認知層 - 邏輯運算)：系統的「數學大腦」。負責執行「餘弦相似度演算法」、動態載入規則、信心過濾與加權評分。 [cite: 86, 88, 91, 96, 97, 98]

### [cite_start]Server Side (Laptop) [cite: 100]
* [cite_start]**`app.py`**：控制中心，負責路由處理。 [cite: 101, 104]
* **`services/ai_coach.py`**：封裝 GEMINI API 呼叫邏輯。 [cite: 102, 105]
* **`services/pose_library.py`**：管理動作教學影片與 PROMPT。 [cite: 103, 106]

---

## [cite_start]未來展望 [cite: 108]
* [cite_start]**趨勢分析**：記錄使用者長期的分數變化，繪製進步曲線。 [cite: 109]
* **整合智慧飲食追蹤**：使用者可透過文字或「拍照」上傳飲食紀錄，利用 GEMINI 的多模態能力自動計算熱量與營養素。 [cite: 110]
