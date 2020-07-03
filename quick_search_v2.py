# from time import perf_counter_ns
# from time import perf_counter
from bs4 import BeautifulSoup
import requests

# global start1
NUM_LINKS = 3


# def time_it(start, type, subject):
#     """
#     usage:
#     start = perf_counter() #  At beginning
#     time_it(start, seconds, function_name) #  At end
#     Helps me optimize code by timing it
#     :param start is the already declared 'start' of either perf_counter
#     :param type lets you choose between ns and s
#     :param subject is the subject you are timing
#     """
# if type == 'ns':
#     end = perf_counter_ns()
#     print(subject + " took {} nano seconds.".format(end - start), file=open('optimized_output.txt', 'a'))
# elif type == 's':
#     end = perf_counter()
#     print(subject + " took {} seconds.".format(round(end - start, 2)), file=open('optimized_output.txt', 'a'))


def get_search() -> str:
    """
    Gets the URL of a user given search
    :return: the URL of the search page
    """
    user_input = input("Learn: ")
    # global start1
    # start1 = perf_counter()
    user_input.replace(' ', '+')
    base = 'https://google.com/search?q='
    return base + user_input


def request(google_url) -> str:
    """
    gets the html of the web page as a string

    :param google_url: the URL of the google search page to scrape
    :return: the HTML of the page
    """
    # start = perf_counter()
    source = requests.get(google_url).text
    # time_it(start, 's', 'requests')
    return source


def brew(source) -> BeautifulSoup:
    """
    takes in a url and brews a tasty soup from it.

    :param source: HTML of the web page to scrape
    :return: some soup
    """
    # start = perf_counter()
    the_soup = BeautifulSoup(source, 'lxml')  # used to use html5lib, but lxml is apparently faster
    # time_it(start, 's', 'brew')
    return the_soup


def just_url(div_text) -> str:
    """
    Cuts everything before 'https://' and everything after the '&' (including the '&')
    :param
    str: div class without 'BNeawe'
    :return: Just the URL nothing else
    """
    # start = perf_counter()
    http_index = div_text.find('http')
    ampersand_index = div_text.find('&')
    # time_it(start, 's', 'just url')
    return div_text[http_index: ampersand_index]


def youtube_filter(link) -> str:
    """
    Filters out youtube links
    :param link: the questioned link
    :return: empty string if youtube link, unchanged link if not youtube
    """
    # if its a youtube 'watch link'
    if link.find('https://www.youtube.com/watch') != -1:
        return ''
    else:
        return link


def http_filter(text) -> str:
    """
    only lets through links
    :param text: questioned text
    :return: empty string if no 'http', unchanged if there is 'http'
    """
    if text.find('http') != -1:
        return text
    else:
        return ''


def apply_filters(text) -> str:
    """
    If the text passes through all filters it will be returned unscathed
    This function applies all filters, and it is where you can add more filters
    :param text: the text to be filtered
    :return: filtered text
    """
    # start = perf_counter()
    filtered_text = youtube_filter(http_filter(text))
    # time_it(start, 's', 'apply filters')
    return filtered_text


def append_no_blanks(a_list, text) -> bool:
    """
    Appends to list only if the item to append is not a blank character
    :param a_list: the list you want to append to
    :param text: the text to append as a new item
    :return bool: True if text was appended, false if nothing was done
    """
    if text != '':
        a_list.append(text)
        return True
    return False


def make_unique_list(a_soup, target_size) -> [str]:
    """
    Takes soup and makes it into a list with no blank space items.
    :param a_soup: The HTML given after making soup from source
    :param target_size: The desired size of the list
    :return: Unique list of URLs as strings
    """
    # The oddly named 'kCrYT' div class represents all the search results
    # start = perf_counter()
    articles = a_soup.find_all('div', class_='kCrYT')
    string_list = []
    # Only append <a>
    for link in articles:
        if link.a:
            string_list.append(str(link))
    # Filter out items with "BNeawe" from new list
    filtered_list = []
    count = 0
    # start = perf_counter()
    for string in string_list:
        if count == target_size:
            break
        # for if there is a 'BNeawe'
        if string.find('BNeawe') != -1:
            index = string.find('BNeawe')
            without_bneawe = string[0: index]
            # applying filters
            filtered_text = just_url(apply_filters(without_bneawe))
            if append_no_blanks(filtered_list, filtered_text):
                count += 1
        # for if there is not a 'BNeawe' (there seems to always be one, but just in case)
        else:
            filtered_text = apply_filters(just_url(string))
            if append_no_blanks(filtered_list, filtered_text):
                count += 1
    # print(string_list)
    # Better print for debugging
    # for string in string_list:
    #     print(string, end='\n')  # , file=open('optimized_output.txt', 'a'))  # "a" means append
    # for article in articles:
    # print(article, end='\n')  # , file=open('optimized_output.txt', 'a'))  # "a" means append
    # str(string_list.append(link.a.get('href')))
    # print(string_list)  # For debugging
    # print(link, end='\n')  # For debugging
    # time_it(start, 's', 'make unique list')
    return filtered_list


def print_list(a_list):
    """
    To print a list in a legible format for debugging
    :param a_list: any list
    """
    # start = perf_counter()
    for component in a_list:
        print(component, end='\n')  # , file=open('optimized_output.txt', 'a'))  # "a" means append
    # time_it(start, 's', 'printlist')


def main():
    search = get_search()
    print_list(make_unique_list(brew(request(search)), NUM_LINKS))
    # time_it(start1, 's', 'everything after input')
    # print(end='\n', file=open('optimized_output.txt', 'a'))
    # requests.get(url).text
    # url = get_search_url()
    # soup = brew(request(url))
    # url_list = make_unique_list(soup, 3)
    # print(url_list)
    # print_list(url_list)


# string = '<div class="kCrYT"><a data-uch="1" href="/url?q=https://www.merriam-webster.com/dictionary/dependency' \

#          '&amp;sa=U&amp;ved=2ahUKEwj7z53_nI7qAhVB-WEKHRnRB6MQFjAMegQIBxAB&amp;usg=AOvVaw3fPtJrFlWNdEjTlmWOnJ8J' \
#          '"><h3 class="zBAuLc"><div class=" '
# print(just_url(string))

if __name__ == '__main__':
    main()
