from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
import os

try:
	from urllib.request import urlretrieve
except ImportError:
	from urllib import urlretrieve
import re


class DButton(Button):
	def __init__(self, text, link, **kwargs):
		self.text = text
		self.link = link
		super(DButton, self).__init__(**kwargs)

	def on_press(self):
		download(self.text, self.link)


class GLayout(GridLayout):
	def __init__(self, **kwargs):
		super(GLayout, self).__init__(**kwargs)
		self.bind(minimum_height=self.setter('height'))
		self.label = Label(text=os.path.dirname(os.path.realpath(__file__)))
		self.add_widget(self.label)
		try:
			page = UrlRequest('http://192.168.2.107:8000/')
			page.wait()
			print(page.result)
		except Exception:
			self.label.text = "Can't access the server."
		if 'page' in locals():
			table = page.result[235:]
			line = re.findall(r'<tr>(.*?)</tr>', table)
			for i in line:
				data = re.findall(r'<td><a href="(.*?)">(.*?)</a> </td><td>(.*?)</td>', i)
				print(data)
				self.add_widget(DButton(data[0][1], data[0][0]))


class Screen(ScrollView):
	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)


class MusicClientApp(App):
	def build(self):
		self.load_kv("main.kv")
		return Screen()


def download(name, link):
	url = 'http://192.168.2.107:8000/' + link
	dir = os.path.dirname(os.path.realpath(__file__))
	urlretrieve(url, name)
	os.rename(dir + "/" + name, '/storage/3463-3632/Music/' + name)
	content = Button(text=name + ' successfully downloaded.')
	popup = Popup(content=content, auto_dismiss=False)
	content.bind(on_press=popup.dismiss)
	popup.open()

if __name__ == "__main__":
	MusicClientApp().run()
