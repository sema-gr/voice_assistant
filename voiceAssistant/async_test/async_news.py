import asyncio
import time

async def fetch_url(site_name, delay):
    print(f"Починаемо завантаження сайту {site_name}")
    await asyncio.sleep(delay)
    print(f"{site_name} завантажено за {delay} sec")
    return f"Данні {site_name}"

async def main():
    start_time = time.time()
    tasks = [
        fetch_url("Google", 2),
        fetch_url("GitHub", 3),
        fetch_url("ChatGPT", 1)
    ]
    results = await asyncio.gather(*tasks)
    print(f"Данні отримані: {results}")
    end_time = time.time()
    print(f"загальний час виконання: {end_time - start_time}")
asyncio.run(main())                      