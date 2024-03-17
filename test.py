import time
import asyncio

async def task():
    time.sleep(2)
    print("Task")
    

async def main():
    asyncio.create_task(task())
    asyncio.create_task(task())
    asyncio.create_task(task())
    asyncio.create_task(task())
    print("Main")

asyncio.run(main())