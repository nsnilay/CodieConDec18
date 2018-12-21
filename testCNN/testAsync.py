# import tornado.ioloop
# from tornado.httpclient import AsyncHTTPClient
#
# urls = ['http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org']
#
#
# def handle_response(response):
#     if response.error:
#         print("Error:", response.error)
#     else:
#         url = response.request.url
#         data = response.body
#         print(url)
#         # print('{}: {} bytes: {}'.format(url, len(data), data))
#
#
# http_client = AsyncHTTPClient()
# for url2 in urls:
#     http_client.fetch(url2, handle_response)
#
# tornado.ioloop.IOLoop.instance().start()
from concurrent.futures import ThreadPoolExecutor
import time


def task(n):
    print("Processing {}".format(n))
    time.sleep(2)


def main():
    print("Starting ThreadPoolExecutor")
    executor = ThreadPoolExecutor()
    executor.submit(task, (2))
    executor.submit(task, (3))

    # with ThreadPoolExecutor() as executor:
    #     future = executor.submit(task, (2))
    #     future = executor.submit(task, (3))
    print("All tasks complete")


if __name__ == '__main__':
    main()