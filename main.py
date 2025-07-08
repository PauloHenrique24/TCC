import asyncio
from playwright.async_api import async_playwright
import json
import os

PROFILE_PATH = os.path.abspath("shein-profile")

async def buscar_shein(termo):
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_PATH,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        page = await browser.new_page()

        # Vai para o site
        await page.goto("https://br.shein.com", timeout=60000)
        await page.wait_for_selector("input.search-input", timeout=30000)

        # Digita o termo na barra de pesquisa
        await page.fill("input.search-input", termo)
        await page.click("button.search-button")
        await page.wait_for_timeout(5000)

        print(f"🔍 Buscando por: {termo}")

        # Scroll lento para carregar produtos
        for _ in range(8):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(1000)

        # Captura os produtos
        produtos = await page.query_selector_all("a.goods-title-link")

        for item in produtos[:10]:  # Limita aos 10 primeiros
            try:
                nome = await item.get_attribute("aria-label") or "Sem nome"
                link = await item.get_attribute("href") or ""
                link = f"https://br.shein.com{link}" if link.startswith("/") else link

                # Encontra o container geral do item
                container = await item.evaluate_handle("el => el.closest('.S-product-item')")

                preco = "Não encontrado"
                vendidos = "Não encontrado"

                if container:
                    preco_el = await container.query_selector("span.normal-price-ctn__sale-price")
                    if preco_el:
                        preco = await preco_el.inner_text()

                    vendidos_el = await container.query_selector("div.product-card__sales-label")
                    if vendidos_el:
                        vendidos = await vendidos_el.inner_text()

                resultados.append({
                    "produto": nome.strip(),
                    "preco": preco.strip(),
                    "vendidos": vendidos.strip(),
                    "link": link.strip()
                })

            except Exception as e:
                print(f"⚠️ Erro ao processar produto: {e}")
                continue

        await browser.close()
        return resultados

if __name__ == "__main__":
    termo = input("🔎 Digite o termo de busca na Shein: ").strip()
    if termo:
        resultado = asyncio.run(buscar_shein(termo))
        with open("resultado_shein.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print("✅ Resultados salvos em resultado_shein.json")
