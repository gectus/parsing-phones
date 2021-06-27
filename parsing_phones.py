import aiohttp
import asyncio
import phonenumbers


class ParsingPhonesService:
    result = {}

    async def get_page(self, page: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(page) as response:
                self.parse_page(page, await response.text())

    def parse_page(self, page: str, html: str):
        """Парсим номера телефоном с помощью библиотеки phonenumbers"""

        phones = []
        numbers = phonenumbers.PhoneNumberMatcher(html, "RU")
        for match in numbers:
            phone = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            phone = phone.replace('+7', '8')
            phones.append(phone)

        self.result[page] = list(set(phones))

    def run(self, pages: list):
        """Обрабатываем страницы используя асинхронный HTTP-клиент"""
        loop = asyncio.get_event_loop()
        coroutines = [self.get_page(page) for page in pages]
        loop.run_until_complete(asyncio.gather(*coroutines))

        return self.result


def main():
    pages = [
        'https://masterdel.ru',
        'https://repetitors.info',
    ]

    service = ParsingPhonesService()
    result = service.run(pages)

    for page, phones in result.items():
        print('%s: %s' % (page, phones))


if __name__ == "__main__":
    main()
