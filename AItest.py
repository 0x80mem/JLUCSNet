import qianfan

class QianfanSemanticAnalysis:
    def __init__(self, ak, sk):
        self.chat_c = qianfan.ChatCompletion(ak=ak, sk=sk)

    def semantic_analysis(self, text):
        response = self.chat_c.do(
            model="ERNIE-3.5-8K-1222",
            messages=[
                {
                    "role": "user",
                    "content": text
                },
            ],
            temperature=1e-9,
        )
        result_text = response['body']['result']

        # 解析模型返回的文本结果，提取关键信息
        info_dict = {}
        lines = result_text.split('\n')
        for line in lines:
            if '：' in line:
                key, value = line.split('：', 1)
                info_dict[key.strip()] = value.strip()

        return info_dict


'''if __name__ == "__main__":
    # 替换成您的 API Key 和 Secret Key
    ak = "QNXKs4AnPVr9RakOgaHoPjdD"
    sk = "SzGodc2ftr7HQ1fjuo7LazVMhKIzCAU1"

    qianfan_sa = QianfanSemanticAnalysis(ak, sk)
    precommand = ("对提供的文段进行语义分析，提取出如下信息："
                  "（姓名，性别，邮箱，联系电话，最高学历，最高学位，办公地址，教研室，学科专业，研究方向，讲授课程，教育经历，工作经历，科研项目，学术论文，著作教材，获奖情况，社会兼职，科研成果，学生培养，治学格言，职称名称，毕业院校，个人简介，访问经历，荣誉奖励，报告交流，学术服务），"
                  "如果有文字与以上任意一条均不匹配，则将其归为（其他），如果有条目可以与多项匹配，则将其归为最为接近的一项，"
                 "如果有一项没有任何信息与之匹配，则该项以‘无’填充即可，并且提取的信息严格按照'姓名'：'xx'的格式，不要多加任何字符")
    # 输入要进行语义分析的文本
    input_text = input("请输入要进行关键词提取的文本：")

    # 获取语义分析结果
    result = qianfan_sa.semantic_analysis(precommand + input_text)

    # 输出语义分析结果
    print("语义分析结果：", result)'''
