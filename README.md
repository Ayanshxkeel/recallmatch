# RecallMatch

Find potentially relevant Canadian product recalls from a product description. RecallMatch searches the [Government of Canada Recalls and Safety Alerts open dataset](https://open.canada.ca/data/en/dataset/d38de914-c94c-429b-8ab1-8776c31643e3) and links each result to its official notice.

**Purpose:** Recall headlines do not always use the words someone would type. This app ranks notices for a person to inspect; it does not determine whether their exact item, model, or batch is recalled.

## Features

- Downloads the public recall CSV and refreshes the cached copy every 24 hours.
- Searches notice titles and product fields using word and two-word phrase matching.
- Shows ranked notices, update dates, text similarity scores, and source links.
- Gives a clear empty result when search terms do not match the dataset.

## Run locally

Requires Python 3 and internet access.

```bash
git clone https://github.com/Ayanshxkeel/recallmatch.git
cd recallmatch
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. On Windows, activate with `.venv\Scripts\activate`.

## Try it

Search `portable Bluetooth speaker`. Open a resulting official notice and check its exact product details. Then search a brand or model from that notice and see how the order changes. Search `xyzqnevermade` to see the no-match message.

## How it works

`load_recalls()` downloads and parses the CSV. `find_matches()` combines each notice's product and title, converts those texts and the query to **TF-IDF** vectors, and sorts notices by **cosine similarity**. The score is text similarity, not recall probability. See [How it works](HOW_IT_WORKS.md) for a code walkthrough.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface, data download, and ranking |
| `requirements.txt` | Python dependencies |
| `HOW_IT_WORKS.md` | Explanation and hands-on changes |

## Limits

A model number may be mentioned only inside the linked notice, beyond the title and product fields searched here. Synonyms and misspellings can be missed. **No result does not mean a product is safe.** The public source must be reachable when the app loads. No AI API key is required.
