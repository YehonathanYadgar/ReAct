import wikipediaapi

wiki = wikipediaapi.Wikipedia('MyProjectName (jonyyadgar@gmail.com)', 'en')

def useWikipedia(x):
    page = wiki.page(x)
    page = page.text
    return page[:1000]


