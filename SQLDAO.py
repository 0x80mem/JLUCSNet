from sqlalchemy import create_engine
from Tables import Page, Content
from sqlalchemy.sql import text
import urllib.parse
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import os

class SQLDAO:
    def __init__(self, url, username, password):
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

        self.embeddings = HuggingFaceEmbeddings(model_name='aspire/acge_text_embedding', encode_kwargs = {'normalize_embeddings': True})
        if os.path.exists("faiss_db"):
            self.vector_store = FAISS.load_local("faiss_db", self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.vector_store = None

    def insertInfo(self, info):
        for page in info:
            url = page['url']
            title = page['title']
            contents = page['content']
            date = page['date']
            date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')

            self.session.merge(Page(url=url, title=title, date=date))
            self.session.commit()

            for i, content in enumerate(contents):
                self.session.merge(Content(url=url, start_paragraph=i, content=content))
                self.session.commit()

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=2, separators=["。", "！", "？", "；"])
                texts = text_splitter.split_text(content)
                if self.vector_store is None:
                    self.vector_store = FAISS.from_texts(
                        texts=texts,
                        embedding=self.embeddings,
                        metadatas=[{"date": page['date']} for _ in range(len(texts))],
                    )
                else:
                    for i, text in enumerate(texts):
                        res = self.vector_store.similarity_search_with_relevance_scores(text, k=1)
                        if res is None or res[0][1] < 1:
                            self.vector_store.merge_from(FAISS.from_texts(
                                texts=[text],
                                embedding=self.embeddings,
                                metadatas=[{"date": page['date']}]
                            ))
        self.vector_store.save_local("faiss_db")

    def searchWithRelevanceScores(self, query: str, k: int = 5):
        return self.vector_store.similarity_search_with_relevance_scores(query, k=k)
    
    def getEngine(self):
        return self.engine