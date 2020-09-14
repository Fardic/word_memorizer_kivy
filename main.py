import sqlite3
from random import randint
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

Window.clearcolor = (0, .2, .2, 1)

saved_word_indexes = set()
saved_words = set()
saved_headwords = set()
saved_text = list()


# Selects random word from database for memory game
def select_random_word():
    conn = sqlite3.connect("prefac_wordlist.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM words")
    conn.commit()
    length = c.fetchone()
    # print(length)
    conn.commit()
    randomInt = randint(1, length[0] - 1)
    c.execute("SELECT * FROM words WHERE rowid = " + str(randomInt))
    conn.commit()
    words = c.fetchone()
    conn.commit()
    headword = words
    conn.close()
    return headword, randomInt


# Takes the saved word indexes from database and adds new word index
def save_words():
    conn = sqlite3.connect("prefac_wordlist.db")
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE Headword = 2424")
    saved_word = c.fetchone()
    print(saved_word[2])
    conn.commit()


    if saved_word[2] == "-1":
        temp_str = ""
        for i in saved_word_indexes:
            temp_str += i + " "
        c = conn.cursor()
        c.execute("UPDATE words SET Verb = \'" + temp_str + "\' WHERE Headword = '2424'")
        conn.commit()
    else:
        temp_str = ""
        temp_arr = saved_word[2].split()
        for i in temp_arr:
            saved_word_indexes.add(i)
        for i in saved_word_indexes:
            temp_str += i + " "
        c = conn.cursor()
        c.execute("UPDATE words SET Verb = \'" + temp_str + "\' WHERE Headword = '2424'")
        conn.commit()
    conn.close()


def import_saved_words():
    conn = sqlite3.connect("prefac_wordlist.db")
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE Headword = 2424")
    conn.commit()
    saved_word = c.fetchone()
    conn.commit()
    if saved_word[2] == "-1":
        pass
    else:
        temp_set = set()
        temp_set.add("No Words Have Been Saved")
        saved_headwords.difference(temp_set)

        temp_arr = saved_word[2].split()
        for i in temp_arr:
            saved_word_indexes.add(i)

        for i in saved_word_indexes:
            c = conn.cursor()
            c.execute("SELECT * FROM words WHERE rowid = " + i)
            conn.commit()
            word = c.fetchone()
            conn.commit()
            saved_words.add(word)
            saved_headwords.add(word[0])
    conn.close()

def remove_saved_word(word):
    conn = sqlite3.connect("prefac_wordlist.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM words WHERE Headword = \'" + word + "\'")
    conn.commit()
    index = c.fetchone()
    conn.commit()
    print(index)
    conn.close()

    conn = sqlite3.connect("prefac_wordlist.db")
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE Headword = 2424")
    saved_word = c.fetchone()
    print(saved_word[2])
    conn.commit()

    temp_str = ""
    temp_arr = saved_word[2].split()
    for i in temp_arr:
        saved_word_indexes.add(i)
    saved_word_indexes.remove(str(index[0]))
    if len(saved_word_indexes) < 1:
        temp_str = "-1"
    else:
        for i in saved_word_indexes:
            temp_str += i + " "
    print(temp_str)
    c = conn.cursor()
    c.execute("UPDATE words SET Verb = \'" + temp_str + "\' WHERE Headword = '2424'")
    conn.commit()
    conn.close()
    saved_headwords.remove(word)
    print(saved_word)
    print(saved_word_indexes)
    print(saved_headwords)

class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.saved_words = saved_words
        self.saved_headwords = saved_headwords

    def exit_memorizer(self):
        App.get_running_app().stop()

    def saved_button(self):
        import_saved_words()
    pass


class SavedWindow(Screen):
    def __init__(self, **kwargs):
        super(SavedWindow, self).__init__(**kwargs)
        # self.trig()
        self.saved_words = saved_words
        self.saved_headwords = saved_headwords
        self.headwords_arr = list()
        self.words_arr = list()

    def pressed_button(self, instance):
        print(instance.text)
        saved_text.clear()
        saved_text.append(instance.text)
        self.manager.current = "saved_meaning"

    def my_callback(self, *args):
        self.grid.clear_widgets()
        self.saved_words = saved_words
        self.saved_headwords = saved_headwords
        self.headwords_arr = list(self.saved_headwords)
        self.words_arr = list(self.saved_words)
        self.headwords_arr.sort()
        self.words_arr.sort()
        print(saved_headwords)


        if not self.grid.children:
            for i in self.saved_headwords:
                temp_button = Button(text=str(i), size=(self.grid.width, self.height // 6), background_color=(0.2, 0.8, 0.8, 1), size_hint_y=None)
                temp_button.bind(on_release=self.pressed_button)
                self.grid.add_widget(temp_button)


    # def trig(self, *args):
    #     Clock.schedule_interval(self.my_callback, 2)

    pass


class SavedMeaningWindow(Screen):
    def __init__(self, **kwargs):
        super(SavedMeaningWindow, self).__init__(**kwargs)

    def write_everything(self, *args):
        for i in saved_words:
            if saved_text[0] == i[0]:
                print("nice")
                self.rand_word_label.text = "[color=000000]" + i[0].capitalize() + "[/color]"
                self.rand_mean_label.text = "[color=000000]" + i[1].capitalize() + "[/color]"
                self.verb.text = "[color=000000]" + i[2].capitalize() + "[/color]"
                self.noun.text = "[color=000000]" + i[3].capitalize() + "[/color]"
                self.adj.text = "[color=000000]" + i[4].capitalize() + "[/color]"
                self.adv.text = "[color=000000]" + i[5].capitalize() + "[/color]"

    def delete_everything(self):
        self.rand_word_label.text = ""
        self.rand_mean_label.text = ""
        self.verb.text = ""
        self.noun.text = ""
        self.adj.text = ""
        self.adv.text = ""

    def remove_word(self):
        remove_saved_word(saved_text[0])
        pass

    # def trig(self, *args):
    #     Clock.schedule_interval(self.write_everything, 2)
    pass


class RandomWindow(Screen):
    def __init__(self, **kwargs):
        super(RandomWindow, self).__init__(**kwargs)
        self.wordSet, self.index = select_random_word()

    def display_word(self):
        self.wordSet, self.index = select_random_word()
        self.rand_word_label.text = "[color=000000]" + self.wordSet[0] + "[/color]"
        self.rand_mean_label.text = ""
        self.verb.text = ""
        self.noun.text = ""
        self.adj.text = ""
        self.adv.text = ""

    def display_meaning(self):
        self.rand_mean_label.multiline = True
        self.rand_mean_label.text = "[color=000000]" + self.wordSet[1] + "[/color]"
        if self.wordSet[2].find(" ") != -1:
            self.verb.text = "[color=000000]" + self.wordSet[2].replace(" ", "\n").capitalize() + "[/color]"
        else:
            self.verb.text = "[color=000000]" + self.wordSet[2].capitalize() + "[/color]"
        if self.wordSet[3].find(" ") != -1:
            self.noun.text = "[color=000000]" + self.wordSet[3].replace(" ", "\n").capitalize() + "[/color]"
        else:
            self.noun.text = "[color=000000]" + self.wordSet[3].capitalize() + "[/color]"
        if self.wordSet[4].find(" ") != -1:
            self.adj.text = "[color=000000]" + self.wordSet[4].replace(" ", "\n").capitalize() + "[/color]"
        else:
            self.adj.text = "[color=000000]" + self.wordSet[4].capitalize() + "[/color]"
        if self.wordSet[5].find(" ") != -1:
            self.adv.text = "[color=000000]" + self.wordSet[5].replace(" ", "\n").capitalize() + "[/color]"
        else:
            self.adv.text = "[color=000000]" + self.wordSet[5].capitalize() + "[/color]"

    def save_word(self):
        saved_word_indexes.add(str(self.index))
        save_words()
        print(saved_word_indexes)

    pass


kv = Builder.load_file("wordmemorizer.kv")


class WordMemorizerApp(App):

    def build(self):
        return kv


if __name__ == "__main__":
    WordMemorizerApp().run()
