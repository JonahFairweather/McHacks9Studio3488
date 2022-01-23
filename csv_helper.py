
def add_to_txt(response):
    fobj = open("responses.txt", "w")
    fobj.write(response)
    fobj.close()


def read_txt():
    response = ""
    fobj = open("responses.txt", "r")
    for line in fobj:
        response += line
    fobj.close()
    return response
