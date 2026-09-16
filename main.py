import os
import google.generativeai as genai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock

# Configuration de l'API Gemini
API_KEY = "VOTRE_CLE_API_ICI"
genai.configure(api_key=API_KEY)

model_name = "models/gemini-3.6-flash"
system_instruction = (
    "Tu t'appelles Annaelle. Tu es une professeure et assistante juridique "
    "experte en droit de la RDC. Tu t'adresses à Manassé en l'appelant par son prénom. "
    "Sois claire, rigoureuse et chaleureuse."
)

class AnnaelleAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super(AnnaelleAppUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Initialisation du modèle Gemini
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat()

        # Zone d'affichage des messages (Scrollable)
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.message_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))
        self.scroll.add_widget(self.message_layout)
        self.add_widget(self.scroll)

        # Layout pour la saisie et le bouton
        input_layout = BoxLayout(size_hint=(1, 0.15), spacing=5)
        
        self.text_input = TextInput(
            hint_text="Pose ta question juridique à Annaelle...",
            size_hint=(0.8, 1),
            multiline=False
        )
        self.text_input.bind(on_text_validate=self.envoyer_message)
        input_layout.add_widget(self.text_input)

        send_button = Button(
            text="Envoyer",
            size_hint=(0.2, 1),
            background_color=(0.1, 0.5, 0.8, 1)
        )
        send_button.bind(on_press=self.envoyer_message)
        input_layout.add_widget(send_button)

        self.add_widget(input_layout)

        # Message d'accueil initial
        self.ajouter_message("Annaelle", "Bonjour Manassé ! Je suis Annaelle, ton assistante juridique. De quoi veux-tu qu'on discute aujourd'hui ?")

    def ajouter_message(self, auteur, texte):
        msg_label = Label(
            text=f"[b]{auteur}[/b] : {texte}",
            size_hint_y=None,
            text_size=(self.width - 20, None),
            markup=True
        )
        msg_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.message_layout.add_widget(msg_label)
        # Faire défiler vers le bas automatiquement
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def envoyer_message(self, instance):
        texte_utilisateur = self.text_input.text.strip()
        if not texte_utilisateur:
            return

        self.ajouter_message("Manassé", texte_utilisateur)
        self.text_input.text = ""

        try:
            response = self.chat.send_message(texte_utilisateur)
            self.ajouter_message("Annaelle", response.text)
        except Exception as e:
            self.ajouter_message("Erreur", str(e))

class AnnaelleApp(App):
    def build(self):
        self.title = "Annaelle - Assistant Juridique RDC"
        return AnnaelleAppUI()

if __name__ == '__main__':
    AnnaelleApp().run()
      
