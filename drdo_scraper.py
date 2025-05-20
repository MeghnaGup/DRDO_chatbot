import asyncio
import json
from playwright.async_api import async_playwright

# This function gets all internal links from the homepage
async def get_internal_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.drdo.gov.in/drdo/")

        # Get all anchor tags and filter internal links
        links = await page.eval_on_selector_all("a", "elements => elements.map(el => el.href)")
        internal_links = list(set(link for link in links if link.startswith("https://www.drdo.gov.in")))
        
        await browser.close()
        return internal_links

# This function scrapes data from each internal page
async def scrape_page_data(page, url):
    await page.goto(url)
    title = await page.title()
    content = await page.inner_text("body")
    return {"url": url, "title": title, "content": content[:1000]}  # Trimming long content

# Main function that loops through all internal links
async def scrape_all_pages():
    internal_links = await get_internal_links()
    print(f"Found {len(internal_links)} internal links. Scraping...")

    all_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for idx, link in enumerate(internal_links):
            try:
                print(f"[{idx + 1}/{len(internal_links)}] Scraping: {link}")
                data = await scrape_page_data(page, link)
                all_data.append(data)
            except Exception as e:
                print(f"Failed to scrape {link}: {e}")

        await browser.close()

    return all_data

# Save the scraped data to a JSON file
def save_to_json(data, filename="drdo_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Data saved to {filename}")

# Run everything
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  # Makes it safe for nested event loops (optional for VS Code, needed for Jupyter)

    all_scraped_data = asyncio.run(scrape_all_pages())
    save_to_json(all_scraped_data)
