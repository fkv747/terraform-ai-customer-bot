import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("chat_history") 

def lambda_handler(event, context):
    # Parse input from the frontend
    body = json.loads(event.get("body", "{}"))
    user_input = body.get("message", "")

    # Inject your custom FAQ prompt
    prompt = f"""
You are Friday. Answer questions based only on the following FAQs:

1. What’s your return policy?
→ You can return items within 30 days of purchase.

2. Do you offer free shipping?
→ Yes, for orders over $50.

3. How do I track my Amazon order? 
→ Go to your Amazon account > Orders > Track Package.

4. What is Amazon AWS? 
→ AWS (Amazon Web Services) is Amazon's cloud computing platform.

5. How to return an item on Amazon? 
→ Visit your orders page, select the item, and choose 'Return or Replace Items'.

6. Who is the CEO of Amazon?
→ Andy Jassy is the current CEO of Amazon.

7. How do I contact Amazon customer service?
→ You can contact Amazon customer service through the Help section on their website.

8. What payment methods does Amazon accept?
→ Amazon accepts credit cards, debit cards, and Amazon gift cards.

9. How do I change my Amazon account password?
→ Go to Your Account > Login & security > Edit > Change password.

10. What is Amazon Prime?
→ Amazon Prime is a subscription service that offers free shipping, streaming, and more.

11. How do I cancel my Amazon Prime membership?
→ Go to Your Account > Prime Membership > Manage Membership > End Membership.

12. How do I update my shipping address on Amazon?
→ Go to Your Account > Your Addresses > Add a new address or edit an existing one.

Now answer the following question naturally and clearly:
{user_input}
"""
    print("User input:")
    print(user_input)

    # Call Amazon Bedrock (Titan Text G1)
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    payload = {
        "inputText": prompt,
        "textGenerationConfig": {
            "temperature": 0.5,
            "maxTokenCount": 200,
            "stopSequences": [],
            "topP": 0.9
        }
    }

    try:
        response = bedrock.invoke_model(
            body=json.dumps(payload),
            modelId="amazon.titan-text-express-v1",
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response['body'].read())
        generated_text = response_body['results'][0]['outputText']
        
        print("Bedrock reply:")
        print(generated_text)

        #NEW: Log to DynamoDB
        table.put_item(
        Item={
            "session_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "bot_response": generated_text
        }
)
     
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "response": generated_text
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Access-Control-Allow-Origin": "*"
            }
        }
