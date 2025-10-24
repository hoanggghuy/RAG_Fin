class Reflection:
    def __init__(self,llm):
        self.llm = llm
    def concat_and_format_text(self, texts):
        concat_text = []
        for text in texts:
            role = text.get('role')
            content = text.get('content')

            if role and content:
                concat_text.append(f"{role}: {content}")
        return '\n'.join(concat_text)
    def __call__(self, chat_history, query,length = 10):
        if len(chat_history) >= length:
            chat_history = chat_history[len(chat_history) - length:]
        history_string = self.concat_and_format_text(chat_history)
        self.conversation = {
            "role": "user",
            "content": f"{history_string} đây là lịch sử trò chuyện hãy kết hợp cùng {query} để đưa ra câu hỏi chính xác nhất mà khách hàng đang muốn hỏi. Kết quả trả về duy nhất là câu hỏi sát với {query} nhất và nội dung kết quả không được bao gồm các thông tin trong lịch sử trò chuyện và các câu hỏi trước đó. Không được hỏi thêm gì."
        }
        completion = self.llm.generate_content([self.conversation])
        return completion