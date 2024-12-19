import logging
import jwt
import datetime
import azure.functions as func

SECRET_KEY = "your_secret_key"

def public(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing GenerateJWT request.")

    try:
        # リクエストボディを取得
        req_body = req.get_json()
        payload = req_body.get("payload", {})
        
        if not payload:
            return func.HttpResponse("Payload is missing", status_code=400)

        # 有効期限を設定
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        # JWTを生成
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        # トークンをレスポンスとして返す
        return func.HttpResponse(token, status_code=200)

    except Exception as e:
        logging.error(f"Error generating JWT: {str(e)}")
        return func.HttpResponse("Error generating JWT", status_code=500)