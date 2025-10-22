import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

def chunk_data(input_path:str,output_path:str,chunk_size:int,chunk_overlap:int):
    if not os.path.exists(input_path):
        print("Input path does not exist")
    with open(input_path,"r",encoding="utf-8") as f:
        input_data = json.load(f)
    texts = []
    if isinstance(input_data,list):
        for text in input_data:
            texts.append(
                {
                    "metadata": text["metadata"],
                    "page_content": text["page_content"],
                }
            )
    else: print("Data is wrong format")

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    chunks =[]
    for text in texts:
        page_content = text["page_content"]
        if text["metadata"]["category"] == "Thông tin chi tiết sản phẩm":
            for chunk in splitter.split_text(page_content):
                chunks.append({
                    "metadata": text["metadata"],
                    "page_content": chunk,
                })
        else:
            chunks.append({
                "metadata": text["metadata"],
                "page_content": page_content,
            })
    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(chunks,f,ensure_ascii=False,indent=4)

