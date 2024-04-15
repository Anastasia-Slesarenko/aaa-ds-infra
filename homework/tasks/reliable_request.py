import abc

import httpx


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(
    url: str, observer: ResultsObserver, max_retry: int = 10, timeout: float = 15
) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """

    async with httpx.AsyncClient() as client:
        # # YOUR CODE GOES HERE
        retries = 0
        while retries < max_retry and retries != -1:
            try:
                response = await client.get(url, timeout=timeout)
                response.raise_for_status()
                data = response.read()

                observer.observe(data)
                retries = -1

            except httpx.HTTPStatusError as e:
                retries += 1
                print(f"An error occurred: {e}")

            except httpx.TimeoutException as e:
                retries = -1
                print(f"A timeout occurred: {e}")
        #####################
