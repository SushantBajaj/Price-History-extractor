from playwright.async_api import async_playwright
# import time
# import asyncio
from fastapi import FastAPI
app = FastAPI()

async def get_product_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-zygote',
            '--disable-gpu',
            '--mute-audio'
        ])
        context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
        page = await context.new_page()

        await page.goto("https://pricehistory.app")
        await page.fill("#search", url)
        await page.press("#search", "Enter")
        print("searched")
        await page.wait_for_url("https://pricehistory.app/*/*")
        new_url = page.url
        print("found :"+ new_url)
        # new_url = await page.evaluate("document.location.href")
        await browser.close()
        return new_url



async def extract_chart_data(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-zygote',
            '--disable-gpu',
            '--mute-audio'
        ])
        context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_function("window.ChartConfigs?.data?.datasets?.[1]?.data")
        variable_value = await page.evaluate("window.ChartConfigs.data.datasets[1].data")
        
        await browser.close()
        return variable_value

@app.get("/extract")
async def extract(url: str):
    print("changing from url to product url")
    product_url = await get_product_page(url)
    print(product_url)
    try:
        data = await extract_chart_data(product_url)
        return {"data": data}
    except Exception as e:
        return {"error": e}



# temp_url = "https://www.amazon.in/Portronics-Projector-Resolution-Rotatable-Streaming/dp/B0CQG7XMXC/?_encoding=UTF8&ref_=pd_hp_d_btf_gcx_gw_per_1"
# async def main():
#     product_url = await get_product_page(temp_url)
#     print(product_url)
#     data = await extract_chart_data(product_url)
#     print(data)

# asyncio.run(main())
# print(get_product_page(temp_url))
