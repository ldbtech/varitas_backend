from fastapi import FastAPI 

app_auth = FastAPI()

@app_auth.post('/login')
async def login():
    pass

@app_auth.post('/register')
async def register():
    pass

@app_auth.post('/forget_password')
async def forget_password():
    pass

@app_auth.post('/logout')
async def logout():
    pass