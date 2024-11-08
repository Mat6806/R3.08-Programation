'''
import time 
def task(i):
    print(f"task{i}starts")
    time.sleep(1)
    print(f"task{i}ends")

if __name__ == '__main__':
    start = time.perf_counter()
    task(1) 
    task(2)
    end = time.perf_counter()
    print(task(1),task(2))
    '''

#Ex1
import threading
import time
def task(i):
    print(f"task{i}starts")
    time.sleep(1)
    print(f"task{i}ends")

start = time.perf_counter()
for i in range(5):
    t1 = threading.Thread(target=task, args=[1])
    t1.start()
    print("Je suis la thread 1")
    t2 = threading.Thread(target=task, args=[2])
    t2.start()
    print("Je suis la thread 2")
    t1.join() # j'attends la fin de la thread
    t2.join() # j'attends la fin de la thread

end = time.perf_counter()
print(f"Tasks ended in {round(end - start, 2)} second(s)")


#Ex2
import threading
import time

def countdown1(n):
    while n > 0:
        print(f"Thread 1 : {n}")
        n -= 1
        time.sleep(1)

def countdown2(n):
    while n > 0:
        print(f"Thread 2 : {n}")
        n -= 1
        time.sleep(1)

thread1 = threading.Thread(target=countdown1, args=(5,))
thread2 = threading.Thread(target=countdown2, args=(3,))

thread1.start()
time.sleep(0.5)  
thread2.start()

thread1.join()
thread2.join()

#Ex3
import time
import concurrent.futures
import requests
img_urls = [
 'https://cdn.pixabay.com/photo/2016/04/04/14/12/monitor-1307227_1280.jpg',
 'https://cdn.pixabay.com/photo/2018/07/14/11/33/earth-3537401_1280.jpg',
 'https://cdn.pixabay.com/photo/2016/06/09/20/38/woman-1446557_1280.jpg',
]
def download_image(img_url):
 img_bytes = requests.get(img_url).content
 img_name = img_url.split('/')[4]
 with open(img_name, 'wb') as img_file:
    img_file.write(img_bytes)
    print(f"{img_name} was downloaded")
if __name__ == '__main__':
   start = time.perf_counter()
   with concurrent.futures.ThreadPoolExecutor() as executor:
      executor.map(download_image, img_urls)
   end = time.perf_counter()
   print(f"Tasks ended in {round(end - start, 2)} second(s)")

