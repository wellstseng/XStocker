
import asyncio
try:
    from web.stock.tasks import load_predict_price
except:
    from stock.tasks import load_predict_price
__loading_queue=[]

async def __execute_async_loading_queue():
    while len(__loading_queue) != 0:
        stock_id = __loading_queue[0]
        result = load_predict_price.delay(stock_id)
        while result.status == "Pending":
            await asyncio.sleep(0.5)
        del __loading_queue[0]
        await asyncio.sleep(10)

def load(stock_id:str):
    if  stock_id in __loading_queue:
        return 
    enable_loader = False
    if len(__loading_queue) == 0:
        enable_loader = True

    __loading_queue.append(stock_id) 

    if enable_loader:
        asyncio.run(__execute_async_loading_queue())
    


