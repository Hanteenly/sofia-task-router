from sofia.backends.Backend import Backend
import re

class LocalBackend(Backend):

    def execute(self, task):
        if task.intent == "summarize":
            sentences = re.split(r"[.!?]+", task.payload.get("text"))
            sentences = [sentence for sentence in sentences if sentence.strip()]
            words = []

            for sentence in sentences:
                words.extend(sentence.split())

            if len(sentences) <= 3:
                return task.payload.get("text")

            elif len(sentences) <= 6:
                result_words = {}
                result = []
                result_sentences = []

                for word in words:
                    if word in result_words:
                        result_words[word] += 1
                    else:
                        result_words[word] = 1

                for word in result_words:
                    if result_words[word] > 2:
                        result.append(word)

                for word in result:
                    for sentence in sentences:
                        if word in sentence:
                            result_sentences.append(sentence)

                return result_sentences
            
            elif len(sentences) > 6:
                result_words = {}
                result = []
                result_sentences = []
                for word in words:
                    if word in result_words:
                        result_words[word] += 1
                    else:
                        result_words[word] = 1
            
                for word in result_words:
                    if result_words[word] > 4:
                        result.append(word)
            
                for word in result:
                    for sentence in sentences:
                        if word in sentence:
                            result_sentences.append(sentence)

                return result_sentences
        else:
            return "error"