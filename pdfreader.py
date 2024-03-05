import pdfplumber
from queue import Queue
from threading import Thread
from transformers import pipeline

# 创建文本概括的pipeline，使用默认的预训练模型
summarizer = pipeline("summarization")

def process_pdf(path, text_queue):
    with pdfplumber.open(path) as pdf:
        text = ""
        for page in pdf.pages:  # 修改为遍历每一页
            text += page.extract_text() + "\n"  # 将所有页面的文本合并
        print(f"Extracted from {path}.")
        text_queue.put(text)  # 将提取的文本放入NLP队列

def process_text(text):
    # 生成文本的概括
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    print(f"Generated summary: {summary[0]['summary_text']}")

def pdf_worker():
    while True:
        pdf_path = pdf_queue.get()
        if pdf_path is None:  # 检查是否收到结束信号
            pdf_queue.task_done()
            break
        process_pdf(pdf_path, text_queue)
        pdf_queue.task_done()

def nlp_worker():
    while True:
        text = text_queue.get()
        if text is None:  # 检查是否收到结束信号
            text_queue.task_done()
            break
        process_text(text)
        text_queue.task_done()

pdf_queue = Queue()
text_queue = Queue()

# 启动PDF处理工作线程
num_pdf_worker_threads = 4
pdf_threads = []
for i in range(num_pdf_worker_threads):
    t = Thread(target=pdf_worker)
    t.start()
    pdf_threads.append(t)

# 启动NLP处理工作线程
num_nlp_worker_threads = 2  # 根据你的系统资源调整线程数量
nlp_threads = []
for i in range(num_nlp_worker_threads):
    t = Thread(target=nlp_worker)
    t.start()
    nlp_threads.append(t)

# 将PDF路径添加到队列中
pdf_paths = ["pdftest1.pdf", "pdftest2.pdf", "pdftest3.pdf"]
for path in pdf_paths:
    pdf_queue.put(path)

pdf_queue.join()  # 等待所有PDF文件处理完成

# 添加结束信号，确保所有PDF处理工作线程都能够正确退出
for i in range(num_pdf_worker_threads):
    pdf_queue.put(None)
for t in pdf_threads:
    t.join()

text_queue.join()  # 等待所有文本处理完成

# 添加结束信号，确保所有NLP处理工作线程都能够正确退出
for i in range(num_nlp_worker_threads):
    text_queue.put(None)
for t in nlp_threads:
    t.join()
