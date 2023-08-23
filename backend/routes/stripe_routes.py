import os
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
import stripe
import stripe.error
from backend.dependency import auth_dependency
from backend.models.requests import NoterPlan

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
        raise HTTPException(status_code=400, detail='Bad signature')

    if not event:
        raise HTTPException(status_code=400, detail='Event required')
    
    event_type = event['type']

    if event_type in ['customer.subscription.updated', 'customer.subscription.created', 'customer.subscription.deleted']:
        # Data from webhook event
        stripe_customer_id = event['data']['object']['customer']
        subscription_status = event['data']['object']['status']
        has_noter_access = subscription_status == 'active' or subscription_status == 'trialing'

        # Update the database
        async with db.get_session() as session:
            session.query(User).filter(User.stripe_id == stripe_customer_id).update({
                User.has_noter_access: has_noter_access
            })

            session.commit()

        # All set, return 204 No Content
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=501, detail=f"unhandled event: {event['type']}")


@router.post('/stripe/create-checkout-session', include_in_schema=False)
async def create_checkout_session(
    plan: NoterPlan,
    currency: str = 'usd',
    is_auth: Union[bool, dict] = Depends(auth_dependency)
):
    free_trial_subscription_data = {
        'trial_period_days': 7,
        'trial_settings': {
            'end_behavior': {
                'missing_payment_method': 'pause'
            }
        }
    }
    
    session = stripe.checkout.Session.create(
        allow_promotion_codes=True,
        currency=currency ,
        mode='subscription',
        customer=is_auth['stripe_id'],
        customer_update={
            'address': 'auto',
            'name': 'auto',
            'shipping': 'auto'
        },
        billing_address_collection='auto',
        payment_method_collection='if_required',
        success_url=os.environ['LANDING_PAGE_URL'] + '/register?ssid={CHECKOUT_SESSION_ID}',  # {CHECKOUT_SESSION_ID} is replaced with the stripe id, TODO: it is unused as of right now though
        cancel_url=os.environ['LANDING_PAGE_URL'] + '/register',
        automatic_tax={
            'enabled': True
        },
        line_items=[
            {
                'adjustable_quantity': {
                    'enabled': False
                },
                'quantity': 1,
                'price': plan.stripe_price,
            }
        ],
        subscription_data=None if NoterPlan.FREE == plan else free_trial_subscription_data
    )
    
    return {
        'url': session.url,
        'for': is_auth['id']
    }


@router.post('/stripe/create-portal-session', include_in_schema=False)
async def create_portal_session(
    is_auth: Union[bool, dict] = Depends(auth_dependency)
):
    session = stripe.billing_portal.Session.create(
        customer=is_auth['stripe_id'],
        return_url=os.environ['LANDING_PAGE_URL'],
        configuration=os.environ['STRIPE_BILLING_PORTAL_CONFIGURATION']
    )

    return {
        'url': session.url,
        'for': is_auth['id']
    }


@router.get('/stripe/plans', include_in_schema=False)
async def get_plans():
    return {
        'Free': {
            'id': NoterPlan.FREE,
            'price': 'Free',
            'period': None,
            'features': [
                'Take all the notes you want',
                'Note editor',
                'Mobile and Desktop sign in'
            ]
        },
        'Premium Monthly': {
            'id': NoterPlan.PREMIUM_MONTHLY,
            'price': '$6',
            'period': 'month',
            'features': [
                '7 day free trial',
                'Take all the notes you want',
                'Note editor',
                'Mobile and Desktop sign in',
                'Note summarization',
                'One-click study guides',
                'Autonote',
                'Note quizzes',
                'Share with others who have Noter'
            ]
        },
        'Premium Yearly': {
            'id': NoterPlan.PREMIUM_YEARLY,
            'price': '$68',
            'period': 'year',
            'features': [
                '7 day free trial',
                'Take all the notes you want',
                'Premium, world-class editor',
                'Mobile and Desktop sign in',
                'Note summarization',
                'One-click study guides',
                'Autonote',
                'Note quizzes',
                'Share with others who have Noter'
            ]
        }
    }
