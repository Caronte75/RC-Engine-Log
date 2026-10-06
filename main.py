
import sqlite3
from datetime import date
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen

DB_PATH = Path(App.get_running_app().user_data_dir) / "rc_engine_log.db" if App.get_running_app() else Path("rc_engine_log.db")

KV = r"""
#:import dp kivy.metrics.dp

<LightCard@BoxLayout>:
    padding: dp(14)
    spacing: dp(10)

ScreenManager:
    HomeScreen:
    EngineScreen:
    SessionScreen:

<HomeScreen>:
    name: "home"
    canvas.before:
        Color:
            rgb: .96,.97,.98
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(7)

        BoxLayout:
            size_hint_y: None
            height: dp(66)
            spacing: dp(12)
            Label:
                text: "RC"
                font_size: dp(30)
                bold: True
                color: .08,.48,.82,1
                size_hint_x: None
                width: dp(55)
            BoxLayout:
                orientation: "vertical"
                Label:
                    text: "ENGINE LOG"
                    font_size: dp(22)
                    bold: True
                    color: .07,.12,.18,1
                    halign: "left"
                    text_size: self.size
                Label:
                    text: "Gestione litri motori"
                    font_size: dp(12)
                    color: .35,.40,.45,1
                    halign: "left"
                    text_size: self.size

        Label:
            text: "COME FUNZIONA"
            font_size: dp(14)
            bold: True
            color: .08,.48,.82,1
            size_hint_y: None
            height: dp(24)
            halign: "left"
            text_size: self.size

        Label:
            text: "1. Crea il motore con + NUOVO MOTORE\n2. Apri il motore e registra ogni uscita con + NUOVA SESSIONE\n3. Inserisci pista, litri e note: il totale viene calcolato automaticamente\n4. Puoi modificare o eliminare motori e sessioni in qualsiasi momento"
            font_size: dp(11)
            color: .30,.34,.39,1
            size_hint_y: None
            height: dp(74)
            halign: "left"
            valign: "top"
            text_size: self.width, None

        Label:
            text: "I MIEI MOTORI"
            font_size: dp(18)
            bold: True
            color: .10,.15,.22,1
            size_hint_y: None
            height: dp(30)
            halign: "left"
            text_size: self.size

        ScrollView:
            GridLayout:
                id: engines_box
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                padding: dp(1)
                height: self.minimum_height

        Button:
            text: "+   NUOVO MOTORE"
            size_hint_y: None
            height: dp(50)
            background_normal: ""
            background_color: .08,.48,.82,1
            color: 1,1,1,1
            font_size: dp(15)
            bold: True
            on_release: app.new_engine()

        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(42)
            Label:
                text: "RC Engine Log"
                font_size: dp(11)
                color: .45,.48,.52,1
                size_hint_y: None
                height: dp(18)
            Label:
                text: "Designed by Caruso"
                font_size: dp(10)
                italic: True
                color: .55,.57,.60,1
                size_hint_y: None
                height: dp(18)

<EngineScreen>:
    name: "engine"
    canvas.before:
        Color:
            rgb: .96,.97,.98
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(10)

        BoxLayout:
            size_hint_y: None
            height: dp(55)
            spacing: dp(8)
            Button:
                text: "‹"
                font_size: dp(30)
                size_hint_x: None
                width: dp(55)
                background_normal: ""
                background_color: .88,.91,.94,1
                color: .08,.15,.22,1
                on_release: app.go_home()
            Label:
                text: root.engine_name
                font_size: dp(23)
                bold: True
                color: .07,.12,.18,1
                halign: "left"
                text_size: self.size

        Label:
            text: "LITRI UTILIZZATI"
            font_size: dp(13)
            bold: True
            color: .35,.40,.45,1
            size_hint_y: None
            height: dp(25)

        Label:
            text: root.total_text
            font_size: dp(44)
            bold: True
            color: .08,.48,.82,1
            size_hint_y: None
            height: dp(82)

        Button:
            text: "+   NUOVA SESSIONE"
            size_hint_y: None
            height: dp(54)
            background_normal: ""
            background_color: .08,.48,.82,1
            color: 1,1,1,1
            font_size: dp(16)
            bold: True
            on_release: app.new_session()

        BoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(8)
            Button:
                text: "✎ RINOMINA"
                background_normal: ""
                background_color: .84,.87,.90,1
                color: .08,.15,.22,1
                on_release: app.rename_engine()
            Button:
                text: "🗑 ELIMINA"
                background_normal: ""
                background_color: .94,.82,.82,1
                color: .65,.08,.08,1
                on_release: app.delete_engine()

        Label:
            text: "STORICO SESSIONI"
            font_size: dp(15)
            bold: True
            color: .10,.15,.22,1
            size_hint_y: None
            height: dp(32)
            halign: "left"
            text_size: self.size

        ScrollView:
            GridLayout:
                id: sessions_box
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                padding: dp(1)
                height: self.minimum_height

<SessionScreen>:
    name: "session"
    canvas.before:
        Color:
            rgb: .96,.97,.98
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(12)

        Label:
            id: title
            text: "NUOVA SESSIONE"
            font_size: dp(23)
            bold: True
            color: .07,.12,.18,1
            size_hint_y: None
            height: dp(50)

        TextInput:
            id: session_date
            hint_text: "Data (GG/MM/AAAA)"
            multiline: False
            size_hint_y: None
            height: dp(52)
            background_color: 1,1,1,1
            foreground_color: .08,.12,.18,1
            padding: dp(14)

        TextInput:
            id: track
            hint_text: "Pista"
            multiline: False
            size_hint_y: None
            height: dp(52)
            background_color: 1,1,1,1
            foreground_color: .08,.12,.18,1
            padding: dp(14)

        TextInput:
            id: liters
            hint_text: "Litri utilizzati"
            input_filter: "float"
            multiline: False
            size_hint_y: None
            height: dp(52)
            background_color: 1,1,1,1
            foreground_color: .08,.12,.18,1
            padding: dp(14)

        TextInput:
            id: notes
            hint_text: "Note (facoltative)"
            multiline: True
            background_color: 1,1,1,1
            foreground_color: .08,.12,.18,1
            padding: dp(14)

        BoxLayout:
            size_hint_y: None
            height: dp(54)
            spacing: dp(10)
            Button:
                text: "ANNULLA"
                background_normal: ""
                background_color: .84,.87,.90,1
                color: .08,.15,.22,1
                on_release: app.cancel_session()
            Button:
                text: "SALVA"
                background_normal: ""
                background_color: .08,.48,.82,1
                color: 1,1,1,1
                bold: True
                on_release: app.save_session()
"""

class HomeScreen(Screen):
    pass

class EngineScreen(Screen):
    engine_id = NumericProperty(0)
    engine_name = StringProperty("")
    total_text = StringProperty("0,0 L")

class SessionScreen(Screen):
    default_date = StringProperty("")

class RCEngineLog(App):
    current_engine_id = 0
    editing_session_id = None

    def build(self):
        self.title = "RC Engine Log"
        self.db = None
        Builder.load_string(KV)
        self.open_db()
        return Builder.load_string(KV)

    def on_start(self):
        self.refresh_home()

    def open_db(self):
        db_path = Path(self.user_data_dir) / "rc_engine_log.db"
        self.db = sqlite3.connect(db_path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS engines(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engine_id INTEGER NOT NULL,
            session_date TEXT NOT NULL,
            track TEXT,
            liters REAL NOT NULL,
            notes TEXT,
            FOREIGN KEY(engine_id) REFERENCES engines(id)
        )""")
        self.db.commit()

    def refresh_home(self):
        box = self.root.get_screen("home").ids.engines_box
        box.clear_widgets()
        from kivy.uix.button import Button
        rows = self.db.execute("""
            SELECT e.id, e.name, COALESCE(SUM(s.liters),0)
            FROM engines e LEFT JOIN sessions s ON s.engine_id=e.id
            GROUP BY e.id ORDER BY e.name
        """).fetchall()

        for eid, name, liters in rows:
            b = Button(
                text=f"🔥  {name}\n      {liters:.1f} L",
                size_hint_y=None, height=82,
                background_normal="", background_color=(1,1,1,1),
                color=(.08,.15,.22,1), halign="left"
            )
            b.bind(on_release=lambda _, x=eid: self.open_engine(x))
            box.add_widget(b)


    def new_engine(self):
        from kivy.uix.textinput import TextInput
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout

        inp = TextInput(hint_text="Nome motore", multiline=False)
        ok = Button(text="SALVA", size_hint_y=None, height=50)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        layout.add_widget(inp); layout.add_widget(ok)
        pop = Popup(title="NUOVO MOTORE", content=layout, size_hint=(.85,.35))
        def save(_):
            name = inp.text.strip()
            if name:
                self.db.execute("INSERT INTO engines(name) VALUES(?)", (name,))
                self.db.commit(); pop.dismiss(); self.refresh_home()
        ok.bind(on_release=save)
        pop.open()

    def rename_engine(self):
        from kivy.uix.textinput import TextInput
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout

        row = self.db.execute("SELECT name FROM engines WHERE id=?", (self.current_engine_id,)).fetchone()
        if not row:
            return
        inp = TextInput(text=row[0], multiline=False)
        ok = Button(text="SALVA", size_hint_y=None, height=50,
                    background_normal="", background_color=(.08,.48,.82,1), color=(1,1,1,1))
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        layout.add_widget(inp); layout.add_widget(ok)
        pop = Popup(title="RINOMINA MOTORE", content=layout, size_hint=(.85,.35))
        def save(_):
            name = inp.text.strip()
            if name:
                self.db.execute("UPDATE engines SET name=? WHERE id=?", (name, self.current_engine_id))
                self.db.commit()
                pop.dismiss()
                self.open_engine(self.current_engine_id)
        ok.bind(on_release=save)
        pop.open()

    def delete_engine(self):
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout

        row = self.db.execute("SELECT name FROM engines WHERE id=?", (self.current_engine_id,)).fetchone()
        if not row:
            return
        layout = BoxLayout(orientation="vertical", padding=12, spacing=10)
        msg = Label(text=f"Eliminare '{row[0]}' e tutte le sue sessioni?")
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)
        cancel = Button(text="ANNULLA")
        delete = Button(text="ELIMINA", background_normal="", background_color=(.82,.16,.16,1), color=(1,1,1,1))
        buttons.add_widget(cancel); buttons.add_widget(delete)
        layout.add_widget(msg); layout.add_widget(buttons)
        pop = Popup(title="CONFERMA ELIMINAZIONE", content=layout, size_hint=(.88,.38))
        cancel.bind(on_release=pop.dismiss)
        def do_delete(_):
            self.db.execute("DELETE FROM sessions WHERE engine_id=?", (self.current_engine_id,))
            self.db.execute("DELETE FROM engines WHERE id=?", (self.current_engine_id,))
            self.db.commit()
            pop.dismiss()
            self.go_home()
        delete.bind(on_release=do_delete)
        pop.open()

    def delete_session(self, sid):
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout

        layout = BoxLayout(orientation="vertical", padding=12, spacing=10)
        layout.add_widget(Label(text="Vuoi eliminare questa sessione?"))
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)
        cancel = Button(text="ANNULLA")
        delete = Button(text="ELIMINA", background_normal="", background_color=(.82,.16,.16,1), color=(1,1,1,1))
        buttons.add_widget(cancel); buttons.add_widget(delete)
        layout.add_widget(buttons)
        pop = Popup(title="CONFERMA", content=layout, size_hint=(.82,.32))
        cancel.bind(on_release=pop.dismiss)
        def do_delete(_):
            self.db.execute("DELETE FROM sessions WHERE id=?", (sid,))
            self.db.commit()
            pop.dismiss()
            self.refresh_engine()
        delete.bind(on_release=do_delete)
        pop.open()

    def open_engine(self, engine_id):
        row = self.db.execute("SELECT name FROM engines WHERE id=?", (engine_id,)).fetchone()
        if not row: return
        self.current_engine_id = engine_id
        screen = self.root.get_screen("engine")
        screen.engine_id = engine_id
        screen.engine_name = row[0]
        self.refresh_engine()
        self.root.current = "engine"

    def refresh_engine(self):
        screen = self.root.get_screen("engine")
        total = self.db.execute("SELECT COALESCE(SUM(liters),0) FROM sessions WHERE engine_id=?", (self.current_engine_id,)).fetchone()[0]
        count = self.db.execute("SELECT COUNT(*) FROM sessions WHERE engine_id=?", (self.current_engine_id,)).fetchone()[0]
        screen.total_text = f"{total:.1f} L\n{count} SESSIONI"
        box = screen.ids.sessions_box
        box.clear_widgets()
        from kivy.uix.button import Button
        rows = self.db.execute("""
            SELECT id, session_date, track, liters, notes
            FROM sessions WHERE engine_id=? ORDER BY id DESC
        """, (self.current_engine_id,)).fetchall()
        for sid, d, track, liters, notes in rows:
            text = f"{d}  •  {track or '-'}  •  {liters:.1f} L"
            if notes: text += f"\n{notes}"
            from kivy.uix.boxlayout import BoxLayout
            rowbox = BoxLayout(size_hint_y=None, height=82, spacing=6)
            b = Button(text=text + "\n✎ MODIFICA",
                       background_normal="", background_color=(1,1,1,1),
                       color=(.08,.15,.22,1), halign="left")
            b.bind(on_release=lambda _, x=sid: self.edit_session(x))
            d = Button(text="🗑", size_hint_x=None, width=55,
                       background_normal="", background_color=(.94,.82,.82,1),
                       color=(.65,.08,.08,1))
            d.bind(on_release=lambda _, x=sid: self.delete_session(x))
            rowbox.add_widget(b)
            rowbox.add_widget(d)
            box.add_widget(rowbox)

    def new_session(self):
        self.editing_session_id = None
        s = self.root.get_screen("session")
        s.ids.title.text = "NUOVA SESSIONE"
        s.ids.session_date.text = date.today().strftime("%d/%m/%Y")
        s.ids.track.text = ""; s.ids.liters.text = ""; s.ids.notes.text = ""
        self.root.current = "session"

    def edit_session(self, sid):
        row = self.db.execute("""
            SELECT session_date, track, liters, notes FROM sessions WHERE id=?
        """, (sid,)).fetchone()
        if not row: return
        self.editing_session_id = sid
        s = self.root.get_screen("session")
        s.ids.title.text = "MODIFICA SESSIONE"
        s.ids.session_date.text, s.ids.track.text, s.ids.liters.text, s.ids.notes.text = str(row[0]), row[1] or "", str(row[2]), row[3] or ""
        self.root.current = "session"

    def save_session(self):
        s = self.root.get_screen("session")
        try: liters = float(s.ids.liters.text.replace(",", "."))
        except: return
        d = s.ids.session_date.text.strip()
        track = s.ids.track.text.strip()
        notes = s.ids.notes.text.strip()
        if not d or liters < 0: return
        if self.editing_session_id:
            self.db.execute("""UPDATE sessions SET session_date=?, track=?, liters=?, notes=? WHERE id=?""",
                            (d, track, liters, notes, self.editing_session_id))
        else:
            self.db.execute("""INSERT INTO sessions(engine_id,session_date,track,liters,notes) VALUES(?,?,?,?,?)""",
                            (self.current_engine_id,d,track,liters,notes))
        self.db.commit()
        self.editing_session_id = None
        self.refresh_engine()
        self.root.current = "engine"

    def cancel_session(self):
        self.editing_session_id = None
        self.root.current = "engine"

    def go_home(self):
        self.refresh_home()
        self.root.current = "home"

if __name__ == "__main__":
    RCEngineLog().run()
