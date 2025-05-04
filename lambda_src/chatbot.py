import boto3
import json
import os
from datetime import datetime
import uuid

# Bedrock and DynamoDB setup
bedrock = boto3.client("bedrock-runtime", region_name=os.environ["REGION"])
dynamodb = boto3.resource("dynamodb", region_name=os.environ["REGION"])

TABLE_NAME = "chat_history"

def lambda_handler(event, context):
    try:
        print("Event Received:", event)
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "Hello, how can I help you today?")
        model_id = os.environ["MODEL_ID"]

        # === Prompt with Friday Persona ===
        prompt = f"""
You are Friday, a smart and witty AI assistant inspired by Tony Stark's personal AI.

Always respond with clarity, charm, and a hint of dry humor. Keep replies helpful and end with a fitting emoji — like 😎 or 🤖.

User said: {user_message}
Your response:
"""

        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 300,
                "temperature": 0.7,
                "topP": 0.9
            }
        }

        response = bedrock.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response['body'].read())
        ai_reply = response_body.get("results", [{}])[0].get("outputText", "")

        # Save to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                "session_id": body.get("session_id", str(uuid.uuid4())),
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": prompt,
                "response": ai_reply
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "prompt": prompt,
                "response": ai_reply
            })
        }

    except KeyError as e:
        print("KeyError:", str(e))
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing key: {str(e)}"})
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
