import wikipedia




def show_search_data(what_to_search):
    ny = wikipedia.search(str(what_to_search))
    return ny
    
def show_text_data(give_a_text_to_answear):
    text=wikipedia.summary(str(give_a_text_to_answear),sentences=2).encode("utf-8")
    if len(text)==None:
        return "Nothing found!"
    else:
        return text

##print(show_text_data("heart"))
