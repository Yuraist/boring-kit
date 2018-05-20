import os
import PyPDF2

# Setup working directories
project_dir = os.path.abspath('temp/project')
en_files_dir = os.path.join(project_dir, 'en')
ru_files_dir = os.path.join(project_dir, 'ru')


def get_texts_from_file(file):
    # Initiate a texts array
    page_texts = []

    # Initiate a reader object
    pdf_reader = PyPDF2.PdfFileReader(file)

    for i in range(pdf_reader.numPages):
        page_object = pdf_reader.getPage(i)
        text = page_object.extractText()
        page_texts.append(text)

    return page_texts


def find_word(word, texts):
    """Searches for the word in texts and returns array of boolean
    """
    pgs = []
    for text in texts:
        text = text.lower()
        if word in text:
            pgs.append(True)
        else:
            pgs.append(False)

    return pgs


def rename_file(file_path, word):
    file = open(file_path, 'rb')
    texts = get_texts_from_file(file)
    pages = find_word(word, texts)
    file.close()

    if True in pages:
        # Create a new file name
        file_name_array = file.name.split('/')
        file_name = word + '_' + file_name_array[-1]
        file_dir = '/'.join(file_name_array[:-1])
        new_name = os.path.join(file_dir, file_name)

        # Rename the file
        os.rename(file_path, new_name)


def find_word_in_directory(word, dir_path):
    # Get a list of files
    files = os.listdir(dir_path)

    # Rename the files
    for file_name in files:
        file_path = os.path.join(dir_path, file_name)

        word_len = len(word) + 1
        if file_name[:word_len] != word + '_':
            print(file_name)
            try:
                rename_file(file_path, word)
            except:
                print('Something wrong')


keywords = ['порог', 'rgb', 'хаф', 'hough']

for keyword in keywords:
    find_word_in_directory(keyword, ru_files_dir)
    find_word_in_directory(keyword, en_files_dir)
