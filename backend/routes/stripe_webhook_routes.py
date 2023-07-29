import os
from fastapi import APIRouter, HTTPException, Header, Request, Response
import stripe
import stripe.error

from backend.tables import User
from backend.noterdb import db

router = APIRouter()

@router.post('/stripe/hook', include_in_schema=False)
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    data = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=os.environ['STRIPE_ENDPOINT_SECRET']
        )
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    event_data = event['data']

    print(event['type'])

    if event and event['type'] == 'customer.subscription.updated':
        # Data from webhook event
        stripe_customer_id = event['data']['object']['customer']
        subscription_status = event['data']['object']['status']
        has_noter_access = subscription_status == 'active' or subscription_status == 'trialing'
        print(stripe_customer_id, subscription_status, has_noter_access)

        # Update the database
        db.session.query(User).filter(User.stripe_id == stripe_customer_id).update({
            User.has_noter_access: has_noter_access
        })
        db.session.commit()

        # All set, return 204 No Content
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=501, detail=f"unhandled event: {event['type']}")
