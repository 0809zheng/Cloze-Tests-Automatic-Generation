import generator
import random
from tkinter import *  # 导入 Tkinter 库


def insert_point():
    word = entry.get()
    sentences = generator.get_sentences(word)
    scores = [0 for i in sentences]
    complexity_scores = generator.get_complexity_score(sentences)
    context_scores = generator.get_context_score(sentences)
    grammar_scores = generator.get_grammar_score(sentences, word)
    length_scores = generator.get_length_score(sentences)
    for i in range(len(scores)):
        scores[i] += (complexity_scores[i] / max(complexity_scores)) * \
                     (context_scores[i] / max(context_scores)) * \
                     (grammar_scores[i] / max(grammar_scores)) * \
                     (length_scores[i] / max(length_scores))
    for i in range(len(scores)):
        print(round(scores[i], 10), end=": ")
        print(sentences[i])
    try:
        sentence = sentences[scores.index(max(scores))]
        if not sentence:
            text.insert(INSERT, "Sorry! Can't generate cloze test for \"" + word + "\".")
        else:
            distracts = [word]
            synonym = generator.get_synonym(word)
            distracts += generator.get_distracts(sentence, word)  # 还没删近义词
            distracts = [x.lower() for x in distracts]
            random.shuffle(distracts)
            sentence = sentence.replace(word, '_____')
            text.insert(INSERT, sentence + "\n\n")
            count = 0
            for w in distracts:
                count += 1
                text.insert(INSERT, str(count) + ". " + w + "   ")
            text.insert(INSERT, "\n\nCorrect answer: " + word)
    except ValueError:
        text.insert(INSERT, "Sorry! Can't generate cloze test for \"" + word + "\".")


root = Tk()
root.title('Cloze Test Generator')
# root.geometry('500x500')
Label(root, text="Your word").grid(row=0, sticky=E, padx=5, ipadx=5, pady=10)
entry = Entry(root)
entry.grid(row=0, sticky=E + W, column=1, padx=5, ipadx=5, pady=10)
button = Button(root, text="Generate", command=insert_point)
button.grid(row=0, column=2, pady=10)
text = Text(root, width=60, height=10, font=("Consolas", 10, "normal"))
text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
root.mainloop()
