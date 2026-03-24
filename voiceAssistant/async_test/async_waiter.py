import asyncio
import time

async def cook_steak(table_number):
    print(f"Кухар отримав замовлення і почав готувати стейк для столика {table_number}")
    await asyncio.sleep(3)
    print(f"Стейк для столика {table_number} готовий")
    return f"Стейк для столика {table_number}"

async def serve_table(table_number: int):
    print(f'Офіціант підходить до столику {table_number}')
    print(f'Офіціант приймає замовлення {table_number}') 
    print(f'Офіціант передає замовлення для столика {table_number} на кухню')
    steak_task = asyncio.create_task(cook_steak(table_number)) # adds func to main event loop
    
    steak = await steak_task
    print(f"Офіціант отримав {steak} та подає його столику {table_number}")
    
async def main():
    start_time = time.time()
    list_tasks = [
        asyncio.create_task(serve_table(1)),
        asyncio.create_task(serve_table(2)),
        asyncio.create_task(serve_table(3))
    ]
    
    await asyncio.gather(*list_tasks)
    end_time = time.time()
    print(f"all time: {end_time - start_time}")
asyncio.run(main())