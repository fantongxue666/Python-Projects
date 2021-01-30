import asyncio
import time
import aiohttp

async def request(url):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as response:
            # text()返回字符串形式的响应数据
            # read()返回二进制形式的响应数据
            # json()返回的就是json对象
            # 注意：获取响应数据操作之前一定要使用await进行手动挂起
            page_text = await response.text()

start = time.time()

urls=[
    "www.test.com",
    "www.test123.com",
    "www.456.com"
]

# 任务列表：存放多个任务对象
stasks = []
for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    stasks.append(task)

loop = asyncio.get_event_loop()
# 需要将任务列表封装到wait中
loop.run_until_complete(asyncio.wait(stasks))

print("耗时",time.time()-start)