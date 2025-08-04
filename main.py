#!/usr/bin/env python3
"""
Leecode Encoder/Decoder Android App
A mobile application for encoding/decoding text using the Leecode system.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import platform
import re

# Import clipboard functionality
try:
    if platform == 'android':
        from android.runnable import run_on_ui_thread
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        ClipData = autoclass('android.content.ClipData')
        ClipboardManager = autoclass('android.content.ClipboardManager')
        Context = autoclass('android.content.Context')
    else:
        # Fallback for desktop testing
        import pyperclip
except ImportError:
    pass

# Mapping dictionary from number strings to characters
number_to_char = {
    '00': 'A', '01': 'B', '02': 'C', '03': 'D', '04': 'E', '05': 'F',
    '06': 'G', '07': 'H', '08': 'I', '09': 'J', '10': 'K', '11': 'L',
    '12': 'M', '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R',
    '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X',
    '24': 'Y', '25': 'Z', '26': 'a', '27': 'b', '28': 'c', '29': 'd',
    '30': 'e', '31': 'f', '32': 'g', '33': 'h', '34': 'i', '35': 'j',
    '36': 'k', '37': 'l', '38': 'm', '39': 'n', '40': 'o', '41': 'p',
    '42': 'q', '43': 'r', '44': 's', '45': 't', '46': 'u', '47': 'v',
    '48': 'w', '49': 'x', '50': 'y', '51': 'z', '52': '0', '53': '1',
    '54': '2', '55': '3', '56': '4', '57': '5', '58': '6', '59': '7',
    '60': '8', '61': '9', '62': '.', '63': ',', '64': '?', '65': '!',
    '66': ';', '67': ':', '68': "'", '69': '"', '70': '-', '71': '—',
    '72': '(', '73': ')', '74': '[', '75': ']', '76': '{', '77': '}',
    '78': '/', '79': '\\', '80': '|', '81': '@', '82': '#', '83': '$',
    '84': '%', '85': '^', '86': '&', '87': '*', '88': '_', '89': '~',
    '90': '`', '91': '<', '92': '>', '93': '=', '94': ' ', '95': '\t',
    '96': '\n', '97': '\r'
}

# Reverse the dictionary for encoding
char_to_number = {v: k for k, v in number_to_char.items()}

class LeecodeApp(App):
    def build(self):
        self.title = "Leecode Encoder/Decoder"
        
        # Main container
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title_label = Label(
            text='[size=24][b]Leecode Encoder/Decoder[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=60
        )
        main_layout.add_widget(title_label)
        
        # Create tabbed panel
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # Encoder tab
        encoder_tab = TabbedPanelItem(text='Encoder')
        encoder_tab.add_widget(self.create_encoder_tab())
        tab_panel.add_widget(encoder_tab)
        
        # Decoder tab
        decoder_tab = TabbedPanelItem(text='Decoder')
        decoder_tab.add_widget(self.create_decoder_tab())
        tab_panel.add_widget(decoder_tab)
        
        # Reference tab
        reference_tab = TabbedPanelItem(text='Reference')
        reference_tab.add_widget(self.create_reference_tab())
        tab_panel.add_widget(reference_tab)
        
        main_layout.add_widget(tab_panel)
        
        return main_layout
    
    def create_encoder_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input section
        input_label = Label(
            text='[b]Enter text to encode:[/b]',
            markup=True,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(input_label)
        
        self.encode_input = TextInput(
            multiline=True,
            hint_text='Type your text here...',
            size_hint_y=0.4
        )
        layout.add_widget(self.encode_input)
        
        # Buttons layout
        button_layout = GridLayout(cols=2, size_hint_y=None, height=50, spacing=10)
        
        encode_btn = Button(text='Encode Text')
        encode_btn.bind(on_press=self.encode_text)
        button_layout.add_widget(encode_btn)
        
        copy_encoded_btn = Button(text='Copy Result')
        copy_encoded_btn.bind(on_press=self.copy_encoded_result)
        button_layout.add_widget(copy_encoded_btn)
        
        layout.add_widget(button_layout)
        
        # Output section
        output_label = Label(
            text='[b]Encoded result:[/b]',
            markup=True,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(output_label)
        
        self.encode_output = TextInput(
            multiline=True,
            readonly=True,
            hint_text='Encoded result will appear here...',
            size_hint_y=0.4
        )
        layout.add_widget(self.encode_output)
        
        # Status label
        self.encode_status = Label(
            text='',
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.encode_status)
        
        return layout
    
    def create_decoder_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input section
        input_label = Label(
            text='[b]Enter Leecode to decode:[/b]',
            markup=True,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(input_label)
        
        self.decode_input = TextInput(
            multiline=True,
            hint_text='Enter numeric code here (e.g., 071430374115408)...',
            size_hint_y=0.4
        )
        layout.add_widget(self.decode_input)
        
        # Buttons layout
        button_layout = GridLayout(cols=2, size_hint_y=None, height=50, spacing=10)
        
        decode_btn = Button(text='Decode Leecode')
        decode_btn.bind(on_press=self.decode_text)
        button_layout.add_widget(decode_btn)
        
        copy_decoded_btn = Button(text='Copy Result')
        copy_decoded_btn.bind(on_press=self.copy_decoded_result)
        button_layout.add_widget(copy_decoded_btn)
        
        layout.add_widget(button_layout)
        
        # Output section
        output_label = Label(
            text='[b]Decoded result:[/b]',
            markup=True,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(output_label)
        
        self.decode_output = TextInput(
            multiline=True,
            readonly=True,
            hint_text='Decoded result will appear here...',
            size_hint_y=0.4
        )
        layout.add_widget(self.decode_output)
        
        # Status label
        self.decode_status = Label(
            text='',
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.decode_status)
        
        return layout
    
    def create_reference_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title_label = Label(
            text='[b]Character Reference[/b]',
            markup=True,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(title_label)
        
        # Create reference text
        reference_text = self.generate_reference_text()
        
        # Scrollable text input for reference
        reference_display = TextInput(
            text=reference_text,
            multiline=True,
            readonly=True,
            font_size=12
        )
        
        scroll_view = ScrollView()
        scroll_view.add_widget(reference_display)
        layout.add_widget(scroll_view)
        
        return layout
    
    def generate_reference_text(self):
        """Generate the character reference text."""
        text = "Character → Code Mapping:\n\n"
        
        # Sort by code for better organization
        sorted_chars = sorted(char_to_number.items(), key=lambda x: x[1])
        
        for char, code in sorted_chars:
            if char == ' ':
                display_char = 'SPACE'
            elif char == '\t':
                display_char = 'TAB'
            elif char == '\n':
                display_char = 'NEWLINE'
            elif char == '\r':
                display_char = 'CARRIAGE RETURN'
            else:
                display_char = char
            
            text += f"{code} → {display_char}\n"
        
        return text
    
    def clean_input(self, text):
        """Clean input: collapse multiple spaces."""
        text = re.sub(r' +', ' ', text)
        return text
    
    def encode_text(self, instance):
        """Encode the input text."""
        try:
            input_text = self.encode_input.text.strip()
            if not input_text:
                self.show_popup("Warning", "Please enter some text to encode.")
                return
            
            cleaned_text = self.clean_input(input_text)
            encoded = ''
            
            for char in cleaned_text:
                if char in char_to_number:
                    encoded += char_to_number[char]
                else:
                    raise ValueError(f"Character '{char}' not supported in Leecode mapping.")
            
            self.encode_output.text = encoded
            self.encode_status.text = f"✓ Encoded: {len(input_text)} chars → {len(encoded)} digits"
            self.encode_status.color = (0, 1, 0, 1)  # Green
            
        except Exception as e:
            self.show_popup("Encoding Error", str(e))
            self.encode_status.text = "✗ Encoding failed"
            self.encode_status.color = (1, 0, 0, 1)  # Red
    
    def decode_text(self, instance):
        """Decode the input Leecode."""
        try:
            input_code = self.decode_input.text.strip()
            if not input_code:
                self.show_popup("Warning", "Please enter a Leecode to decode.")
                return
            
            # Remove any whitespace or non-digit characters
            clean_code = re.sub(r'[^0-9]', '', input_code)
            
            if len(clean_code) % 2 != 0:
                raise ValueError("Encoded string length must be even (pairs of digits).")
            
            decoded = ''
            for i in range(0, len(clean_code), 2):
                part = clean_code[i:i+2]
                if part in number_to_char:
                    decoded += number_to_char[part]
                else:
                    raise ValueError(f"Code '{part}' not found in Leecode mapping.")
            
            self.decode_output.text = decoded
            self.decode_status.text = f"✓ Decoded: {len(clean_code)} digits → {len(decoded)} chars"
            self.decode_status.color = (0, 1, 0, 1)  # Green
            
        except Exception as e:
            self.show_popup("Decoding Error", str(e))
            self.decode_status.text = "✗ Decoding failed"
            self.decode_status.color = (1, 0, 0, 1)  # Red
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            if platform == 'android':
                self.copy_to_android_clipboard(text)
            else:
                # Fallback for desktop testing
                try:
                    pyperclip.copy(text)
                except:
                    pass
            self.show_popup("Success", "Text copied to clipboard!")
        except Exception as e:
            self.show_popup("Error", f"Could not copy to clipboard: {str(e)}")
    
    def copy_to_android_clipboard(self, text):
        """Copy text to Android clipboard."""
        if platform == 'android':
            activity = PythonActivity.mActivity
            clipboard = activity.getSystemService(Context.CLIPBOARD_SERVICE)
            clip = ClipData.newPlainText("Leecode", text)
            clipboard.setPrimaryClip(clip)
    
    def copy_encoded_result(self, instance):
        """Copy encoded result to clipboard."""
        result = self.encode_output.text.strip()
        if result:
            self.copy_to_clipboard(result)
        else:
            self.show_popup("Warning", "No encoded result to copy.")
    
    def copy_decoded_result(self, instance):
        """Copy decoded result to clipboard."""
        result = self.decode_output.text.strip()
        if result:
            self.copy_to_clipboard(result)
        else:
            self.show_popup("Warning", "No decoded result to copy.")
    
    def show_popup(self, title, message):
        """Show a popup message."""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(text=message, text_size=(300, None), halign='center')
        content.add_widget(label)
        
        close_btn = Button(text='OK', size_hint_y=None, height=40)
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    LeecodeApp().run()