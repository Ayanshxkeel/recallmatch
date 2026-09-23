# RecallMatch

Search Canadian product recall notices by product description. The app downloads Health Canada's public recall CSV, represents the notice titles and products with TF-IDF word and two-word phrases, and ranks them by cosine similarity to your query.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Try `portable Bluetooth speaker` or a product and brand from a recent official notice. Open the linked notice to confirm the exact model or batch. A low score or no result **does not mean a product is safe**. The dataset is cached for 24 hours. This is text matching, not a safety classifier.

Data: [Government of Canada recalls and safety alerts](https://open.canada.ca/data/en/dataset/d38de914-c94c-429b-8ab1-8776c31643e3).

## Learn the code

See [How it works](HOW_IT_WORKS.md) for the data flow, hands-on checks, limitations, and ideas for your own changes.
