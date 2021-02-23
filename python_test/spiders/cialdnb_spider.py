import scrapy
import python_test.utils.libregex as rust
from sys import stdin, stdout
from json import dumps as json_dumps


RE_PHONE: r'' = r"(((\d{1,4})|(\(\d{1,5}\)))(-| )((\d{1,5})|(\(\d{1,5}\)))(-| )(\d{1,5})(-\d{1,5}| \d{1,5}| )*.)</"
RE_LOGO: r'' = r'"((\S*)(/|-|_)(\w*)(.png|.svg|.jpeg|.jpg))"'


class cialdnbSpider(scrapy.Spider):
    name = "cialdnb"

    def start_requests(self) -> [{}]:
        urls: list = list(map(lambda x: x.replace('\n', ''), stdin.readlines()))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        _response: str = self.re_sub(response.text, pattern=r"<script..*</script>")
        yield self._stdout_write({
            "website": response.url,
            "logo": self._checkout_logo(base=response.url,
                                        path=self.re_findall(_response, pattern=RE_LOGO, group=1)[0]),
            "phone": list(set(map(lambda x: self.re_sub(x, pattern=r"\D*"),
                                  self.re_findall(_response, pattern=RE_PHONE, group=1))))
        })

    @staticmethod
    def _checkout_logo(base: str, path: str) -> str:
        return path if path.startswith("http") else \
            f"{'/'.join(base.split('/')[:3]) if base.count('/') > 2 else base}{path}"

    @staticmethod
    def _stdout_write(result: dict) -> dict:
        stdout.write(json_dumps(result)+'\n')
        stdout.flush()
        return result

    @staticmethod
    def re_sub(text: str, *, pattern: r'' = r'\r|\n', repl: str = '') -> str:
        """Regex rust: 4x mais rapido do que re.sub"""
        return rust.re_sub(text.strip(), pattern, repl)

    @staticmethod
    def re_findall(text: str, *, pattern: r'', group: int) -> list:
        """Regex rust: 4x mais rapido do que re.findall, e o paramentro 'group' é escolher o nivel do pattern"""
        return rust.re_findall(text, pattern, group)
