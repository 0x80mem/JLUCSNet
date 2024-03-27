from langchain_community.llms.chatglm import ChatGLM
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from SQLDAO import SQLDAO
import Config
import torch
import time
import datetime

endpoint_url = (
            "http://127.0.0.1:8123"
        )

class LLMChat:
    def __init__(self, k: int = 3):
        self.k = k
        self.sqldao = SQLDAO(Config.sqlConnection['url'], Config.sqlConnection['user'], Config.sqlConnection['password'], device='cpu')
        self.retriever = self.sqldao.vector_store.as_retriever(
            search_type="similarity_score_threshold", 
            search_kwargs={'score_threshold': 0.0, 'k': k})
        self.llm = ChatGLM(
            endpoint_url=endpoint_url,
            model_kwargs={"device": "cpu"},
        )

    def getResponse(self, query: str):

        template = f"""你是一个吉林大学计算机科学技术学院信息帮助助手，你应当仅基于以下上下文回答问题:
        {{context}}
        时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        问题: {{question}}
        """
        prompt = ChatPromptTemplate.from_template(template)

        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        output = self.chain.invoke(query)
        torch.cuda.empty_cache()
        return output
    
    def getDocs(self, query: str):
        docs = self.sqldao.searchWithRelevanceScores(query, self.k)
        torch.cuda.empty_cache()
        return docs
        

# sql = SQLDAO(Config.sqlConnection['url'], Config.sqlConnection['user'], Config.sqlConnection['password'])
# sql.insertInfo([
#     {
#         'url': 'https://www.jlu.edu.cn',
#         'title': '吉林大学',
#         'date': 'Wed, 01 Dec 2021 00:00:00 GMT',
#         'content': [
#             '当想在多个索引中，复用一个 Node 时，可以通过定义 DocumentStore 结构，并在添加Nodes时指定 DocumentStore', 
#             'langchain是一个大语言模型Agent开发框架，我们在这里使用它读取数据内容并建立索引，完成对前述文本嵌入模型和数据库的调用，搜索引擎构建'
#             ]
#     },
#     {
#         'url': 'https://www.jlu.12du.cn',
#         'title': '吉林大s学',
#         'date': 'Wed, 01 Dec 2022 00:00:00 GMT',
#         'content': [
#             '当想在多个索引中通过定义 DocumentStore 结构，并在添加Nodes时指定 DocumentStore', 
#             'langchain是一个大，我们在这里使用它读取数据内容并建立索引，完成对前述文本嵌入模型和数据库的调用，搜索引擎构建'
#             ]
#     },
#     {
#         'url': 'https://baike.baidu.com/item/%E7%A7%A6%E5%A7%8B%E7%9A%87/6164',
#         'title': '秦始皇',
#         'date': 'Wed, 01 Dec 2023 00:00:00 GMT',
#         'content': [
#             """秦始皇嬴政（前259年—前210年），嬴姓，赵氏（一说秦氏），名政（一说正） [3] [140] ，也有祖龙 [1]、吕政 [2]等别称
#             （详见“人物争议-姓名之争”）。中国古代杰出的政治家、战略家、改革家，中国历史上第一个专制主义中央集权国家——秦朝的建立
#             者，中国第一位称皇帝的君主。 [149]""",
#             """"嬴政为秦庄襄王和赵姬之子，因父亲在赵国做人质，故生于赵都邯郸。 [3]秦庄襄王成为秦国太子后，嬴政被放回秦国。 [1
#             6]前247年，嬴政继承王位。前238年，平定长信侯嫪毐叛乱，并铲除权臣吕不韦，开始亲政，起用李斯、尉缭等客卿。自前230年起
#             ，先后灭韩、赵、魏、楚、燕、齐，完成了一统六国的大业。 [149]""",
#             """前221年，嬴政自诩“德兼三皇，功过五帝”，采用三皇之“皇”、五帝之“帝”构成“皇帝”称号，被称为“始皇帝”。 [6] [65]政治
#             上，嬴政在中央设置三公九卿，地方上废除分封制，代以郡县制；经济上，统一货币和度量衡；社会文化上，实施书同文，车同轨的
#             政策，以首都咸阳为中心修筑通往各地的道路，规定以法为教，以吏为师；军事上，北击匈奴，收取河南地，修筑万里长城；南征百
#             越，修筑灵渠，沟通长江和珠江水系。 [149]前210年，嬴政驾崩于沙丘平台，享年五十岁，葬于骊山秦始皇陵。死后由胡亥继位，
#             翌年就爆发了埋葬秦朝的秦末农民战争。 [150]""",
#             """嬴政结束了春秋战国诸侯纷争的局面 [149]，奠定了中国两千余年政治制度基本格局 [151]，被明代思想家李贽誉为“千古一帝”
#             。 [152]同时，他推行严刑峻法、焚书坑儒、穷奢极欲、大兴土木、妄图成仙、滥征徭役等行为也引发后世争议。"""
#         ]
#     }
# ])
# chat = LLMChat()
# 
# import time
# print(chat.getResponse("秦始皇是谁"))
# time.sleep(5)
# print(chat.getResponse("秦始皇什么时候死的"))


