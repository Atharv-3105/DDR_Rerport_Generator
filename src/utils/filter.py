#Filter pages which have little text inorder to increase efficiency
def filter_pages(pages, min_text_length = 20):
    return [p for p in pages if len(p["text"]) > min_text_length]