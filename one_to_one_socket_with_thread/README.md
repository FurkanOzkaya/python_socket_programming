# One to One Socket Chat with Thread Example with Python

## How to Run:
Run server first

```
py server.py
```
Run 2 or more client 

```
py client.py
```

---

## AsycnIO instead Thread 
I prefer to use asyncIO instead thread. Here you can learn what is [AsyncIO](https://furkanozkaya.com/software-languages/asyncio-nedir-nasil-kullanilir/).

I will try to do with asycnIO too check this repo again if there is not.

----

### Note: 

If you want to implement you need to check a lot of things.

Here some of them which I remember:

- Username's must be unique.

- If there is no user in users list we need to warn client about that.

- Disconnect Message, seperator etc. must not be predictable by clients.

...