from completion import OpenAICompletion
import random
from synthetic_query_messages import SYSTEM_MESSAGE, USER_MESSAGE
from tqdm import tqdm


OPENAI_MODELS = ["gpt-3.5-turbo-1106", "gpt-4", "gpt-4-turbo"]

class SyntheticQueryCreator:
    def __init__(self, system_message, human_message, model, client):
        self.system_message = system_message
        self.human_message = human_message
        if model in OPENAI_MODELS:
            self.model = OpenAICompletion(system_message, human_message, model, client)
        else:
            raise ValueError("Model not supported yet.")
        
    def run(self, corpus, number_of_questions=100):
        docs = corpus.dataset.text.text()
        ids = corpus.dataset.id.text()
        
        questions = []
        relevance = []
        pbar = tqdm(total=number_of_questions)

        # Randomly draw the documents that we will generate questions for
        doc_indices = random.sample(range(len(docs)), number_of_questions)
        for d in doc_indices:
            text, label = docs[d], ids[d]
            question = self.model.run(text)
            questions.append(question)
            relevance.append(label)
            pbar.update(1)
        pbar.close()
        return questions, relevance


def create_synthetic_queries(
    corpus,
    system_message=SYSTEM_MESSAGE,
    human_message=USER_MESSAGE,
    model="gpt-3.5-turbo-1106",
    number_of_questions=100,
    save_to_file=True,
    dataset_name="",
):
    creator = SyntheticQueryCreator(system_message, human_message, model)
    questions, relevance = creator.run(corpus, number_of_questions)
    if save_to_file:
        if dataset_name:
            dataset_name = f'{dataset_name}_'
        
        with open(f'{dataset_name}questions_{number_of_questions}.txt', 'w') as f:
            f.write('\n'.join(questions))
        
        with open(f'{dataset_name}relevance_{number_of_questions}.txt', 'w') as f:
            f.write('\n'.join(relevance))
    return questions, relevance


def load_synthetic_queries(path_to_questions, path_to_relevance):
    with open(path_to_questions, "r") as f:
        questions = f.read()
        questions = questions.split("\n")
    
    with open(path_to_relevance, "r") as f:
        relevance = f.read()
        relevance = relevance.split("\n")
    return questions, relevance