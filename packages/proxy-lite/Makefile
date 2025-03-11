.PHONY: proxy

proxy:
	uv pip install uv
	uv venv --python 3.12 --python-preference managed
	uv sync
	uv pip install -e .
	playwright install

app:
	streamlit run src/proxy_lite/app.py
