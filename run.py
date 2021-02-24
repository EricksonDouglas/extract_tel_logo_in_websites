import logging

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from python_test.spiders.cialdnb_spider import CialdnbSpider


def spider_results() -> list:
    logging.getLogger('scrapy').propagate = False
    results: list = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)
    _process = CrawlerProcess(get_project_settings())
    _process.crawl(CialdnbSpider)
    _process.start()
    return results


if __name__ == '__main__':
    from sys import stdout
    from json import dumps as json_dumps
    stdout.write(json_dumps(spider_results()) + '\n')
    stdout.flush()
