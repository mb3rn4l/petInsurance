import time
from .models import Claim

def process_claim_async(claim_id):
    """
    Simulated task to process the claim in the background.
    Change the status from PROCESSING to IN_REVIEW after a delay.
    """
    time.sleep(3)
    try:
        claim = Claim.objects.get(id=claim_id)
        if claim.status == 'PROCESSING':
            claim.status = 'IN_REVIEW'
            claim.save()
            print(f"Claim #{claim_id} processed: Changed to IN_REVIEW")
    except Exception as e:
        print(f"Error processing claim #{claim_id}: {str(e)}")