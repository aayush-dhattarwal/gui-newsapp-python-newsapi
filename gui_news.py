import io
import webbrowser
from tkinter import *
from urllib.request import urlopen
import requests
from PIL import ImageTk, Image


class GuiNews:

    def __init__(self):

        # Fetching API data
        self.data = requests.get(
            'https://newsapi.org/v2/top-headlines?country=in&apiKey=1c468d8ea9b54fd48f99d60030708170').json()
        # Load GUI
        self.load_gui()
        # loading the first article
        self.load_news_item(0)

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.title('AD News Feed')
        self.root.configure(background='#040c1a')

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):

        # clear the screen for the new news item
        self.clear()

        # Load image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo)
        label.pack()

        # News Heading
        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='#040c1a', fg='white', wraplength=350,
                        justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('helvetica', 15))

        # News Details
        details = Label(self.root, text=self.data['articles'][index]['description'], bg='#040c1a', fg='white',
                        wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        # Buttons in frame
        frame = Frame(self.root, bg='#040c1a')
        frame.pack(expand=True, fill=BOTH)
        # Previous Button
        if index != 0:
            prev = Button(frame, text='Prev', width=16, height=3, command=lambda: self.load_news_item(index - 1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=16, height=3,
                      command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)
        # Next Button
        if index != len(self.data['articles']) - 1:
            next = Button(frame, text='Next', width=16, height=3, command=lambda: self.load_news_item(index + 1))
            next.pack(side=LEFT)

        self.root.mainloop()
    # Open in Browser to read more
    def open_link(self, url):
        webbrowser.open(url)


obj = GuiNews()
