import pandas as pd
import pyodbc
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
from urllib import parse
import openpyxl

df = pd.read_excel('fakeDate.xlsx')

# 取得所有可選的週日期區間字串（作為 Dropdown 選項）
date_ranges = sorted(df['週日期區間'].unique())
numeric_cols = ['帶看組數', '紅燈帶看', '非紅燈帶看',
                '龍騰_開價', '龍騰_ad', '龍騰_買方預算上限']

app = Dash(__name__)

# --- App 佈局 (Layout) ---
app.layout = html.Div([
    dcc.Dropdown(
        id='daterange-dropdown',
        options=[{'label': dr, 'value': dr} for dr in date_ranges],
        multi=True, placeholder="選擇週日期區間"
    ),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in numeric_cols],
        value=[numeric_cols[0]],
        multi=True, placeholder="選擇要繪製的數值欄位"
    ),
    dcc.Dropdown(
        id='department-dropdown',
        options=[{'label': d, 'value': d} for d in sorted(df['部'].unique())],
        multi=True, placeholder="選擇部門"
    ),
    dcc.Dropdown(
        id='store-dropdown',
        # options=[{'label': s, 'value': s} for s in sorted(df['店'].unique())], # <--- 舊的寫法，我們將移除它
        options=[],  # <--- 初始選項為空，將由下面的 callback 動態生成
        multi=True, placeholder="選擇店家 (請先選擇部門)"
    ),
    dcc.Graph(id='line-graph'),
    html.A(
        "下載圖表 HTML",
        id="download-link",
        download="chart.html",
        href="",
        target="_blank"
    )
])

# --- 新增的 Callback：連動部門和店家下拉選單 ---
@app.callback(
    Output('store-dropdown', 'options'), # 輸出1: 更新店家的選項
    Output('store-dropdown', 'value'),   # 輸出2: 清空已選的店家
    Input('department-dropdown', 'value') # 輸入: 監聽部門的選擇
)
def set_store_options(selected_departments):
    """
    當部門選單變動時，此函式會被觸發，
    以更新店家選單的選項並清空其值。
    """
    # 如果沒有選擇任何部門，則顯示所有店家
    if not selected_departments:
        all_stores = sorted(df['店'].unique())
        options = [{'label': s, 'value': s} for s in all_stores]
        # 回傳所有店家的選項，並清空已選店家
        return options, []

    # 如果選擇了部門，則只顯示屬於這些部門的店家
    filtered_df = df[df['部'].isin(selected_departments)]
    available_stores = sorted(filtered_df['店'].unique())
    options = [{'label': s, 'value': s} for s in available_stores]
    
    # 回傳篩選後的店家選項，並清空已選店家
    return options, []


# --- 更新圖表  ---
@app.callback(
    Output('line-graph', 'figure'),
    Input('daterange-dropdown', 'value'),
    Input('column-dropdown', 'value'),
    Input('department-dropdown', 'value'),
    Input('store-dropdown', 'value'),
)
def update_line_chart(selected_ranges, selected_cols, depts, stores):
    dff = df.copy()
    if selected_ranges:
        dff = dff[dff['週日期區間'].isin(selected_ranges)]
    if depts:
        dff = dff[dff['部'].isin(depts)]
    if stores:
        dff = dff[dff['店'].isin(stores)]

    fig = go.Figure()

    # 處理未選擇店家時的情況
    store_list = stores if stores else dff['店'].unique()
    
    # 處理未選擇欄位時的情況
    cols_to_plot = selected_cols if selected_cols else []

    for store in store_list:
        df_store = dff[dff['店'] == store]
        for col in cols_to_plot:
            fig.add_trace(go.Scatter(
                x=df_store['週日期區間'],
                y=df_store[col],
                mode='lines+markers',
                name=f"{store} - {col}"
            ))

    fig.update_layout(
        title="店別 x 指標 疊圖",
        xaxis_title="週日期區間",
        yaxis_title="數值",
        legend_title="店 - 指標",
        hovermode='x unified'
    )
    return fig

# --- 更新下載連結 ---
@app.callback(
    Output("download-link", "href"),
    Input("line-graph", "figure")
)
def update_download_link(figure):
    fig = go.Figure(figure)
    html_str = fig.to_html(full_html=True, include_plotlyjs='cdn')
    data_uri = "data:text/html;charset=utf-8," + parse.quote(html_str)
    return data_uri

# --- 啟動伺服器 ---
if __name__ == '__main__':
    app.run(debug=True, port=8051)
