import os.path
import pyperclip

import remi.gui as gui
import pyautogui as pya

from api_requests import Translate_Ru, Paraphraze, Summarize_Ru
from tkinter import filedialog
from tkinter import Tk
from Reader import Reader
from remi import App

__DEFAULT_INPUT_STR__ = "PDF text will be displayed here. " \
                        "Choose text piece you want to operate with " \
                        " to copy it into text buffer. " \
                        "All operations will further be performed " \
                        "with data stored in buffer."

__DEFAULT_OUTPUT_STR__ ="PDF текст будет отображаться здесь. " \
                        "Выберите текстовую часть, с которой вы хотите работать, " \
                        "чтобы скопировать его в текстовый буфер. " \
                        "Все операции будут " \
                        "выполнены с данными, хранящимися в буфере."

__DEFAULT_BUFFER_STR__ =   "This is text buffer. Choose the piece " \
                            "of text you want to operate with and put it " \
                            "in this window. Then choose how you want to " \
                            "transform the text using the buttons located above."

class PDFReader(App):
    def __init__(self, *args):
        super(PDFReader, self).__init__(*args)

    def print_translate(self, *args):
        self.output.set_text(Translate_Ru(self.text_buffer.text))

    def print_summarize(self, *args):
        self.output.set_text(Summarize_Ru(self.text_buffer.text, 0.5))

    def print_paraphraze(self, *args):
        self.output.set_text(Paraphraze(self.text_buffer.text))


    def main(self):

        pdf_selection_status = 'No PDF selected'
        self.mainContainer = gui.Container(width=1000,
                                          margin='0px auto',
                                            style={
                                                'display': 'block',
                                                'overflow': 'hidden',
                                                'background': 'linear-gradient(to top, #ffcbbb, #88ff77)'
                                            }
                                         )
        horizontalContainer = gui.Container(width='100%',
                                                layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                                margin='0px',
                                                    style={
                                                     'display': 'block',
                                                     'overflow': 'auto'
                                                    }
                                                )

        pdf_input_text_box_style = {
            'width': '450px',
            'height': '812px',
            'margin': '1px',
            'border': '3px solid #111',
            'background': 'linear-gradient(to top, #edff91, #bbffff)'
        }
        
        buffer_and_output_text_box_style = {
            'width': '450px',
            'height': '400px',
            'margin': '1px',
            'border': '3px solid #111',
            'background': 'linear-gradient(to top, #edff91, #bbffff)'
        }

        self.pdf_status = gui.Label(pdf_selection_status,
                             width=1000,
                             height=30,
                             margin='10px')

        top_container = gui.VBox(width=1000,
                                       height=100,
                                            style={
                                                'display': 'block',
                                                'overflow': 'auto',
                                                'background': 'linear-gradient(to top, #f8c6ff, #bbf4ff)',
                                            }
                                       )

        container_style = {
            'width': '500px',
            'height': '820px',
            'display': 'block',
            'overflow': 'auto',
            'text-align': 'center',
            'background': 'linear-gradient(to top, #f8ffbb, #f8c6ff)'
        }

        output_container = gui.Container(
            style=container_style
        )
        self.input_container = gui.Container(
            style=container_style
        )

        button_style = {
            'margin': '1px',
            'width': '125px',
            'height': '75px',
            'font-size': '150%',
            'background': 'linear-gradient(to top, #f8ffbb, #f8c6ff)',
            'border': '2px solid #111',
            'font-family': 'Impact',
            'color': '#fa8e47',
            'text-align': 'center',
            'vertical-align': 'super'
        }
        pdf_selection_button_style = {
            'margin': '1px',
            'width': '150px',
            'height': '75px',
            'font-size': '200%',
            'background': 'linear-gradient(to top, #f8ffbb, #f8c6ff)',
            'font-family': 'Impact',
            'border': '3px solid #111',
            'color': '#fa8e47',
            'text-align': 'center',
            'vertical-align': 'super'
        }

        bt_file_choose = gui.Button('Select PDF file', style=pdf_selection_button_style)
        bt_translate = gui.Button("Translate", style=button_style)
        bt_summarize = gui.Button("Summarize", style=button_style)
        bt_paraphraze = gui.Button("Paraphraze", style=button_style)

        top_container.append(bt_translate)
        top_container.append(bt_paraphraze)
        top_container.append(bt_summarize)

        bt_file_choose.onclick.do(self.open_file)
        bt_translate.onclick.do(self.print_translate)
        bt_paraphraze.onclick.do(self.print_paraphraze)
        bt_summarize.onclick.do(self.print_summarize)


        self.input = gui.TextInput(style=pdf_input_text_box_style)
        self.input.set_text(__DEFAULT_INPUT_STR__)
        self.input.attributes['readonly'] = 'true'


        self.text_buffer = gui.TextInput(style=buffer_and_output_text_box_style)
        self.text_buffer.set_text(__DEFAULT_BUFFER_STR__)

        self.output = gui.TextInput(style=buffer_and_output_text_box_style)
        self.output.set_text(__DEFAULT_OUTPUT_STR__)

        output_container.append([self.text_buffer, self.output])

        self.input_container.append([self.input])

        bottom_container_style = {
            'width': '1000px',
            'display': 'block',
            'overflow': 'auto',
            'text-align': 'center',
            'background': 'linear-gradient(to top, #ffcbbb, #f8ffbb)'
        }
        bottom_container = gui.Container(style=bottom_container_style)
        bottom_container.append([bt_file_choose])

        pdf_status_container_style = {
            'width': '1000px',
            'display': 'block',
            'overflow': 'auto',
            'text-align': 'center',
            'background': 'linear-gradient(to top, #ff7777, #ffcbbb)'
        }

        pdf_status_container = gui.Container(style=pdf_status_container_style)
        pdf_status_container.append(self.pdf_status)

        horizontalContainer.append([top_container,
                                         self.input_container,
                                         output_container,
                                         bottom_container,
                                         pdf_status_container])
        self.mainContainer.append([horizontalContainer])
        return self.mainContainer


    def open_file(self, *args):
        root = Tk()
        filepath = filedialog.askopenfilename(
            title='Выбор PDF',
            defaultextension='input',
            initivalfile='example.pdf',
            initialdir=os.getcwd()
        )
        root.withdraw()
        if filepath:
            #file_downloader = gui.FileDownloader("Download",
            #                                     filepath,
            #                                     width=250,
            #                                     height=30)
            self.pdf_status.set_text('Current PDF: \n' + filepath)
            text_buf = Reader(filepath).return_pdf_text()
            self.input.set_text(text_buf)

    def on_fileselection_dialog_confirm(self, filelist):
        self.pdf_status.set_text('Current PDF: %s' % ','.join(filelist))
        if len(filelist):
            f = filelist[0]
            file_downloader = gui.FileDownloader("download selected", f, width=200, height=30)
            self.input_container.append(file_downloader, key='file_downloader')
            full_text = Reader(filelist[0]).return_pdf_text()
            self.input.set_text(full_text)

    def on_close(self):
        super(PDFReader, self).on_close()
        os.close(1)
