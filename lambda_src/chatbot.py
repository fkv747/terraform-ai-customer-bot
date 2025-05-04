import boto3
import json
import os
from datetime import datetime
import uuid

# Initialize Bedrock and DynamoDB
bedrock = boto3.client("bedrock-runtime", region_name=os.environ["REGION"])
dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])
TABLE_NAME = "chat_history"

def lambda_handler(event, context):
    try:
        method = event.get("httpMethod", "")
        path = event.get("path", "")

        # === Handle CORS Preflight ===
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": ""
            }

        # === Handle Transcript Download ===
        if method == "GET" and path == "/get-transcript":
            params = event.get("queryStringParameters") or {}
            session_id = params.get("session_id")
            if not session_id:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                        "Access-Control-Allow-Headers": "*",
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": "Missing session_id"})
                }

            table = dynamodb.Table(TABLE_NAME)
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id),
                ScanIndexForward=True
            )
            items = response.get("Items", [])

            transcript_lines = []
            for item in items:
                timestamp = item.get("timestamp", "")
                prompt = item.get("prompt", "")
                reply = item.get("response", "")
                transcript_lines.append(f"[{timestamp}] You: {prompt}")
                transcript_lines.append(f"[{timestamp}] Friday: {reply}")
                transcript_lines.append("")

            transcript_text = "\n".join(transcript_lines)

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Content-Type": "text/plain",
                    "Content-Disposition": f"attachment; filename=chat_transcript_{session_id}.txt"
                },
                "body": transcript_text
            }

        # === Handle POST /chat ===
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "Hello, how can I help you today?")
        session_id = body.get("session_id", str(uuid.uuid4()))
        model_id = os.environ["MODEL_ID"]

        # Get recent chat history
        table = dynamodb.Table(TABLE_NAME)
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(session_id),
            ScanIndexForward=False,
            Limit=5
        )
        history_items = response.get("Items", [])
        history_items.reverse()

        history_lines = []
        for item in history_items:
            history_lines.append(f"User: {item.get('prompt', '')}")
            history_lines.append(f"Friday: {item.get('response', '')}")
        history_text = "\n".join(history_lines)

        # Final prompt format
        prompt = f"""
You are Friday, a smart and witty AI assistant inspired by Tony Stark's personal AI.

Always respond with clarity, charm, and a hint of dry humor. Keep replies helpful and end with a fitting emoji — like 😎 or 🤖.

Conversation History:
{history_text}

New Message:
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

        bedrock_response = bedrock.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(bedrock_response['body'].read())
        ai_reply = response_body.get("results", [{}])[0].get("outputText", "")

        # Save only the clean user input + reply
        table.put_item(
            Item={
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": user_message,
                "response": ai_reply
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "session_id": session_id,
                "prompt": user_message,
                "response": ai_reply
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
