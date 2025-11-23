# Universal Identity Donation Protocol (UIDP)

## Overview

The Universal Identity Donation Protocol (UIDP) is a self-enforcing charitable distribution system that automatically routes a predetermined percentage of revenue to charitable organizations. The system is designed to make charitable giving **mandatory at the protocol level** rather than discretionary at the governance level.

## Key Features

### 1. **Mandatory Charity Allocation**
- 7% of all revenue automatically routed to ValorYield Engine (501(c)(3) pending)
- Charitable portion transferred FIRST - if it fails, entire transaction is aborted
- No human discretion or override capability
- Enforced by code, not governance

### 2. **Multi-Platform Support**
- **Stripe:** Credit card and ACH payments
- **PayPal:** Traditional online payments
- **Cryptocurrency:** Bitcoin, Ethereum, and other blockchains
- **Smart Contracts:** On-chain enforcement for crypto payments

### 3. **NFT Donation Receipts**
- Every donation generates an NFT receipt
- Immutable proof of charitable contribution
- Tax deduction documentation
- Tradeable/transferrable proof of impact

### 4. **Transparency & Verification**
- All transactions logged to blockchain via CAT_PUSH protocol
- Public audit trail on IPFS and Arweave
- Real-time compliance verification
- Anyone can verify charitable allocations

## Architecture

```
Payment Source (Stripe/PayPal/Crypto)
    ↓
UIDP Webhook Handler
    ↓
Amount Splitter (93% / 7%)
    ↓
    ├→ Nonprofit Wallet (7%) [PRIORITY]
    └→ DAO Wallet (93%) [ONLY AFTER NONPROFIT SUCCEEDS]
    ↓
CAT_PUSH Transaction Log
    ↓
Blockchain + IPFS + Arweave
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file:
```bash
# Wallet Addresses
DAO_WALLET_ADDRESS=your_dao_wallet_address
NONPROFIT_WALLET_ADDRESS=your_nonprofit_wallet_address

# Webhook Secrets (for signature verification)
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_secret
PAYPAL_WEBHOOK_ID=your_paypal_webhook_id

# Optional: Blockchain RPC endpoints
ETH_RPC_URL=https://mainnet.infura.io/v3/your_key
BTC_RPC_URL=https://your_btc_node
```

## Usage

### Running the Webhook Handler

#### Test Mode
```bash
python3 uidp/webhook_handler.py
```

#### Production Server
```bash
# Using Flask (example)
python3 uidp/server.py

# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 uidp.server:app
```

### Processing Payments

#### Stripe Webhook
```python
from uidp.webhook_handler import UIDPWebhookHandler

handler = UIDPWebhookHandler()

# In your webhook endpoint
@app.post('/webhooks/stripe')
def stripe_webhook():
    payload = request.get_data()
    signature = request.headers.get('Stripe-Signature')
    
    event = json.loads(payload)
    result = handler.handle_stripe_webhook(event, signature)
    
    return jsonify(result)
```

#### PayPal Webhook
```python
@app.post('/webhooks/paypal')
def paypal_webhook():
    payload = request.get_json()
    result = handler.handle_paypal_webhook(payload)
    return jsonify(result)
```

#### Cryptocurrency Transaction
```python
# Monitor blockchain for incoming transactions
def process_crypto_tx(tx_hash, amount, currency):
    result = handler.handle_crypto_transaction(tx_hash, amount, currency)
    return result
```

### Minting NFT Receipts

```python
from uidp.nft_receipt import NFTReceiptMinter

minter = NFTReceiptMinter(node_id="Node137")

# Mint a receipt
receipt = minter.mint_receipt(
    total_amount=Decimal('100.00'),
    nonprofit_amount=Decimal('7.00'),
    beneficiary='ValorYield Engine',
    donor_address='0x1234...',
    transaction_hash='0xabcd...'
)

# Upload to IPFS
ipfs_uri = minter.upload_to_ipfs(receipt)

# Mint NFT on blockchain
nft_result = minter.mint_nft_on_chain(
    receipt=receipt,
    contract_address='0xNFTContract...',
    donor_wallet='0x1234...'
)

print(f"NFT minted: Token ID {nft_result['token_id']}")
```

### Verifying Compliance

```python
# Check compliance over last 30 days
compliance = handler.verify_compliance(days=30)

print(f"Compliant: {compliance['compliant']}")
print(f"Total Revenue: {compliance['total_revenue']}")
print(f"Total Charity: {compliance['total_charity']}")
print(f"Percentage: {compliance['actual_percentage']}")
```

## How It Works

### 1. Payment Receipt
When a payment is received via any integrated platform (Stripe, PayPal, crypto), the UIDP webhook handler is notified.

### 2. Automatic Splitting
The system automatically calculates:
- **Nonprofit amount:** 7% of total
- **DAO amount:** 93% of total

### 3. Priority Routing
**Critical:** The nonprofit receives funds FIRST:
```python
# Nonprofit transfer MUST succeed
nonprofit_result = route_to_nonprofit(nonprofit_amount)

if nonprofit_result['status'] != 'success':
    # ABORT entire transaction
    # In production, this triggers a refund
    return {'status': 'failed', 'error': 'Charity allocation failed'}

# Only proceed to DAO after nonprofit is confirmed
dao_result = route_to_dao(dao_amount)
```

### 4. Immutable Logging
Every transaction is logged to:
- **Blockchain:** Via OpenTimestamps or direct smart contract event
- **IPFS:** Decentralized storage
- **Arweave:** Permanent archival
- **Local Log:** For immediate access

### 5. NFT Receipt Generation
An NFT is optionally minted containing:
- Total transaction amount
- Charitable amount
- Beneficiary organization
- Timestamp and verification hash
- Metadata for tax deduction

## Security

### Signature Verification
All webhooks are verified using cryptographic signatures:

**Stripe:**
```python
verified = verify_stripe_signature(payload, signature, secret)
if not verified:
    return {'status': 'error', 'error': 'Invalid signature'}
```

**PayPal:**
```python
# PayPal provides webhook signature verification
# Implementation follows PayPal security best practices
```

### Transaction Integrity
- All amounts use `Decimal` type to avoid floating-point errors
- Cryptographic hashing of all transaction records
- GPG signing of CAT_PUSH logs
- Immutable blockchain storage

### Failure Handling
- If nonprofit transfer fails → entire transaction aborted
- If DAO transfer fails → nonprofit keeps funds (charity is priority)
- All failures logged for manual review
- Automatic retry mechanisms (configurable)

## Compliance Verification

### Automated Checks
The system automatically verifies:
- ✓ Charitable percentage matches oath specification (7%)
- ✓ All transactions properly logged
- ✓ No gaps in transaction chain
- ✓ Cryptographic signatures valid
- ✓ Blockchain records match internal records

### Manual Verification
Anyone can verify compliance by:
1. Querying blockchain transaction logs
2. Checking IPFS/Arweave archives
3. Running compliance verification script
4. Reviewing public transparency reports

### Example Compliance Check
```bash
# Run compliance verification
python3 uidp/verify_compliance.py --days 30

# Output:
# ✓ Compliant: Yes
# ✓ Total Revenue: $10,000.00
# ✓ Total Charity: $700.00
# ✓ Percentage: 7.00%
# ✓ Transactions: 42
# ✓ All blockchain records verified
```

## Testing

### Unit Tests
```bash
# Run all tests
python3 -m pytest uidp/tests/

# Run specific test
python3 -m pytest uidp/tests/test_webhook_handler.py
```

### Integration Tests
```bash
# Test with Stripe test mode
STRIPE_TEST_MODE=1 python3 uidp/tests/test_stripe_integration.py

# Test with PayPal sandbox
PAYPAL_SANDBOX=1 python3 uidp/tests/test_paypal_integration.py
```

### Manual Testing
```bash
# Run webhook handler in test mode
python3 uidp/webhook_handler.py

# Simulate a payment
curl -X POST http://localhost:8000/test/payment \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.00, "source": "test"}'
```

## API Reference

### UIDPWebhookHandler

#### Methods

**`calculate_split(amount: Decimal) -> Tuple[Decimal, Decimal]`**
- Calculates nonprofit and DAO amounts
- Returns: `(nonprofit_amount, dao_amount)`

**`handle_stripe_webhook(payload: Dict, signature: str) -> Dict`**
- Processes Stripe webhook events
- Verifies signature
- Routes payments automatically

**`handle_paypal_webhook(payload: Dict) -> Dict`**
- Processes PayPal webhook events
- Routes payments automatically

**`handle_crypto_transaction(tx_hash: str, amount: Decimal, currency: str) -> Dict`**
- Processes cryptocurrency transactions
- Routes payments automatically

**`split_and_route(amount: Decimal, source: str, source_tx_id: str) -> Dict`**
- Core routing logic
- Splits and routes payment
- Returns transaction result

**`verify_compliance(days: int) -> Dict`**
- Verifies compliance over time period
- Returns compliance report

### NFTReceiptMinter

#### Methods

**`mint_receipt(...) -> Dict`**
- Creates NFT receipt for donation
- Returns receipt metadata

**`upload_to_ipfs(receipt: Dict) -> str`**
- Uploads receipt to IPFS
- Returns IPFS URI

**`mint_nft_on_chain(receipt: Dict, contract_address: str, donor_wallet: str) -> Dict`**
- Mints NFT on blockchain
- Returns transaction details

**`verify_receipt(receipt_id: str) -> Optional[Dict]`**
- Verifies receipt authenticity
- Returns receipt data if valid

**`calculate_tax_summary(donor_address: str, tax_year: int) -> Dict`**
- Generates tax deduction summary
- Returns all donations for tax year

## Smart Contract Integration

### Ethereum Example
```solidity
contract UIDPEscrow {
    address public nonprofitWallet = 0x...;
    address public daoWallet = 0x...;
    uint8 public charitablePercentage = 7;
    
    function receivePayment() public payable {
        require(msg.value > 0, "Payment required");
        
        uint256 nonprofitAmount = (msg.value * charitablePercentage) / 100;
        uint256 daoAmount = msg.value - nonprofitAmount;
        
        // Nonprofit transfer FIRST
        (bool success1, ) = nonprofitWallet.call{value: nonprofitAmount}("");
        require(success1, "Nonprofit transfer failed");
        
        // DAO transfer only after nonprofit succeeds
        (bool success2, ) = daoWallet.call{value: daoAmount}("");
        require(success2, "DAO transfer failed");
        
        emit PaymentProcessed(msg.sender, msg.value, nonprofitAmount, daoAmount);
    }
}
```

### Deployment
```bash
# Deploy smart contract
python3 uidp/deploy_contract.py --network mainnet

# Verify deployment
python3 uidp/verify_contract.py --address 0x...
```

## Transparency & Reporting

### Monthly Transparency Report
Generated automatically on the 1st of each month:
- Total revenue received
- Total charitable allocation
- All transaction hashes
- Compliance verification
- Published to GitHub, IPFS, Arweave

### Real-Time Dashboard
```bash
# Start transparency dashboard
python3 uidp/dashboard.py

# Access at http://localhost:5000
```

Shows:
- Live transaction feed
- Cumulative charitable impact
- Compliance status
- Recent NFT receipts
- Blockchain verification links

## FAQs

### Q: Can the 7% be changed?
A: No. The percentage is locked in the cryptographic oath and cannot be changed without breaking the node's identity chain.

### Q: What happens if the nonprofit transfer fails?
A: The entire transaction is aborted. In production, this triggers an automatic refund to the sender.

### Q: Are donations tax-deductible?
A: Once ValorYield Engine receives 501(c)(3) approval from the IRS, donations will be tax-deductible. NFT receipts provide documentation.

### Q: Can I verify the charitable allocations?
A: Yes! All transactions are public on blockchain. Anyone can verify at any time.

### Q: What happens to the DAO's 93%?
A: It's used for operational costs, development, and growth. The DAO is a for-profit entity using the remaining funds to sustain and scale operations.

### Q: How are beneficiary charities chosen?
A: ValorYield Engine (the nonprofit) distributes funds to IRS-approved 501(c)(3) organizations focusing on medical research, humanitarian aid, veterans, and education.

## Roadmap

### Phase 1: Core Implementation ✓
- [x] Webhook handlers for Stripe, PayPal, crypto
- [x] Automatic payment splitting
- [x] NFT receipt generation
- [x] Transaction logging
- [x] Compliance verification

### Phase 2: Smart Contracts (In Progress)
- [ ] Deploy Ethereum smart contract
- [ ] Deploy Polygon smart contract (lower fees)
- [ ] Multi-signature security
- [ ] Emergency pause functionality

### Phase 3: Production Deployment
- [ ] Production server setup
- [ ] Monitoring and alerting
- [ ] Automatic backup systems
- [ ] Disaster recovery procedures

### Phase 4: Expansion
- [ ] Additional payment processors
- [ ] More blockchain integrations
- [ ] Enhanced NFT artwork
- [ ] Mobile app for donors

## Contributing

This is an open-source project. Contributions welcome!

### Development Setup
```bash
git clone https://github.com/Me10101-01/Node137_Uplink_Receipt.git
cd Node137_Uplink_Receipt
pip install -r requirements.txt
python3 -m pytest
```

### Code Standards
- Python 3.8+ with type hints
- PEP 8 style guide
- Comprehensive docstrings
- Unit tests for all functions
- Security-first mindset

## License

MIT License - See LICENSE file for details

## Support

- **GitHub Issues:** https://github.com/Me10101-01/Node137_Uplink_Receipt/issues
- **Documentation:** https://github.com/Me10101-01/Node137_Uplink_Receipt/tree/main/uidp
- **Email:** [Contact via GitHub]

## Acknowledgments

Built with ❤️ by Node 137 / Domenic Garza

Part of the Strategickhaos dual-entity ecosystem:
- **Strategickhaos DAO LLC:** Technology development
- **ValorYield Engine:** Charitable distribution (501(c)(3) pending)

---

**Status:** Production-ready prototype  
**Version:** 1.0.0  
**Last Updated:** November 23, 2025  
**Patent:** Provisional application pending (USPTO)
