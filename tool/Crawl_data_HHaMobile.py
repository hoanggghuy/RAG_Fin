import time
import requests
from bs4 import BeautifulSoup
import json


all_doc_for_rag = []

class Crawl_Data_HHaMobile:
    def __init__(self,urls: list):
        if not isinstance(urls, list):
            raise TypeError("urls should be a list")
        self.urls = urls
        self.scraped_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def crawl_single_product(self,url):
        try:
            response = requests.get(url, headers=self.headers,timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            product_data = {}
            name_element = soup.select_one("div.header-name h1")
            product_data["ten_san_pham"] = name_element.text.strip() if name_element else None
            product_data["gia_cac_phien_ban_va_mau"] = []
            version_options = soup.select("div#option-version .item-option")
            for option in version_options:
                version_name = option.select_one("span")
                version_price = option.select_one("p")
                if version_name and version_price:
                    product_data["gia_cac_phien_ban_va_mau"].append(
                        {"phien_ban": version_name.text.strip(),"gia_ban": version_price.text.strip()}
                    )
            color_options = soup.select("div#option-color .item-option")
            for option in color_options:
                color_name = option.select_one("span")
                color_price = option.select_one("p")
                if color_name and color_price:
                    product_data["gia_cac_phien_ban_va_mau"].append(
                        {"mau_sac": color_name.text.strip(), "gia_ban": color_price.text.strip()}
                    )
            product_data["uu_dai"] = [
                promo.get_text(separator= " ", strip=True)
                for promo in soup.select("#product-promotion-content .promotion-item span, #product-promotion-more .promotion-item span")
                if promo
            ]

            product_data["thong_tin_san_pham"] = [
                p.get_text(separator="",strip=True)
                for p in soup.select("#productContent p")
                if p and p.get_text(strip=True)
            ]

            product_data["thong_so_ky_thuat"] = {
                spec.select_one("strong").text.strip(): spec.select_one("span").get_text(strip=True)
                for spec in soup.select("#specs-content li")
                if spec.select_one("strong") and spec.select_one("span")
            }
            return product_data
        except Exception as e:
            print(e)


    def group_data(self,product_data,url):
        if not product_data: return []

        documents = []
        base_metadata = {
            "product_name": product_data.get("ten_san_pham","None"),
            "source_url": url
        }
        grouped_content = {
            "Giá bán": [],
            "Ưu đãi": [],
            "Thông tin chi tiết sản phẩm": []
        }

        for item in product_data.get("gia_cac_phien_ban_va_mau",[]):
            if "phien_ban" in item:
                grouped_content["Giá bán"].append(f"bộ nhớ {item['phien_ban']} giá {item['gia_ban']}.")
            elif "mau_sac" in item:
                grouped_content["Giá bán"].append(f"Bản màu {item['mau_sac']} giá {item['gia_ban']}.")
        for promo in product_data.get("uu_dai",[]):
            grouped_content["Ưu đãi"].append(f"{promo}")
        for key, value in product_data.get("thong_so_ky_thuat", {}).items():
            grouped_content["Thông tin chi tiết sản phẩm"].append(f"{key} {value}")
        for spec in product_data.get("thong_tin_san_pham", []):
            if len(spec) > 20:
                grouped_content["Thông tin chi tiết sản phẩm"].append(spec)

        for category, content_list in grouped_content.items():
            if content_list:
                page_content = "\n".join(content_list)
                metadata = base_metadata.copy()
                metadata["category"] = category
                documents.append({"page_content": page_content, "metadata": metadata})
        return documents

    def run(self):
        all_documents = []
        for url in self.urls:
            raw_data = self.crawl_single_product(url)
            if raw_data:
                processed_docs =self.group_data(raw_data,url)
                all_documents.extend(processed_docs)
            time.sleep(1)
        self.scraped_data = all_documents
        return self.scraped_data

    def save_to_json(self,path):
        with open(path,"w",encoding="utf-8") as f:
            json.dump(self.scraped_data,f,indent=4,ensure_ascii=False)
