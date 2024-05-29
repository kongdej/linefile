### Installation
- Update LINE Message API webhook URL
```
    ex: https://9086-1-46-203-66.ngrok-free.app/webhook
```
- Update LINE LIFF endpoint URL
```
    ex: https://9086-1-46-203-66.ngrok-free.app/liff
```
- Update /liff/index.html
```
    const webhookUrl = "https://9086-1-46-203-66.ngrok-free.app/"  //<-- webhook
    const liffId = "1654109634-mOJGk7bV" //<-- Liff Id
```   

- Update docker-compose.yml
```
    LINE_CHANNEL_SECRET: "xxxx"
    LINE_CHANNEL_TOKEN: "xxxxxxxxxxx"
    HOST_URL: "https://liff.line.me/1654109634-mOJGk7bV"
```
- Manual start server on line container
 ```
> uvicorn app.main:app --reload --host=0.0.0.0 
 ```

- Auto start uncomment last line of Dockerfile


### Build documents
- upload document to /documents


```
> python addpdf.py
```
- output directory is /public