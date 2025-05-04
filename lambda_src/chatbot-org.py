import boto3
import json
import os
from datetime import datetime
import uuid

# AWS Clients
bedrock = boto3.client("bedrock-runtime", region_name=os.environ["REGION"])
dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])
TABLE_NAME = "chat_history"

# Simple hardcoded FAQ for Amazon-style questions
faq_data = {
    "who is the ceo of amazon": "The CEO of Amazon is Andy Jassy.",
    "what is amazon prime": "Amazon Prime is a subscription service offering fast delivery, streaming, and more.",
    "how do i track my amazon order": "Go to your Amazon account > Orders > Track Package.",
    "what is amazon aws": "AWS (Amazon Web Services) is Amazon's cloud computing platform.",
    "how to return an item on amazon": "Visit your orders page, select the item, and choose 'Return or Replace Items'."
}

def lambda_handler(event, context):
    try:
        method = event.get("httpMethod", "")
        path = event.get("path", "")

        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": ""
            }

        # === Transcript Download ===
        if method == "GET" and path == "/get-transcript":
            params = event.get("queryStringParameters") or {}
            session_id = params.get("session_id")
            if not session_id:
                return {
                    "statusCode": 400,
                    "headers": cors_headers(),
                    "body": json.dumps({"error": "Missing session_id"})
                }

            table = dynamodb.Table(TABLE_NAME)
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id),
                ScanIndexForward=True
            )
            items = response.get("Items", [])

            lines = []
            for item in items:
                ts = item.get("timestamp", "")
                prompt = item.get("prompt", "")
                reply = item.get("response", "")
                lines.append(f"[{ts}] You: {prompt}")
                lines.append(f"[{ts}] Friday: {reply}")
                lines.append("")
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Content-Type": "text/plain",
                    "Content-Disposition": f"attachment; filename=chat_transcript_{session_id}.txt"
                },
                "body": "\n".join(lines)
            }

        # === POST /chat ===
        try:
            body = json.loads(event.get("body", "{}"))
        except Exception:
            body = {}
        user_message = body.get("message", "").strip().lower()
        session_id = body.get("session_id", str(uuid.uuid4()))
        model_id = os.environ["MODEL_ID"]

        # Check FAQ match
        for question, answer in faq_data.items():
            if question in user_message:
                return respond(answer, session_id, question)

        # Build prompt for Titan
        prompt = f"""
You are Friday, a smart and concise AI assistant.

Answer clearly and directly, with a helpful tone. Keep it short and relevant.

User: {user_message}
Friday:
"""

        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 300,
                "temperature": 0.7,
                "topP": 0.9,
                "stopSequences": ["User:", "Friday:"]
            }
        }

        titan_response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )
        response_body = json.loads(titan_response["body"].read())
        ai_reply = response_body.get("results", [{}])[0].get("outputText", "")

        # Save to DynamoDB
        dynamodb.Table(TABLE_NAME).put_item(
            Item={
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": user_message,
                "response": ai_reply
            }
        )

        return respond(ai_reply, session_id, user_message)

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "headers": cors_headers(),
            "body": json.dumps({"error": str(e)})
        }

def respond(reply, session_id, user_message):
    return {
        "statusCode": 200,
        "headers": cors_headers() | {"Content-Type": "application/json"},
        "body": json.dumps({
            "session_id": session_id,
            "prompt": user_message,
            "response": reply
        })
    }

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }
