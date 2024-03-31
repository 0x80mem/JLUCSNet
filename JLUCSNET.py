import mainWindow
from PyQt5.QtWidgets import QApplication
from LLMChat import LLMChat
import sys
import threading
import copy
import torch
import time
from datetime import datetime

class Chat:
    def __init__(self, llm: LLMChat):
        self.llm = llm
        self.mutex = threading.Lock()

    def getRevalentDocs(self, query):
        self.mutex.acquire()
        torch.cuda.empty_cache()
        try:
            docs = copy.deepcopy(self.llm.getDocs(query))
            for doc in docs:
                doc[0].page_content = f"...{doc[0].page_content[len(doc[0].metadata['title']) + len(doc[0].metadata['date']) + 2:]}..."
        except Exception as e:
            torch.cuda.empty_cache()
            self.mutex.release()
            return str(e), "System"
        torch.cuda.empty_cache()
        self.mutex.release()
        return (docs, "DataBase")
    
    def getResponse(self, query):
        self.mutex.acquire()
        torch.cuda.empty_cache()

        try:
            try:
                output = self.llm.getResponse(query)
            except Exception as e:
                output = self.llm.getResponse(query, k = 2)
        except Exception as e:
            torch.cuda.empty_cache()
            self.mutex.release()
            return str(e), "System"
        torch.cuda.empty_cache()
        self.mutex.release()
        return (output, "AI")

    def gpt_slot(self, input):
        return (self.getRevalentDocs(input), self.getResponse(input))
        

if __name__ == '__main__':
    llm = LLMChat()
    app = QApplication(sys.argv)
    chat = Chat(llm)
    window = mainWindow.NWindow(gpt_slot = chat.gpt_slot)
    chat.window = window
    window.show()
    sys.exit(app.exec_())