from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from functools import partial
from kivy.core.window import Window

Window.size = (360, 640)

GOREVLER = [f"Gün {i+1}" for i in range(30)]

# ------------------- Öneri Ekranı -------------------
class OneriScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(layout)

        scroll = ScrollView(size_hint=(1, 1))
        container = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        container.bind(minimum_height=container.setter("height"))
        scroll.add_widget(container)
        layout.add_widget(scroll)

        container.add_widget(Label(text="🤖 Ne Yapsam?", font_size=30, size_hint_y=None, height=60))

        self.buton = Button(text="Öneri Ver", size_hint_y=None, height=60)
        self.buton.bind(on_press=self.oneri_ver)
        container.add_widget(self.buton)

        self.sonuc = Label(text="", font_size=18, halign="center", valign="middle", size_hint_y=None, height=100)
        self.sonuc.bind(size=self.sonuc.setter("text_size"))
        container.add_widget(self.sonuc)

    def oneri_ver(self, instance):
        self.sonuc.text = "🎉 Bugün de bir şeyler başarman yeterli! 🙂"

# ------------------- Aylık Plan Ekranı -------------------
class AylikPlanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(layout)

        scroll = ScrollView(size_hint=(1, 1))
        self.container = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.container.bind(minimum_height=self.container.setter('height'))
        scroll.add_widget(self.container)
        layout.add_widget(scroll)

        self.container.add_widget(Label(text="📅 Aylık Görev Planı", font_size=30, size_hint_y=None, height=60))

        self.toggles = []

        for gorev in GOREVLER:
            box = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
            label = Label(text=gorev, halign="left")
            label.bind(size=label.setter("text_size"))
            toggle = Button(text="❌", size_hint=(None, 1), width=50)
            toggle.bind(on_press=partial(self.open_detay, gorev))
            box.add_widget(label)
            box.add_widget(toggle)
            self.container.add_widget(box)
            self.toggles.append(toggle)

    def open_detay(self, gorev, instance):
        app = App.get_running_app()
        detay_screen = app.sm.get_screen("detay")
        detay_screen.set_gorev(gorev, instance)
        app.sm.current = "detay"

# ------------------- Görev Detay Ekranı -------------------
class GorevDetayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(layout)

        # Geri tuşu
        geri_btn = Button(text="⬅ Geri", size_hint_y=None, height=50)
        geri_btn.bind(on_press=self.geri)
        layout.add_widget(geri_btn)

        # Görev başlığı
        self.gorev_label = Label(text="", font_size=24, size_hint_y=None, height=50)
        layout.add_widget(self.gorev_label)

        # Görev detay input
        self.gorev_input = TextInput(hint_text="Görevini buraya yaz...", multiline=True, size_hint=(1,0.5))
        layout.add_widget(self.gorev_input)

        # Tamamla butonu
        self.tamamla_btn = Button(text="✅ Tamamla", size_hint_y=None, height=60)
        self.tamamla_btn.bind(on_press=self.tamamla)
        layout.add_widget(self.tamamla_btn)

        # Tebrik mesajı
        self.tebrik_label = Label(text="", font_size=24, color=(0,1,0,1))
        layout.add_widget(self.tebrik_label)

        self.toggle_btn = None

    def set_gorev(self, gorev, toggle_btn):
        self.gorev_label.text = gorev
        self.gorev_input.text = ""
        self.tebrik_label.text = ""
        self.toggle_btn = toggle_btn

    def geri(self, instance):
        App.get_running_app().sm.current = "aylik"

    def tamamla(self, instance):
        if self.toggle_btn:
            self.toggle_btn.text = "✅"
        self.tebrik_label.text = "🎉 Tebrikler! Görev tamamlandı!"
        # 3 saniye sonra tebrik mesajını sil ve Aylık Plan ekranına dön
        Clock.schedule_once(self.sil_tebrik, 3)
        Clock.schedule_once(self.don_aylik, 3)

    def sil_tebrik(self, dt):
        self.tebrik_label.text = ""

    def don_aylik(self, dt):
        App.get_running_app().sm.current = "aylik"

# ------------------- Ana Uygulama -------------------
class NeYapsamApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")

        # Sekme butonları
        top_box = BoxLayout(size_hint=(1, 0.08))
        root.add_widget(top_box)

        self.sm = ScreenManager(size_hint=(1, 0.92))
        root.add_widget(self.sm)

        self.sm.add_widget(OneriScreen(name="oneriler"))
        self.sm.add_widget(AylikPlanScreen(name="aylik"))
        self.sm.add_widget(GorevDetayScreen(name="detay"))

        btn1 = Button(text="Öneriler")
        btn1.bind(on_press=partial(self.change_screen, "oneriler"))
        top_box.add_widget(btn1)

        btn2 = Button(text="Aylık Plan")
        btn2.bind(on_press=partial(self.change_screen, "aylik"))
        top_box.add_widget(btn2)

        # Sağ üst kapatma tuşu
        kapat_btn = Button(
            text="❌",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"right":1, "top":1}
        )
        kapat_btn.bind(on_press=lambda x: App.get_running_app().stop())
        root.add_widget(kapat_btn)

        return root

    def change_screen(self, screen_name, instance):
        self.sm.current = screen_name


NeYapsamApp().run()
