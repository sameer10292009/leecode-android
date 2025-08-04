import streamlit as st
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

def clean_input(text):
    """Clean input: collapse multiple spaces."""
    text = re.sub(r' +', ' ', text)
    return text

def encode(text):
    """Encode a string using Leecode format."""
    if not text:
        return ""
    
    text = clean_input(text)
    encoded = ''
    for char in text:
        if char in char_to_number:
            encoded += char_to_number[char]
        else:
            raise ValueError(f"Character '{char}' (Unicode: {ord(char)}) not supported in Leecode mapping.")
    return encoded

def decode(code):
    """Decode a Leecode string (must be even-length)."""
    if not code:
        return ""
    
    # Remove any whitespace or non-digit characters
    code = re.sub(r'[^0-9]', '', code)
    
    if len(code) % 2 != 0:
        raise ValueError("Encoded string length must be even (pairs of digits).")
    
    decoded = ''
    for i in range(0, len(code), 2):
        part = code[i:i+2]
        if part in number_to_char:
            decoded += number_to_char[part]
        else:
            raise ValueError(f"Code '{part}' not found in Leecode mapping.")
    return decoded

def copy_to_clipboard(text, label):
    """Helper function to create a copy button."""
    if st.button(f"📋 Copy {label}", key=f"copy_{label}"):
        try:
            # Fallback method since pyperclip might not work in all environments
            st.code(text, language=None)
            st.success(f"{label} copied to display! Select and copy manually if needed.")
        except Exception as e:
            st.code(text, language=None)
            st.info(f"Manual copy required. {label} displayed above.")

# Streamlit App Configuration
st.set_page_config(
    page_title="Leecode Encoder/Decoder",
    page_icon="🔢",
    layout="wide"
)

# Main App
st.title("🔢 Leecode Encoder/Decoder Tool")
st.markdown("Convert text to numeric codes and vice versa using the Leecode character mapping system.")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🔐 Encoder", "🔓 Decoder", "📋 Character Reference"])

with tab1:
    st.header("Text to Leecode Encoder")
    st.markdown("Enter text below to convert it to Leecode numeric format.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Text")
        input_text = st.text_area(
            "Enter text to encode:",
            height=200,
            placeholder="Type your text here...",
            key="encode_input"
        )
        
        if st.button("🔐 Encode Text", key="encode_btn"):
            if input_text:
                try:
                    encoded_result = encode(input_text)
                    st.session_state.encoded_result = encoded_result
                    st.success("Text encoded successfully!")
                except ValueError as e:
                    st.error(f"Encoding Error: {str(e)}")
                    st.session_state.encoded_result = ""
            else:
                st.warning("Please enter some text to encode.")
                st.session_state.encoded_result = ""
    
    with col2:
        st.subheader("Encoded Result")
        if hasattr(st.session_state, 'encoded_result') and st.session_state.encoded_result:
            st.text_area(
                "Leecode:",
                value=st.session_state.encoded_result,
                height=200,
                disabled=True,
                key="encode_output"
            )
            copy_to_clipboard(st.session_state.encoded_result, "Encoded Text")
            st.info(f"Character count: {len(input_text)} → Code length: {len(st.session_state.encoded_result)}")
        else:
            st.text_area(
                "Leecode:",
                value="",
                height=200,
                disabled=True,
                placeholder="Encoded result will appear here...",
                key="encode_output_empty"
            )

with tab2:
    st.header("Leecode to Text Decoder")
    st.markdown("Enter Leecode numeric format below to convert it back to readable text.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Leecode")
        input_code = st.text_area(
            "Enter Leecode to decode:",
            height=200,
            placeholder="Enter numeric code here (e.g., 071430374115408)",
            key="decode_input"
        )
        
        if st.button("🔓 Decode Leecode", key="decode_btn"):
            if input_code:
                try:
                    decoded_result = decode(input_code)
                    st.session_state.decoded_result = decoded_result
                    st.success("Leecode decoded successfully!")
                except ValueError as e:
                    st.error(f"Decoding Error: {str(e)}")
                    st.session_state.decoded_result = ""
            else:
                st.warning("Please enter a Leecode to decode.")
                st.session_state.decoded_result = ""
    
    with col2:
        st.subheader("Decoded Result")
        if hasattr(st.session_state, 'decoded_result') and st.session_state.decoded_result:
            st.text_area(
                "Decoded Text:",
                value=st.session_state.decoded_result,
                height=200,
                disabled=True,
                key="decode_output"
            )
            copy_to_clipboard(st.session_state.decoded_result, "Decoded Text")
            clean_code = re.sub(r'[^0-9]', '', input_code)
            st.info(f"Code length: {len(clean_code)} → Character count: {len(st.session_state.decoded_result)}")
        else:
            st.text_area(
                "Decoded Text:",
                value="",
                height=200,
                disabled=True,
                placeholder="Decoded result will appear here...",
                key="decode_output_empty"
            )

with tab3:
    st.header("📋 Leecode Character Reference")
    st.markdown("Complete mapping of characters to their corresponding Leecode numeric values.")
    
    # Create columns for better display
    col1, col2, col3, col4 = st.columns(4)
    
    # Split the mapping into chunks for display
    items = list(char_to_number.items())
    chunk_size = len(items) // 4 + 1
    
    columns = [col1, col2, col3, col4]
    
    for i, col in enumerate(columns):
        start_idx = i * chunk_size
        end_idx = min(start_idx + chunk_size, len(items))
        chunk = items[start_idx:end_idx]
        
        with col:
            for char, code in chunk:
                # Handle special characters for display
                display_char = char
                if char == ' ':
                    display_char = '␣ (space)'
                elif char == '\t':
                    display_char = '⇥ (tab)'
                elif char == '\n':
                    display_char = '↵ (newline)'
                elif char == '\r':
                    display_char = '⏎ (carriage return)'
                
                st.text(f"{code} → {display_char}")

# Footer with instructions
st.markdown("---")
st.markdown("""
### How to use:
1. **Encoding**: Enter your text in the Encoder tab and click 'Encode Text'
2. **Decoding**: Enter your Leecode numbers in the Decoder tab and click 'Decode Leecode'
3. **Reference**: Check the Character Reference tab for the complete mapping table

### Notes:
- Leecode uses 2-digit codes (00-97) for each character
- Only characters in the reference table are supported
- Whitespace is automatically cleaned (multiple spaces become single spaces)
- Copy functionality displays the result for manual copying
""")
