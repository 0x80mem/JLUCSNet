import mainWindow
from PyQt5.QtWidgets import QApplication
from LLMChat import LLMChat
import sys
import threading
import time
import torch

class Chat:
    def __init__(self, llm):
        self.llm = llm
        self.mutex = threading.Lock()

    def getRevalentDocs(self, query):
        self.mutex.acquire()
        torch.cuda.empty_cache()
        try:
            docs = self.llm.getDocs(query)
            for doc in docs:
                doc[0].page_content = f"...{doc[0].page_content[len(doc[0].metadata['title']) + len(doc[0].metadata['date']) + 3:]}..."
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
            output = self.llm.getResponse(query)
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