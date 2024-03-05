from flask import Flask, request, jsonify
import threading
import pdfplumber
from queue import Queue
from transformers import pipeline
from threading import Thread

from PDFanalyzer.pdfreader import pdf_threads, nlp_threads

app = Flask(__name__)
summarizer = pipeline("summarization")
pdf_queue = Queue()
text_queue = Queue()
def process_text(text):
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']


def pdf_worker():
    while True:
        task = pdf_queue.get()
        if task is None:
            pdf_queue.task_done()
            break
        path, callback = task
        with pdfplumber.open(path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        pdf_queue.task_done()
        summary = process_text(text)
        text_queue.put((callback, summary))


def nlp_worker():
    while True:
        task = text_queue.get()
        if task is None:
            text_queue.task_done()
            break
        callback, summary = task
        callback(summary)
        text_queue.task_done()


def start_workers():
    for _ in range(4):
        t = Thread(target=pdf_worker)
        t.start()

    for _ in range(2):
        t = Thread(target=nlp_worker)
        t.start()


start_workers()


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    pdf_paths = data.get('pdf_paths', [])

    results = []

    def collect_result(summary):
        results.append(summary)

    for path in pdf_paths:
        pdf_queue.put((path, collect_result))

    pdf_queue.join()
    text_queue.join()

    for _ in range(len(pdf_threads) + len(nlp_threads)):
        pdf_queue.put(None)
        text_queue.put(None)

    return jsonify({"summaries": results})


if __name__ == '__main__':
    app.run(debug=True)
