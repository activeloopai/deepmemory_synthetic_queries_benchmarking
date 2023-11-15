class OpenAICompletion:
    def __init__(self, system_message, human_message, model, client):
        self.client = client
        self.model = model
        self.system_message = system_message
        self.human_message = human_message
    
    def run(self, text):
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": self.human_message.format(input=text)},
            ]
        )
        return self._get_question_from_response(response)
    
    def _get_question_from_response(self, response):
        output_str = response.choices[0].message.content
        _, question = output_str.split(":")
        return question.replace("\"", "").replace("}", "").strip()