# One to One Socket Chat with AsyncIO Example with Python

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


### Note: 

If you want to implement you need to check a lot of things.

Here some of them which I remember:

- Username's must be unique.

- If there is no user in users list we need to warn client about that.

- Disconnect Message, seperator etc. must not be predictable by clients.

...