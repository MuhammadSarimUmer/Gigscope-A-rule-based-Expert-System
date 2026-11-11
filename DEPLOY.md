# Deploy GigScope on Streamlit Community Cloud

## 1. Create a public GitHub repository

Push the `gigscope/` folder contents (or the whole repo with `app.py` at repo root or in `gigscope/`).

## 2. Check files

- `app.py` (entry point)
- `requirements.txt`
- `packages.txt` with line `graphviz`
- `.streamlit/config.toml`
- Pre-generated `assets/` (DOT files; PNG/SVG optional but recommended)

## 3. Connect Streamlit Cloud

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. **New app** → pick your repo and branch
4. Main file path: `gigscope/app.py` (or `app.py` if you moved it to root)
5. Deploy

## 4. Confirm public access

Open the app URL in an **incognito** window. Free apps sleep — open it shortly before your viva.

## 5. Regenerate tree images (optional)

On a machine with Graphviz installed:

```bash
cd gigscope
pip install -r requirements.txt
python export_assets.py
git add assets/
git commit -m "Regenerate tree assets"
git push
```

## Troubleshooting

| Issue | Fix |
|---|---|
| `Graphviz not found` | Ensure `packages.txt` includes `graphviz`; redeploy; or rely on `st.graphviz_chart` + DOT download in app |
| Module not found | Check `requirements.txt` and app path |
| App memory limit | Pre-commit PNGs in `assets/`; avoid rendering full KB in session |
| Old code showing | Clear cache in Streamlit Cloud → Reboot app |
