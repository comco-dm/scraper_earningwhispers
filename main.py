

import json
import aiohttp
from context import cookies, headers, url_target

async def get_data(date: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url_target}/{date}', cookies=cookies, headers=headers) as response:
            return await response.json()

#save data to json
async def save_data(data: dict):    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
                  
if __name__ == '__main__':
    date = 20250605
    import asyncio
    data = asyncio.run(get_data(str(date)))
    asyncio.run(save_data(data))