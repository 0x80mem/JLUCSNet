class Document:
    def __init__(self):
        self.page_content = "Test Content 测试文档内容"*100
        self.meta_data = {
            "title": "Test Title 测试标题",
            "url": "www.baidu.com",
            "date": "Test date",
        }


'''
                -list
                    -tuple
                        -document
                            -page_content(str)
                            -meta_data(dic)
                                -'url':str
                                -'title':str
                                -'date': str or empty list
                        -float

    '''
Database_test_list = (
    (Document(), "0.85"),
    (Document(), "0.75"),
    (Document(), "0.65")
)
AI_test = """
以下是使用 C++ 编写的 "Hello, World!" 程序：

```
#include <iostream>



int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

这段代码使用了 C++ 的标准库中的 `iostream` 头文件，以便能够使用 `std::cout` 对象来输出文本到控制台。在 `main()` 函数中，我们调用 `std::cout` 的 `<<` 操作符来输出 "Hello, World!" 到控制台，并在最后加上 `std::endl` 来结束当前行并刷新输出缓冲区。
"""

