import os

class TextEngine:
    @staticmethod
    def textengine(text):
        # Iterate over the characters in the text
        for i in range(len(text)):
            # Build up the current substring of the text
            current_text = text[:i+1]
            # Clear the console
            os.system('cls')
            # Convert the latest character to uppercase
            latest_char = current_text[-1].upper()
            # Print the current substring with the latest character uppercase
            print(current_text[:-1] + latest_char + current_text[i+1:])