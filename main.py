import asyncio
import time
import httpx
import pprint

URLS = [
    "https://google.com", "https://github.com", "https://python.org", "https://example.com", "https://invalid.example"
]

async def check_website(client, url, semaphores):
    async with semaphores:
        try:
            start = time.perf_counter()
            
            response = await client.get(url)
            
            response.raise_for_status()
            
            duration = time.perf_counter() - start
            
            return response.status_code, duration
        
        except httpx.HTTPStatusError as exc:
            return f"{exc.response.status_code}"
            
        except httpx.ConnectError as exc:
            return f"{exc}"
        
        except httpx.ConnectTimeout as exc:
            return f"{exc}"
            
        
async def main():
    print("====================================================")
    print("                    PULSE CHECK                     ")
    print("               Website Health Monitor               ")
    print("====================================================")
    
    print("")
    print(f"checking {len(URLS)} websites...")

    print("")
    print("WEBSITE                   STATUS       RESPONSE TIME")
    
    async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
        semaphore = asyncio.Semaphore(5)
        results = await asyncio.gather(
            *(check_website(client, url, semaphore) for url in URLS)
        )  
            
        online_count = 0
        offline_count = 0
        response_time = []

        for url, result in zip(URLS, results):
            if isinstance(result, tuple):
                status, duration = result
                if 200 <= status < 300:
                    response_time.append(duration)
                    status = "ONLINE"
                    online_count += 1
                    print(f"{url}         {status}         {duration*1000:.2f}ms")
                else:
                    offline_count += 1
                    print(f"{url}         HTTP ERROR     {duration * 1000:.2f} ms")
            else:
                status = "OFFLINE"
                offline_count += 1
                print(f"{url}         {status}         N/A")
            
        
        print("====================================================")
        print("                    SUMMARY                         ")
        print("====================================================")
        
        print(f"Total websites checked: {len(URLS)}")
        print(f"Online:                  {online_count}")
        print(f"Offline:                 {offline_count}")
        
        average_times = sum(response_time) / len(response_time)
        print(f"Average response time: {average_times*1000:.2f} ms")

asyncio.run(main())