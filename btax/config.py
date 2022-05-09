from btax.settings import CLIENT_ID, CLIENT_SECRET, DOMAIN, TS_PLUGBOLETO_BASE_URL, TS_TOKEN, TS_CNPJ
#from btax.decorators import bitrix_auth
from pybitrix24 import Bitrix24
import asyncio
#remoto:
bx24 = Bitrix24(DOMAIN, CLIENT_ID, CLIENT_SECRET)

async def ref():
   try:
        await asyncio.sleep(5)
        bx24.refresh_tokens()
   except Exception as e:
        print(e)
        pass
asyncio.run(ref())
