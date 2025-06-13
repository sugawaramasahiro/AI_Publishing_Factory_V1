# README.md を作成／上書き
@"
# AI Publishing Factory V1

ローカルで **Streamlit + OpenAI** を使った電子書籍生成ダッシュボード。

## 起動方法
```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
set OPENAI_API_KEY=********          # PowerShell
streamlit run gui_dashboard.py
