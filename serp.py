from serpapi import GoogleSearch

params = {
  "engine": "google_maps",
  "q": "gift shops",
  "ll": "@19.9940148,73.804693,16z",
  "api_key": "ae8bad07321c4f18db972fe4d3fad8806c65bac32ffb2acd63dd6a27c8fe9f92"
}

search = GoogleSearch(params)
results = search.get_dict()
print(results)