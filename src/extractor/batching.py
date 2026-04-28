#instead of calling LLM at each page, we will batch together pages and then call LLM for efficient response generation
def batch_pages(pages, batch_size = 3):
    for i in range(0, len(pages), batch_size):
        yield pages[i:i + batch_size]