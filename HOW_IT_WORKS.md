# Understand and extend RecallMatch

## The problem
A product description may be worded differently from a recall headline. RecallMatch helps find notices to inspect; it cannot decide whether your exact product is recalled.

## Code path
1. `load_recalls()` downloads the Government of Canada CSV and keeps rows with a title and URL. Streamlit caches it for a day.
2. `find_matches()` joins each notice's product and title into searchable text.
3. `TfidfVectorizer` turns words and two-word phrases into numbers. Common English words have little value; rarer product terms matter more.
4. `cosine_similarity` measures how close your query is to each notice. The largest scores appear first with links to the source.

## Try it yourself
Search `portable Bluetooth speaker`, then a brand or model from one of the returned notices. Compare how the order changes. Search gibberish such as `xyzqnevermade` and confirm the app makes no safety claim.

## A useful change you could make
Add a category filter and show which exact words were shared by the query and a notice. Explain the result to someone else before you put the project on a resume.

## Interview questions
Why TF-IDF instead of exact search? It handles related wording and ranks multiple candidates. Why is the score not a probability? It is a geometric similarity between text vectors. What are its limits? Synonyms, misspellings, and recall details outside the headline can be missed.
