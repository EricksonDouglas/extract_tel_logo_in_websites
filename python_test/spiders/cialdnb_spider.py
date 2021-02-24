from scrapy import Spider, Request
import python_test.utils.libregex as rust
from sys import stdin


RE_PHONE: r'' = r"(((\d{1,4})|(\(\d{1,5}\)))(-| )((\d{1,5})|(\(\d{1,5}\)))(-| )(\d{1,5})(-\d{1,5}| \d{1,5}| )*.)</"
RE_LOGO: r'' = r'"((\S*)(/|-|_)(\w*)(.png|.svg|.jpeg|.jpg))"'


class CialdnbSpider(Spider):
    name = "cialdnb"

    def start_requests(self) -> [{}]:
        urls: list = list(map(lambda x: x.replace('\n', ''), stdin.readlines()))
        for url in urls:
            yield Request(url=url, callback=self.parse,
                          headers={'Cache-Control': 'no-cache',
                                   "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like'
                                                 ' Gecko) Chrome/74.0.3729.169 Safari/537.36'})

    def parse(self, response):
        _response: str = self.re_sub(response.text, pattern=r"<script..*</script>")
        yield {
            "website": response.url,
            "logo": self._checkout_logo(base=response.url,
                                        path=self.re_findall(_response, pattern=RE_LOGO, group=1)[0]),
            "phone": list(set(map(lambda x: self.re_sub(x, pattern=r"\D*"),
                                  self.re_findall(_response, pattern=RE_PHONE, group=1))))
        }

    @staticmethod
    def _checkout_logo(base: str, path: str) -> str:
        return path if path.startswith("http") else \
            f"{'/'.join(base.split('/')[:3]) if base.count('/') > 2 else base}{path}"

    @staticmethod
    def re_sub(text: str, *, pattern: r'' = r'\r|\n', repl: str = '') -> str:
        """Regex rust: 4x mais rapido do que re.sub"""
        return rust.re_sub(text.strip(), pattern, repl)

    @staticmethod
    def re_findall(text: str, *, pattern: r'', group: int) -> list:
        """Regex rust: 4x mais rapido do que re.findall, e o paramentro 'group' é escolher o nivel do pattern"""
        return rust.re_findall(text, pattern, group)
