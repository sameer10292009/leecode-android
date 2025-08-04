#!/usr/bin/env python3
"""
Leecode Encoder/Decoder Desktop Application
A standalone offline tool for encoding/decoding text using the Leecode system.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
import pyperclip

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

class LeecodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leecode Encoder/Decoder")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔢 Leecode Encoder/Decoder", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Encoder tab
        encoder_frame = ttk.Frame(notebook, padding="10")
        notebook.add(encoder_frame, text="🔐 Encoder")
        self.setup_encoder_tab(encoder_frame)
        
        # Decoder tab
        decoder_frame = ttk.Frame(notebook, padding="10")
        notebook.add(decoder_frame, text="🔓 Decoder")
        self.setup_decoder_tab(decoder_frame)
        
        # Character reference tab
        reference_frame = ttk.Frame(notebook, padding="10")
        notebook.add(reference_frame, text="📋 Character Reference")
        self.setup_reference_tab(reference_frame)
        
    def setup_encoder_tab(self, parent):
        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Input section
        input_label = ttk.Label(parent, text="Input Text", font=('Arial', 12, 'bold'))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.encode_input = scrolledtext.ScrolledText(parent, height=15, width=40)
        self.encode_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                              padx=(0, 10), pady=(0, 10))
        
        # Encode button
        encode_btn = ttk.Button(parent, text="🔐 Encode Text", command=self.encode_text)
        encode_btn.grid(row=2, column=0, pady=(0, 10))
        
        # Copy input button
        copy_input_btn = ttk.Button(parent, text="📋 Copy Input", 
                                   command=lambda: self.copy_to_clipboard(self.encode_input.get("1.0", tk.END).strip()))
        copy_input_btn.grid(row=3, column=0, pady=(0, 10))
        
        # Output section
        output_label = ttk.Label(parent, text="Encoded Result", font=('Arial', 12, 'bold'))
        output_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        self.encode_output = scrolledtext.ScrolledText(parent, height=15, width=40, state=tk.DISABLED)
        self.encode_output.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Copy output button
        copy_output_btn = ttk.Button(parent, text="📋 Copy Result", command=self.copy_encoded_result)
        copy_output_btn.grid(row=2, column=1, pady=(0, 10))
        
        # Status label
        self.encode_status = ttk.Label(parent, text="", foreground="green")
        self.encode_status.grid(row=3, column=1, pady=(0, 10))
        
    def setup_decoder_tab(self, parent):
        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Input section
        input_label = ttk.Label(parent, text="Input Leecode", font=('Arial', 12, 'bold'))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.decode_input = scrolledtext.ScrolledText(parent, height=15, width=40)
        self.decode_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                              padx=(0, 10), pady=(0, 10))
        
        # Decode button
        decode_btn = ttk.Button(parent, text="🔓 Decode Leecode", command=self.decode_text)
        decode_btn.grid(row=2, column=0, pady=(0, 10))
        
        # Copy input button
        copy_input_btn = ttk.Button(parent, text="📋 Copy Input", 
                                   command=lambda: self.copy_to_clipboard(self.decode_input.get("1.0", tk.END).strip()))
        copy_input_btn.grid(row=3, column=0, pady=(0, 10))
        
        # Output section
        output_label = ttk.Label(parent, text="Decoded Result", font=('Arial', 12, 'bold'))
        output_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        self.decode_output = scrolledtext.ScrolledText(parent, height=15, width=40, state=tk.DISABLED)
        self.decode_output.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Copy output button
        copy_output_btn = ttk.Button(parent, text="📋 Copy Result", command=self.copy_decoded_result)
        copy_output_btn.grid(row=2, column=1, pady=(0, 10))
        
        # Status label
        self.decode_status = ttk.Label(parent, text="", foreground="green")
        self.decode_status.grid(row=3, column=1, pady=(0, 10))
        
    def setup_reference_tab(self, parent):
        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(parent, text="Character to Code Mapping", 
                               font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create treeview for the mapping table
        columns = ('Character', 'Code', 'Description')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # Define headings
        tree.heading('Character', text='Character')
        tree.heading('Code', text='Code')
        tree.heading('Description', text='Description')
        
        # Configure column widths
        tree.column('Character', width=100, anchor=tk.CENTER)
        tree.column('Code', width=80, anchor=tk.CENTER)
        tree.column('Description', width=200, anchor=tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the treeview and scrollbar
        tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Populate the tree with character mappings
        for char, code in sorted(char_to_number.items(), key=lambda x: x[1]):
            description = self.get_char_description(char)
            tree.insert('', tk.END, values=(char, code, description))
            
    def get_char_description(self, char):
        """Get a description for special characters."""
        descriptions = {
            ' ': 'Space',
            '\t': 'Tab',
            '\n': 'Newline',
            '\r': 'Carriage Return',
            '—': 'Em Dash',
            "'": 'Apostrophe',
            '"': 'Quote'
        }
        
        if char in descriptions:
            return descriptions[char]
        elif char.isalpha():
            return f"Letter {char.upper()}" if char.isupper() else f"Letter {char.lower()}"
        elif char.isdigit():
            return f"Digit {char}"
        else:
            return f"Symbol {char}"
            
    def clean_input(self, text):
        """Clean input: collapse multiple spaces."""
        text = re.sub(r' +', ' ', text)
        return text
        
    def encode_text(self):
        """Encode the input text."""
        try:
            input_text = self.encode_input.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("Warning", "Please enter some text to encode.")
                return
                
            cleaned_text = self.clean_input(input_text)
            encoded = ''
            
            for char in cleaned_text:
                if char in char_to_number:
                    encoded += char_to_number[char]
                else:
                    raise ValueError(f"Character '{char}' (Unicode: {ord(char)}) not supported in Leecode mapping.")
            
            # Update output
            self.encode_output.config(state=tk.NORMAL)
            self.encode_output.delete("1.0", tk.END)
            self.encode_output.insert("1.0", encoded)
            self.encode_output.config(state=tk.DISABLED)
            
            # Update status
            self.encode_status.config(text=f"✓ Encoded: {len(input_text)} chars → {len(encoded)} digits", 
                                    foreground="green")
            
        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
            self.encode_status.config(text="✗ Encoding failed", foreground="red")
            
    def decode_text(self):
        """Decode the input Leecode."""
        try:
            input_code = self.decode_input.get("1.0", tk.END).strip()
            if not input_code:
                messagebox.showwarning("Warning", "Please enter a Leecode to decode.")
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
            
            # Update output
            self.decode_output.config(state=tk.NORMAL)
            self.decode_output.delete("1.0", tk.END)
            self.decode_output.insert("1.0", decoded)
            self.decode_output.config(state=tk.DISABLED)
            
            # Update status
            self.decode_status.config(text=f"✓ Decoded: {len(clean_code)} digits → {len(decoded)} chars", 
                                    foreground="green")
            
        except Exception as e:
            messagebox.showerror("Decoding Error", str(e))
            self.decode_status.config(text="✗ Decoding failed", foreground="red")
            
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        except Exception:
            # Fallback: copy to system clipboard using tkinter
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            messagebox.showinfo("Success", "Text copied to clipboard!")
            
    def copy_encoded_result(self):
        """Copy encoded result to clipboard."""
        result = self.encode_output.get("1.0", tk.END).strip()
        if result:
            self.copy_to_clipboard(result)
        else:
            messagebox.showwarning("Warning", "No encoded result to copy.")
            
    def copy_decoded_result(self):
        """Copy decoded result to clipboard."""
        result = self.decode_output.get("1.0", tk.END).strip()
        if result:
            self.copy_to_clipboard(result)
        else:
            messagebox.showwarning("Warning", "No decoded result to copy.")

def main():
    root = tk.Tk()
    app = LeecodeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()