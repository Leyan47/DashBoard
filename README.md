# KPI DashBoard

這是一個使用 Python Dash 框架建立的互動式儀表板專案。旨在展示如何將業務數據（如帶看次數、廣告成效等）可視化，並提供多維度的篩選功能，幫助使用者快速洞察趨勢。
為了保護隱私並方便分享，本專案使用的數據 (fakeData.xlsx) 均為經過假名化處理的虛構資料，其數值與趨勢不代表任何真實業務情況。

### 功能

- 多維度篩選：使用者可以根據「週日期區間」、「部門」、「店家」以及「數值指標」進行自由組合篩選。
- 連動式下拉選單：當使用者選擇「部門」後，「店家」選單會自動更新，只顯示該部門下的店家，提升操作體驗。
- 動態圖表生成：篩選條件變更後，折線圖會即時重新繪製，以疊圖方式呈現不同店家、不同指標的趨勢。
- 圖表下載：提供一鍵下載圖表為 HTML 檔案的功能，方便離線查看或分享。

### 儀表板預覽

點擊下方圖片即可訪問線上的互動式儀表板！(待添加)

[](https://your-dashboard.onrender.com)

### 安裝與設定
請依照以下步驟來設定並運行此專案。

1.複製專案

```
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

2.建立並啟動虛擬環境 (建議)
- macOS / Linux
```
python3 -m venv venv
source venv/bin/activate
```

- Windows
```
python -m venv venv
.\venv\Scripts\activate
```

安裝相依套件
使用 pip 並透過 requirements.txt 檔案安裝所有必要的套件。
`pip install -r requirements.txt`

### 運行
確認所有套件都已安裝完成後，在你的終端機中運行以下指令：
`python dashboard_op.py`

程式啟動後，你將會看到類似以下的訊息：
```Dash is running on http://127.0.0.1:8051/```

打開你的網頁瀏覽器並訪問 `http://127.0.0.1:8051`，即可看到儀表板。
