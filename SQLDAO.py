from sqlalchemy import create_engine
from Tables import Page, Content
from sqlalchemy.sql import text
import urllib.parse
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import numpy as np
import re

import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import os

def spiltText(text, max_length=256):
    matches = matches = [match.start() for match in re.finditer(r'[。！？；]', text)]
    if len(matches) == 0:
        return RecursiveCharacterTextSplitter(chunk_size=max_length, chunk_overlap=max_length//4).split_text(text)

    start, end, sentence_count = 0, 0, 0
    ret = []
    for i, p in enumerate(matches):
        end = p
        sentence_count += 1
        if end - start > 256:
            ret.append(text[start:start+max_length])
            start += max_length
            sentence_count = 0
        elif sentence_count >= 5 or i == len(matches)-1 or matches[i+1] - start > 256:
            ret.append(text[start:end+1])
            start = end+1
            sentence_count = 0
    if len(text) > max_length:
        ret.append(text[-max_length:])
    return ret
    

class SQLDAO:
    def __init__(self, url, username, password, device='cuda'):
        self.url = url
        self.username = username
        self.password = urllib.parse.quote_plus(password)
        self.engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.url}")
        self.engine.connect().execute(text('CREATE DATABASE IF NOT EXISTS JLUCSNet'))
        self.engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.url}/JLUCSNet")
        Page.__table__.create(self.engine, checkfirst=True)
        Content.__table__.create(self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.embeddings = HuggingFaceEmbeddings(
            model_name='aspire/acge_text_embedding', 
            model_kwargs= {'device': device}, 
            encode_kwargs = {'normalize_embeddings': True})
        if os.path.exists("faiss_db"):
            self.vector_store = FAISS.load_local("faiss_db", self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.vector_store = None

    def insertInfo(self, info):
        #for page in info:
        page = info
        url = page['url']
        title = page['title']
        contents = page['content']
        if len(contents) == 0:
            contents = [title]
            date = datetime.now()
        else:
            date = page['date']
            date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            if 'realtime' in page:
                date = datetime.strptime(page['realtime'], '%Y-%m-%d')
                page['date'] = page['realtime']

        self.session.merge(Page(url=url, title=title, date=date))
        self.session.commit()

        for i, lcontent in enumerate(contents):
            lcontent = re.sub(r'<[^>]*>', ' ', lcontent)
            lcontent = re.sub(r'[^\S\n]+', ' ', lcontent)
            lcontent = re.sub(r'\s*\n\s*', '\n', lcontent)
            lcontents = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128).split_text(lcontent)
            if len(lcontent) > 1024:
                lcontents.append(lcontent[-1024:])
            for content in lcontents:
                self.session.merge(Content(url=url, start_paragraph=i, content=content))
                self.session.commit()

                texts = spiltText(content, max_length=200)
                print(texts)
                if self.vector_store is None:
                    self.vector_store = FAISS.from_texts(
                        texts=[f"{title} {page['date']}:{text}" for text in texts],
                        embedding=self.embeddings,
                        metadatas=[{"url": url, "date": page['date'], "title": title} for _ in range(len(texts))],
                    )
                else:
                    for i, text in enumerate(texts):
                        res = self.vector_store.similarity_search_with_relevance_scores(text, k=1)
                        if res is None or res[0][1] < 0.99:
                            self.vector_store.merge_from(FAISS.from_texts(
                                texts=[f"{title} {page['date']}:{text}"],
                                embedding=self.embeddings,
                                metadatas=[{"url": url, "date": page['date'], "title": title}]
                            ))
        self.vector_store.save_local("faiss_db")

    def searchWithRelevanceScores(self, query: str, k: int = 5):
        embedding = self.embeddings.embed_query(query)
        return self.vector_store.max_marginal_relevance_search_with_score_by_vector(embedding, k=k)
    
    def getEngine(self):
        return self.engine
    
    def clearAll(self):
        Content.__table__.drop(self.engine, checkfirst=True)
        Page.__table__.drop(self.engine, checkfirst=True)
        self.vector_store = None
        if os.path.exists("faiss_db"):
            os.remove("faiss_db\\index.faiss")
            os.remove("faiss_db\\index.pkl")
            os.rmdir("faiss_db")
        Page.__table__.create(self.engine, checkfirst=True)
        Content.__table__.create(self.engine, checkfirst=True)