from src.utils.requestor import Requestor

if __name__ == "__main__":
    requestor = Requestor('http://127.0.0.1:8080')

    for i in range(1000):
        requestor.join()
