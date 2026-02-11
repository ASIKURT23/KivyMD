from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import os

class ASiKuRT_Turbo(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Başlık - aSiKuRT Özel
        layout.add_widget(Label(text="[color=ff4500][b]aSiKuRT TURBO PRO V8[/b][/color]", 
                                markup=True, font_size='26sp'))

        # İşlemler
        options = [
            ("🚀 Full Performans", "settings put global window_animation_scale 0"),
            ("🛡️ Reklamları Kapat", "settings put global private_dns_specifier dns.adguard.com"),
            ("🔋 Pil Tasarrufu", "settings put global low_power 1")
        ]

        for name, cmd in options:
            btn = Button(text=name, size_hint_y=None, height=80)
            btn.bind(on_press=lambda x, c=cmd: os.system(f"su -c '{c}'"))
            layout.add_widget(btn)

        return layout

if __name__ == "__main__":
    ASiKuRT_Turbo().run()
