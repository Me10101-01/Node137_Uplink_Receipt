#!/usr/bin/env python3
"""
Universal Identity Donation Protocol (UIDP)
Webhook Handler for Stripe, PayPal, and Cryptocurrency

This module implements the core UIDP functionality for automatic
revenue splitting between DAO operations (93%) and charitable giving (7%).
"""

import hashlib
import hmac
import json
import logging
import os
import time
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UIDPConfig:
    """Configuration for UIDP system"""
    
    # Charitable allocation (immutable from oath)
    CHARITABLE_PERCENTAGE = Decimal('0.07')  # 7%
    
    # Wallet addresses (to be configured)
    DAO_WALLET = os.getenv('DAO_WALLET_ADDRESS', 'dao_wallet_placeholder')
    NONPROFIT_WALLET = os.getenv('NONPROFIT_WALLET_ADDRESS', 'nonprofit_wallet_placeholder')
    
    # Webhook secrets (for signature verification)
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
    PAYPAL_WEBHOOK_ID = os.getenv('PAYPAL_WEBHOOK_ID', '')
    
    # Minimum transaction amount (to avoid micro-transaction issues)
    MINIMUM_AMOUNT = Decimal('1.00')  # $1 USD
    
    # Node identity
    NODE_ID = 'Node137'
    NODE_OPERATOR = 'Domenic Garza'


class TransactionRecord:
    """Record of a UIDP transaction"""
    
    def __init__(
        self,
        source: str,
        source_tx_id: str,
        total_amount: Decimal,
        nonprofit_amount: Decimal,
        dao_amount: Decimal,
        timestamp: float = None
    ):
        self.source = source
        self.source_tx_id = source_tx_id
        self.total_amount = total_amount
        self.nonprofit_amount = nonprofit_amount
        self.dao_amount = dao_amount
        self.timestamp = timestamp or time.time()
        self.nonprofit_tx_id = None
        self.dao_tx_id = None
        self.status = 'pending'
        self.error = None
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for logging"""
        return {
            'source': self.source,
            'source_tx_id': self.source_tx_id,
            'total_amount': str(self.total_amount),
            'nonprofit_amount': str(self.nonprofit_amount),
            'dao_amount': str(self.dao_amount),
            'nonprofit_tx_id': self.nonprofit_tx_id,
            'dao_tx_id': self.dao_tx_id,
            'timestamp': self.timestamp,
            'status': self.status,
            'error': self.error
        }
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of transaction"""
        data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


class UIDPWebhookHandler:
    """Main UIDP webhook handler"""
    
    def __init__(self):
        self.config = UIDPConfig()
        self.transaction_log = []
        
    def calculate_split(self, amount: Decimal) -> Tuple[Decimal, Decimal]:
        """
        Calculate the split between nonprofit and DAO
        
        Returns:
            (nonprofit_amount, dao_amount)
        """
        nonprofit_amount = amount * self.config.CHARITABLE_PERCENTAGE
        dao_amount = amount - nonprofit_amount
        
        # Round to 2 decimal places for currency
        nonprofit_amount = nonprofit_amount.quantize(Decimal('0.01'))
        dao_amount = dao_amount.quantize(Decimal('0.01'))
        
        # Verify total matches (accounting for rounding)
        total_check = nonprofit_amount + dao_amount
        if total_check != amount:
            # Adjust DAO amount for any rounding difference
            dao_amount = amount - nonprofit_amount
            
        return nonprofit_amount, dao_amount
    
    def verify_stripe_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Stripe webhook signature
        
        Args:
            payload: Raw request body
            signature: Stripe-Signature header value
            
        Returns:
            True if signature is valid
        """
        if not self.config.STRIPE_WEBHOOK_SECRET:
            logger.warning("Stripe webhook secret not configured")
            return False
            
        try:
            # Parse signature header
            sig_parts = dict(item.split('=') for item in signature.split(','))
            timestamp = sig_parts.get('t')
            signatures = [sig_parts.get(f'v{i}') for i in range(10) if f'v{i}' in sig_parts]
            
            # Construct signed payload
            signed_payload = f"{timestamp}.{payload.decode()}"
            
            # Calculate expected signature
            expected_sig = hmac.new(
                self.config.STRIPE_WEBHOOK_SECRET.encode(),
                signed_payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            return any(hmac.compare_digest(expected_sig, sig) for sig in signatures if sig)
            
        except Exception as e:
            logger.error(f"Stripe signature verification failed: {e}")
            return False
    
    def handle_stripe_webhook(self, payload: Dict, signature: str = None) -> Dict:
        """
        Handle Stripe webhook event
        
        Args:
            payload: Stripe event data
            signature: Stripe-Signature header (for verification)
            
        Returns:
            Transaction result dictionary
        """
        try:
            # Verify signature if provided
            if signature and not self.verify_stripe_signature(
                json.dumps(payload).encode(), signature
            ):
                raise ValueError("Invalid Stripe signature")
            
            # Extract event type and data
            event_type = payload.get('type')
            
            if event_type == 'payment_intent.succeeded':
                # Extract payment information
                payment_intent = payload['data']['object']
                amount_cents = payment_intent['amount']
                amount = Decimal(amount_cents) / 100  # Convert cents to dollars
                payment_id = payment_intent['id']
                
                logger.info(f"Stripe payment received: ${amount} (ID: {payment_id})")
                
                # Process the split
                return self.split_and_route(
                    amount=amount,
                    source='stripe',
                    source_tx_id=payment_id
                )
            
            else:
                logger.info(f"Ignoring Stripe event type: {event_type}")
                return {'status': 'ignored', 'event_type': event_type}
                
        except Exception as e:
            logger.error(f"Error handling Stripe webhook: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def handle_paypal_webhook(self, payload: Dict) -> Dict:
        """
        Handle PayPal webhook event
        
        Args:
            payload: PayPal event data
            
        Returns:
            Transaction result dictionary
        """
        try:
            event_type = payload.get('event_type')
            
            if event_type == 'PAYMENT.CAPTURE.COMPLETED':
                # Extract payment information
                resource = payload['resource']
                amount = Decimal(resource['amount']['value'])
                payment_id = resource['id']
                
                logger.info(f"PayPal payment received: ${amount} (ID: {payment_id})")
                
                # Process the split
                return self.split_and_route(
                    amount=amount,
                    source='paypal',
                    source_tx_id=payment_id
                )
            
            else:
                logger.info(f"Ignoring PayPal event type: {event_type}")
                return {'status': 'ignored', 'event_type': event_type}
                
        except Exception as e:
            logger.error(f"Error handling PayPal webhook: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def handle_crypto_transaction(self, tx_hash: str, amount: Decimal, currency: str) -> Dict:
        """
        Handle cryptocurrency transaction
        
        Args:
            tx_hash: Transaction hash on blockchain
            amount: Amount received
            currency: Cryptocurrency type (BTC, ETH, etc.)
            
        Returns:
            Transaction result dictionary
        """
        try:
            logger.info(f"Crypto payment received: {amount} {currency} (TX: {tx_hash})")
            
            # Process the split
            return self.split_and_route(
                amount=amount,
                source=f'crypto_{currency.lower()}',
                source_tx_id=tx_hash
            )
            
        except Exception as e:
            logger.error(f"Error handling crypto transaction: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def split_and_route(
        self,
        amount: Decimal,
        source: str,
        source_tx_id: str
    ) -> Dict:
        """
        Core routing logic - splits payment and routes to destinations
        
        This is the heart of the UIDP protocol. The charitable portion
        is routed FIRST to ensure it cannot be bypassed.
        
        Args:
            amount: Total payment amount
            source: Payment source (stripe, paypal, crypto_btc, etc.)
            source_tx_id: Source transaction ID
            
        Returns:
            Dictionary with transaction details
        """
        try:
            # Validate minimum amount
            if amount < self.config.MINIMUM_AMOUNT:
                raise ValueError(f"Amount ${amount} below minimum ${self.config.MINIMUM_AMOUNT}")
            
            # Calculate split
            nonprofit_amount, dao_amount = self.calculate_split(amount)
            
            logger.info(f"Splitting ${amount}: Nonprofit ${nonprofit_amount}, DAO ${dao_amount}")
            
            # Create transaction record
            tx_record = TransactionRecord(
                source=source,
                source_tx_id=source_tx_id,
                total_amount=amount,
                nonprofit_amount=nonprofit_amount,
                dao_amount=dao_amount
            )
            
            # CRITICAL: Route to nonprofit FIRST
            # This ensures charity payment cannot be skipped
            nonprofit_result = self.route_to_nonprofit(nonprofit_amount, tx_record)
            
            if nonprofit_result['status'] != 'success':
                # Nonprofit transfer failed - do NOT proceed to DAO
                tx_record.status = 'failed'
                tx_record.error = f"Nonprofit transfer failed: {nonprofit_result.get('error')}"
                self.transaction_log.append(tx_record)
                
                logger.error(f"Transaction failed: {tx_record.error}")
                
                # In production, this would trigger a refund
                return {
                    'status': 'failed',
                    'error': 'Charitable allocation failed - transaction aborted',
                    'transaction': tx_record.to_dict()
                }
            
            tx_record.nonprofit_tx_id = nonprofit_result['tx_id']
            
            # Only proceed to DAO after nonprofit is confirmed
            dao_result = self.route_to_dao(dao_amount, tx_record)
            
            if dao_result['status'] != 'success':
                # DAO transfer failed but charity succeeded
                # This is acceptable - charity was priority
                tx_record.status = 'partial'
                tx_record.error = f"DAO transfer failed: {dao_result.get('error')}"
                logger.warning(f"DAO transfer failed but charity succeeded: {tx_record.to_dict()}")
            else:
                tx_record.dao_tx_id = dao_result['tx_id']
                tx_record.status = 'success'
            
            # Log transaction
            self.transaction_log.append(tx_record)
            
            # Log to CAT_PUSH system (blockchain)
            self.cat_push_log(tx_record)
            
            logger.info(f"Transaction completed: {tx_record.to_dict()}")
            
            return {
                'status': tx_record.status,
                'transaction': tx_record.to_dict(),
                'hash': tx_record.calculate_hash()
            }
            
        except Exception as e:
            logger.error(f"Error in split_and_route: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def route_to_nonprofit(self, amount: Decimal, tx_record: TransactionRecord) -> Dict:
        """
        Route payment to nonprofit wallet
        
        In production, this would interact with actual payment APIs.
        For now, this is a simulation/stub.
        
        Args:
            amount: Amount to transfer
            tx_record: Transaction record for context
            
        Returns:
            Dictionary with transfer result
        """
        try:
            logger.info(f"Routing ${amount} to nonprofit wallet: {self.config.NONPROFIT_WALLET}")
            
            # In production, this would call:
            # - Stripe Transfer API
            # - PayPal Payouts API
            # - Cryptocurrency wallet transfer
            # - Smart contract function call
            
            # For now, simulate successful transfer
            tx_id = f"nonprofit_{tx_record.source}_{int(time.time())}"
            
            # Simulate transfer delay
            time.sleep(0.1)
            
            logger.info(f"Nonprofit transfer successful: {tx_id}")
            
            return {
                'status': 'success',
                'tx_id': tx_id,
                'amount': str(amount),
                'destination': self.config.NONPROFIT_WALLET
            }
            
        except Exception as e:
            logger.error(f"Nonprofit transfer failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def route_to_dao(self, amount: Decimal, tx_record: TransactionRecord) -> Dict:
        """
        Route payment to DAO wallet
        
        Args:
            amount: Amount to transfer
            tx_record: Transaction record for context
            
        Returns:
            Dictionary with transfer result
        """
        try:
            logger.info(f"Routing ${amount} to DAO wallet: {self.config.DAO_WALLET}")
            
            # In production, this would call actual payment APIs
            tx_id = f"dao_{tx_record.source}_{int(time.time())}"
            
            # Simulate transfer delay
            time.sleep(0.1)
            
            logger.info(f"DAO transfer successful: {tx_id}")
            
            return {
                'status': 'success',
                'tx_id': tx_id,
                'amount': str(amount),
                'destination': self.config.DAO_WALLET
            }
            
        except Exception as e:
            logger.error(f"DAO transfer failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def cat_push_log(self, tx_record: TransactionRecord) -> None:
        """
        Log transaction to CAT_PUSH protocol (blockchain)
        
        This creates an immutable public record of the transaction.
        
        Args:
            tx_record: Transaction to log
        """
        try:
            log_entry = {
                'type': 'uidp_transaction',
                'node_id': self.config.NODE_ID,
                'operator': self.config.NODE_OPERATOR,
                'transaction': tx_record.to_dict(),
                'hash': tx_record.calculate_hash(),
                'timestamp': datetime.utcfromtimestamp(tx_record.timestamp).isoformat()
            }
            
            # In production, this would:
            # 1. Sign with GPG private key
            # 2. Publish to blockchain (Ethereum, Bitcoin via OpenTimestamps)
            # 3. Store in IPFS
            # 4. Archive in Arweave
            
            # For now, log to file
            log_file = '/home/runner/work/Node137_Uplink_Receipt/Node137_Uplink_Receipt/logs/uidp_transactions.jsonl'
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            logger.info(f"Transaction logged to CAT_PUSH: {tx_record.calculate_hash()}")
            
        except Exception as e:
            logger.error(f"Failed to log to CAT_PUSH: {e}")
    
    def get_transaction_history(self, limit: int = 100) -> list:
        """Get recent transaction history"""
        return [tx.to_dict() for tx in self.transaction_log[-limit:]]
    
    def verify_compliance(self, days: int = 30) -> Dict:
        """
        Verify that all recent transactions comply with charitable oath
        
        Args:
            days: Number of days to check
            
        Returns:
            Compliance report
        """
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        recent_txs = [
            tx for tx in self.transaction_log
            if tx.timestamp >= cutoff_time and tx.status == 'success'
        ]
        
        if not recent_txs:
            return {
                'compliant': True,
                'message': 'No transactions in period',
                'period_days': days
            }
        
        total_revenue = sum(tx.total_amount for tx in recent_txs)
        total_charity = sum(tx.nonprofit_amount for tx in recent_txs)
        
        actual_percentage = (total_charity / total_revenue) if total_revenue > 0 else Decimal('0')
        expected_percentage = self.config.CHARITABLE_PERCENTAGE
        
        # Allow 0.1% tolerance for rounding
        tolerance = Decimal('0.001')
        compliant = abs(actual_percentage - expected_percentage) <= tolerance
        
        return {
            'compliant': compliant,
            'period_days': days,
            'total_revenue': str(total_revenue),
            'total_charity': str(total_charity),
            'actual_percentage': f"{float(actual_percentage) * 100:.2f}%",
            'expected_percentage': f"{float(expected_percentage) * 100:.2f}%",
            'transaction_count': len(recent_txs)
        }


def main():
    """Example usage and testing"""
    handler = UIDPWebhookHandler()
    
    print("=" * 60)
    print("UIDP Webhook Handler - Test Mode")
    print("=" * 60)
    print(f"Node ID: {handler.config.NODE_ID}")
    print(f"Charitable Percentage: {float(handler.config.CHARITABLE_PERCENTAGE) * 100}%")
    print(f"DAO Wallet: {handler.config.DAO_WALLET}")
    print(f"Nonprofit Wallet: {handler.config.NONPROFIT_WALLET}")
    print("=" * 60)
    
    # Test transaction
    print("\nSimulating test transaction...")
    result = handler.split_and_route(
        amount=Decimal('100.00'),
        source='test',
        source_tx_id='test_tx_001'
    )
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    # Verify compliance
    print("\nVerifying compliance...")
    compliance = handler.verify_compliance(days=30)
    print(json.dumps(compliance, indent=2))
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
