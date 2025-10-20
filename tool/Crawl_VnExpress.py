from langchain_community.document_loaders import WebBaseLoader
import json
from bs4 import BeautifulSoup
import requests
from langchain_core.documents import Document

class Crawl_Data(WebBaseLoader):
    def __init__(self,url: list):
        super().__init__(web_paths=url)

    def load(self) -> list[Document]:
        docs = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        for url in self.web_paths:
            try:
                response = requests.get(url, headers=headers,timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                print("Request Exception {}".format(e))
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            doc_contents = ""
            title =soup.find("div", class_= "sidebar-1")
            if title:
                if h1_tag := title.find("h1",class_= "title-detail"):
                    doc_contents += h1_tag.get_text(strip=True) + "\n\n"
                if p_tag := title.find("p", class_ ="description"):
                    doc_contents += p_tag.get_text(strip=True) + "\n\n"

            content_div = soup.find("article", class_= "fck_detail")
            if content_div:
                for element in content_div.find_all(["h2","h3","p","ul","q"]):
                    if element.name in ["h2","h3","q"]:
                        doc_contents += element.get_text(strip=True) + "\n\n"
                    elif element.name == "p":
                        doc_contents += element.get_text(strip=True) + "\n\n"
                    elif element.name == "ul":
                        doc_contents += element.get_text(strip=True) + "\n\n"
                        for li_tag in element.find_all("li"):
                            doc_contents += f"-{li_tag.get_text(strip=True)}\n"
                            doc_contents += "/n"

            final_doc = doc_contents.strip()

            title_text = "Nothing"
            if title and (h1 := title.find("h1")):
                title_text = h1.get_text(strip=True)
            metadata = {"source": url, "title": title_text}
            if final_doc:
                docs.append(Document(page_content=final_doc, metadata=metadata))

        return docs


urls = [
    "https://vnexpress.net/chuyen-tham-cua-tong-bi-thu-gop-phan-dua-quan-he-viet-nam-trieu-tien-sang-giai-doan-moi-4950219.html",
    "https://vnexpress.net/ong-biden-va-ong-trump-chuan-bi-cho-cuoc-tranh-luan-thay-doi-cuc-dien-4761483.html"
]

if __name__ == "__main__":
    loader = Crawl_Data(urls)
    documents = loader.load()


    if documents:
        data_to_save = []
        for doc in documents:
            data_to_save.append(
                {
                    "metadata": doc.metadata,
                    "page_content": doc.page_content,
                }
            )
        if data_to_save:
            data_file_name = "../../data/data_crawl/Crawl_Data.json"
            with open(data_file_name, "w", encoding ="utf-8") as f:
                json.dump(data_to_save, f,ensure_ascii=False, indent=4)




