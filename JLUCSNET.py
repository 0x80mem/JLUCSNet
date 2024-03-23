import mainWindow
from PyQt5.QtWidgets import QApplication
from LLMChat import LLMChat
import sys
import threading
import time
import torch

llm = LLMChat()
_window = None
def gpt_slot(query):
    global llm
    _window.gpt_mutex.acquire()

    try:
        torch.cuda.empty_cache()
        docs = llm.getDocs(query)
        _window.display_message(str(docs), role="ChatGPT")
        output = llm.getResponse(query)
        # _window.display_message(str(query), role="You")
        _window.display_message(str(output), role="ChatGPT")
    except Exception as e:
        torch.cuda.empty_cache()
        _window.display_message(str(e), role="ChatGPT")
    time.sleep(3)
    torch.cuda.empty_cache()
    _window.gpt_mutex.release()

if __name__ == '__main__':
    llm = LLMChat()
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow(gpt_slot = gpt_slot)
    window.gpt_mutex = threading.Lock()
    _window = window
    window.show()
    sys.exit(app.exec_())