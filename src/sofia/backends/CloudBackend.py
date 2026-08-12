from sofia.backends.Backend import Backend
import re

class CloudBackend(Backend):

    def execute(self, task):
        if task.intent == "summarize":
            sentences = re.split(r"[.!?]+", task.payload.get("text"))
            sentences = [sentence for sentence in sentences if sentence.strip()]
            words = []
    
            for sentence in sentences:
                words.extend(sentence.split())
            if len(sentences) == 1:
                    return task.payload.get("text")
               
            else:
                result_words = {}
                result_sentences = []
                word_end = None
                for word in words:
                    if word in result_words:
                        result_words[word] += 1
                        word_end = word
                    else:
                        result_words[word] = 1

                if word_end is None:
                    return task.payload.get("text")
                else:
                    for word in result_words:
                        if result_words[word] > result_words[word_end]:
                            word_end = word
                        
                    for sentence in sentences:
                        if word_end is not None and word_end in sentence:
                            result_sentences.append(sentence)
        
                return result_sentences
        else:
            return "error"