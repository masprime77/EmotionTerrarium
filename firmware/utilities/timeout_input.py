import threading

def ask_input(answer, prompt=""):
    try:
        answer[0] = input(prompt)
    except:
        pass

def input_with_timeout(prompt="Type something: ",timeout=10, default="DEFAULT"):
    answer = [default]
    thread = threading.Thread(target=ask_input, args=(answer,prompt))
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    return answer[0]