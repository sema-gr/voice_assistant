import time

def serve_table(table_number: int):
    print(f"Офіціант підходе до столика {table_number}")
    print(f"Офіціант приймає замовлення у столика {table_number}")
    print(f"Офіціант іде на кухню і починає готувати стейк для столика {table_number}")
    time.sleep(3)
    print(f"Стейк для столика №{table_number} готовий")
    print(f"Офіціант подіє стейк столику {table_number}")
    print("==========================================================\n")

start_time = time.time()
for i in range(3):
    serve_table(i+1)
end_time = time.time()

print(f"\n time for these tasks: {end_time-start_time}")