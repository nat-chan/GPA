import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash()
app.layout = html.Div([
    dcc.Markdown('''
## 成績いいかんじビューア（ITF生向け）
[plotly](https://plot.ly/python/) を用いて作られた，インタラクティブに動かせる成績グラフ作成ツールです．

**お約束** これはジョークプログラムです．使用によって生じた一切の不利益に対して責任を負いません．
### 使い方
- [twins](https://twins.tsukuba.ac.jp)に行き，下図に示すテキストをコピーしてください．
- 下のテキストエリアにペーストしてください．
- 直ちにグラフが更新されます．マウスオーバーで値を確認したり，パンしたりして遊んでください．
    '''.strip()),
    html.Img(
        src="https://i.imgur.com/ZbaXAei.png",
        style={'width': '100%'}
    ),
    dcc.Textarea(
        id='my-id',
        value= """
履修単位数	128.0	16.0	16.0	16.0	16.0	16.0	16.0	16.0	16.0
修得単位数	128.0	16.0	16.0	16.0	16.0	16.0	16.0	16.0	16.0
ＧＰＡ	4.0	4.0	4.0	4.0	4.0	4.0	4.0	4.0	4.0
        """.strip(),
        rows=4,
        style={'width': '100%'}
    ),
    dcc.Graph(id='my-graph'),
    html.Div(id='my-div')
])

def plot(credit, gpa):
    x = [
        ['2016']*2+['2017']*2+['2018']*2+['2019']*2,
        ['春学期', '秋学期']*4,
    ]
    trace1 = go.Bar(
        x=x,
        y=credit,
        name='単位（累計）',
        yaxis="y"
    )
    trace2 = go.Scatter(
        x=x,
        y=gpa,
        name='GPA（各学期）',
        yaxis='y2'
    )
    data = [trace1, trace2]
    layout = go.Layout(
        legend=dict(x=0.05, y=0.95),
        yaxis=dict(
            title='単位'
        ),
        yaxis2=dict(
            title='GPA',
            overlaying='y',
            side='right'
        )
    )
    return {'data':data, 'layout':layout}

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_figure(value):
    value = value.strip()
    for line in value.splitlines():
        if line.startswith("修得単位数"):
            credit = list(map(float,line.split("	")[1:]))
        elif line.startswith("ＧＰＡ"):
            gpa = list(map(float,line.split("	")[1:]))
    credit_overall = credit[0]; credit = credit[1:]
    gpa_overall    = gpa[0]   ; gpa    = gpa[1:]
    gpa.reverse()
    credit.reverse()
    credit = [sum(credit[:(i+1)]) for i in range(len(credit))]
    return plot(credit, gpa)

if __name__ == '__main__':
    app.run_server()
