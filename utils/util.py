from datetime import datetime

def create_token(api_key: str, expiration_time: datetime) -> str:
    
    expiration_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    secret_key = abs(hash(api_key + str(expiration_time)))
    
    return str(secret_key)

def create_api_key(name: str) -> str:
    
    api_key = abs(hash(name)) % 100000000
    if len(str(api_key)) < 4:
        api_key = str(api_key).zfill(9)
    return str(api_key)

if __name__ == "__main__":
    print(create_api_key("John Doe"))