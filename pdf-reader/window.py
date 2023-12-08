import os.path
import pyperclip

import remi.gui as gui
import pyautogui as pya

from api_requests import Translate_Ru, Paraphraze, Summarize_Ru
from tkinter import filedialog
from tkinter import Tk
from Reader import Reader
from remi import App

text_buffer = ''

__DEFAULT_OUTPUT_STR__ ="PDF текст будет отображаться здесь. " \
                        "Выберите часть текста, с которым вы хотите работать, " \
                        "чтобы скопировать выделенный фрагмент " \
                        "в буффер. Все дальнейшие операции будут происходить с данными, " \
                        "хранящимися в буффере."
__DEFAULT_INPUT_STR__ = "PDF text will be displayed here. " \
                        "Choose text piece you want to operate with " \
                        " to copy it into text buffer. " \
                        "All operations will further be performed " \
                        "with data stored in buffer."

class PDFReader(App):
    def __init__(self, *args):
        super(PDFReader, self).__init__(*args)
        self.button_flag: bool = True
        self.clipboard: str = ""

    def update_text_buffer(self, *args):
        global text_buffer

        pyperclip.copy("")
        pya.hotkey('ctrl', 'c')
        text_buffer = str(pyperclip.paste())
        return pyperclip.paste()



    def print_translate(self, *args):
        global text_buffer
        self.full_text = self.clipboard
        # self.output.set_text(self.clipboard)
        self.output.set_text(Translate_Ru(text_buffer))

    def print_summarize(self, *args):
        global text_buffer

        self.full_text = text_buffer
        self.output.set_text(Summarize_Ru(text_buffer, 0.5))

    def print_paraphraze(self, *args):
        global text_buffer
        self.full_text = text_buffer
        self.output.set_text(Paraphraze(text_buffer))


    def main(self):
        global text_buffer

        pdf_selection_status = 'No PDF selected'
        self.verticalContainer = gui.Container(width=1000,
                                          margin='0px auto',
                                            style={
                                                'display': 'block',
                                                'overflow': 'hidden',
                                                'background': 'linear-gradient(to top, #ffcbbb, #88ff77)'
                                            }
                                         )
        self.horizontalContainer = gui.Container(width='100%',
                                                layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                                margin='0px',
                                                    style={
                                                     'display': 'block',
                                                     'overflow': 'auto'
                                                    }
                                                )
        self.subContainerLeft = gui.Container(width=500,
                                                style={
                                                  'display': 'block',
                                                  'overflow': 'auto',
                                                  'text-align': 'center'
                                                }
                                              )

        text_box_style = {
            'width': '450px',
            'height': '500px',
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

        self.bt_file_choose = gui.Button('Select PDF file', style=pdf_selection_button_style)
        self.bt_translate = gui.Button("Translate", style=button_style)
        self.bt_summarize = gui.Button("Summarize", style=button_style)
        self.bt_paraphraze = gui.Button("Paraphraze", style=button_style)

        top_container.append(self.bt_translate)
        top_container.append(self.bt_paraphraze)
        top_container.append(self.bt_summarize)

        self.bt_file_choose.onclick.do(self.open_file)
        self.bt_translate.onclick.do(self.print_translate)
        self.bt_paraphraze.onclick.do(self.print_paraphraze)
        self.bt_summarize.onclick.do(self.print_summarize)


        self.input = gui.TextInput(style=text_box_style)
        self.input.set_text(__DEFAULT_INPUT_STR__)
        self.input.onmouseup.do(self.update_text_buffer)

        self.output = gui.TextInput(style=text_box_style)
        self.output.set_text(__DEFAULT_OUTPUT_STR__)

        container_style = {
            'width': '500px',
            'display': 'block',
            'overflow': 'auto',
            'text-align': 'center',
            'background': 'linear-gradient(to top, #f8ffbb, #f8c6ff)'
        }

        output_container = gui.Container(
            style=container_style
        )
        input_container = gui.Container(
            style=container_style
        )
        self.link = gui.Link("http://localhost:8081",
                             "A link to here",
                             width=200,
                             height=30,
                             margin='10px')

        output_container.append([self.output])

        input_container.append([self.input])

        bottom_container_style = {
            'width': '1000px',
            'display': 'block',
            'overflow': 'auto',
            'text-align': 'center',
            'background': 'linear-gradient(to top, #ffcbbb, #f8ffbb)'
        }
        down_container = gui.Container(style=bottom_container_style)
        down_container.append([self.bt_file_choose])

        pdf_status_container_style = {
            'width': '1000px',
            'display': 'block',
            'overflow': 'auto',
            'text-align': 'center',
            'background': 'linear-gradient(to top, #ff7777, #ffcbbb)'
        }

        pdf_status_container = gui.Container(style=pdf_status_container_style)
        pdf_status_container.append(self.pdf_status)

        self.horizontalContainer.append([top_container,
                                         input_container,
                                         output_container,
                                         down_container,
                                         pdf_status_container])
        self.verticalContainer.append([self.horizontalContainer])
        return self.verticalContainer

    def open_fileselection_dialog(self):
        self.fileselectionDialog = gui.FileSelectionDialog(
            'File Selection Dialog',
            'Select files and folders',
            False,
            '.')
        self.fileselectionDialog.confirm_value.do(
            self.on_fileselection_dialog_confirm)

        self.fileselectionDialog.show(self)

    def open_file(self, widget):
        root = Tk()
        filepath = filedialog.askopenfilename(
            title='Выбор PDF',
            defaultextension='input',
            initialfile='example.pdf',
            initialdir=os.getcwd()
        )
        root.withdraw()
        if filepath:
            file_downloader = gui.FileDownloader("Download",
                                                 filepath,
                                                 width=250,
                                                 height=30)
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
