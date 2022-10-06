from urlextract import URLExtract


def extractURLS(url) :
    extractor = URLExtract()
    return extractor.find_urls(str(url))
