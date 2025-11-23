#!/usr/bin/env python3
"""
NFT Donation Receipt Minter
Creates NFT receipts for charitable donations via UIDP
"""

import hashlib
import json
import time
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional


class NFTReceiptMinter:
    """
    Mints NFT receipts for charitable donations
    
    Each NFT serves as immutable proof of charitable contribution
    and can be used for tax deduction documentation.
    """
    
    def __init__(self, node_id: str = 'Node137'):
        self.node_id = node_id
        self.receipt_counter = 0
        self.minted_receipts = []
        
    def mint_receipt(
        self,
        total_amount: Decimal,
        nonprofit_amount: Decimal,
        beneficiary: str = 'ValorYield Engine',
        donor_address: Optional[str] = None,
        transaction_hash: Optional[str] = None
    ) -> Dict:
        """
        Mint an NFT receipt for a donation
        
        Args:
            total_amount: Total transaction amount
            nonprofit_amount: Amount allocated to charity
            beneficiary: Nonprofit beneficiary name
            donor_address: Donor's wallet address (optional for privacy)
            transaction_hash: Blockchain transaction hash
            
        Returns:
            NFT metadata and receipt information
        """
        self.receipt_counter += 1
        receipt_id = f"{self.node_id}_RECEIPT_{self.receipt_counter:06d}"
        timestamp = time.time()
        
        # Calculate percentage
        percentage = (nonprofit_amount / total_amount * 100) if total_amount > 0 else 0
        
        # Create metadata
        metadata = {
            "name": f"ValorYield Donation Receipt #{self.receipt_counter}",
            "description": (
                f"Proof of ${nonprofit_amount:.2f} charitable contribution "
                f"via Strategickhaos DAO UIDP protocol. "
                f"This NFT certifies that {percentage:.1f}% of the transaction "
                f"was allocated to {beneficiary} for charitable purposes."
            ),
            "image": f"ipfs://[PLACEHOLDER]/receipt_{receipt_id}.png",
            "external_url": "https://github.com/Me10101-01/Node137_Uplink_Receipt",
            "attributes": [
                {
                    "trait_type": "Receipt ID",
                    "value": receipt_id
                },
                {
                    "trait_type": "Total Amount",
                    "value": f"${total_amount:.2f}"
                },
                {
                    "trait_type": "Charitable Amount",
                    "value": f"${nonprofit_amount:.2f}"
                },
                {
                    "trait_type": "Percentage",
                    "value": f"{percentage:.1f}%"
                },
                {
                    "trait_type": "Beneficiary",
                    "value": beneficiary
                },
                {
                    "trait_type": "Node ID",
                    "value": self.node_id
                },
                {
                    "trait_type": "Timestamp",
                    "value": datetime.utcfromtimestamp(timestamp).isoformat()
                },
                {
                    "trait_type": "Transaction Hash",
                    "value": transaction_hash or "N/A"
                }
            ],
            "properties": {
                "category": "donation_receipt",
                "charitable_organization": beneficiary,
                "tax_deductible": "pending_501c3_approval",
                "verification": "blockchain_verified"
            }
        }
        
        # Create receipt record
        receipt = {
            "receipt_id": receipt_id,
            "metadata": metadata,
            "donor_address": donor_address or "anonymous",
            "mint_timestamp": timestamp,
            "blockchain_tx": transaction_hash,
            "ipfs_uri": None,  # To be set after IPFS upload
            "nft_token_id": None,  # To be set after minting
            "status": "prepared"
        }
        
        # Calculate metadata hash for verification
        metadata_json = json.dumps(metadata, sort_keys=True)
        receipt["metadata_hash"] = hashlib.sha256(metadata_json.encode()).hexdigest()
        
        self.minted_receipts.append(receipt)
        
        return receipt
    
    def generate_receipt_image(self, receipt: Dict) -> str:
        """
        Generate visual receipt image (placeholder)
        
        In production, this would create an actual image with:
        - Organization logo
        - Receipt details
        - QR code for verification
        - Blockchain transaction info
        
        Args:
            receipt: Receipt data
            
        Returns:
            Path to generated image or IPFS URI
        """
        # Placeholder - in production would use PIL/Pillow to create image
        return f"receipt_{receipt['receipt_id']}.png"
    
    def upload_to_ipfs(self, receipt: Dict) -> str:
        """
        Upload receipt metadata to IPFS
        
        In production, this would:
        1. Generate receipt image
        2. Upload image to IPFS
        3. Upload metadata JSON to IPFS
        4. Return IPFS URI
        
        Args:
            receipt: Receipt data
            
        Returns:
            IPFS URI for metadata
        """
        # Placeholder - in production would use ipfshttpclient
        ipfs_hash = hashlib.sha256(
            json.dumps(receipt['metadata']).encode()
        ).hexdigest()[:46]
        
        ipfs_uri = f"ipfs://{ipfs_hash}"
        receipt['ipfs_uri'] = ipfs_uri
        receipt['status'] = 'uploaded_to_ipfs'
        
        return ipfs_uri
    
    def mint_nft_on_chain(
        self,
        receipt: Dict,
        contract_address: str,
        donor_wallet: str
    ) -> Dict:
        """
        Mint NFT on blockchain
        
        In production, this would:
        1. Connect to Ethereum/Polygon/etc.
        2. Call NFT contract's mint function
        3. Transfer NFT to donor's wallet
        4. Return transaction hash and token ID
        
        Args:
            receipt: Receipt data with IPFS URI
            contract_address: NFT contract address
            donor_wallet: Recipient wallet address
            
        Returns:
            Minting transaction details
        """
        # Placeholder - in production would use web3.py
        if not receipt.get('ipfs_uri'):
            raise ValueError("Receipt must be uploaded to IPFS before minting")
        
        # Simulate minting
        token_id = self.receipt_counter
        tx_hash = hashlib.sha256(
            f"{contract_address}{donor_wallet}{token_id}{time.time()}".encode()
        ).hexdigest()
        
        receipt['nft_token_id'] = token_id
        receipt['nft_contract'] = contract_address
        receipt['mint_tx_hash'] = tx_hash
        receipt['status'] = 'minted'
        
        return {
            "token_id": token_id,
            "contract_address": contract_address,
            "transaction_hash": tx_hash,
            "owner": donor_wallet,
            "metadata_uri": receipt['ipfs_uri']
        }
    
    def verify_receipt(self, receipt_id: str) -> Optional[Dict]:
        """
        Verify a receipt by ID
        
        Args:
            receipt_id: Receipt identifier
            
        Returns:
            Receipt data if found and valid
        """
        for receipt in self.minted_receipts:
            if receipt['receipt_id'] == receipt_id:
                # Verify metadata hash
                metadata_json = json.dumps(receipt['metadata'], sort_keys=True)
                calculated_hash = hashlib.sha256(metadata_json.encode()).hexdigest()
                
                if calculated_hash == receipt['metadata_hash']:
                    return receipt
                else:
                    return {
                        "error": "Receipt metadata hash mismatch",
                        "receipt_id": receipt_id
                    }
        
        return None
    
    def get_donor_receipts(self, donor_address: str) -> list:
        """
        Get all receipts for a specific donor
        
        Args:
            donor_address: Donor's wallet address
            
        Returns:
            List of receipts
        """
        return [
            receipt for receipt in self.minted_receipts
            if receipt['donor_address'] == donor_address
        ]
    
    def calculate_tax_summary(self, donor_address: str, tax_year: int) -> Dict:
        """
        Calculate tax deduction summary for a donor
        
        Args:
            donor_address: Donor's wallet address
            tax_year: Tax year to summarize
            
        Returns:
            Tax summary with total charitable donations
        """
        year_start = datetime(tax_year, 1, 1).timestamp()
        year_end = datetime(tax_year, 12, 31, 23, 59, 59).timestamp()
        
        donor_receipts = self.get_donor_receipts(donor_address)
        year_receipts = [
            receipt for receipt in donor_receipts
            if year_start <= receipt['mint_timestamp'] <= year_end
        ]
        
        total_charitable = sum(
            Decimal(attr['value'].replace('$', ''))
            for receipt in year_receipts
            for attr in receipt['metadata']['attributes']
            if attr['trait_type'] == 'Charitable Amount'
        )
        
        return {
            "donor_address": donor_address,
            "tax_year": tax_year,
            "total_donations": f"${total_charitable:.2f}",
            "number_of_donations": len(year_receipts),
            "receipts": [
                {
                    "receipt_id": r['receipt_id'],
                    "date": datetime.utcfromtimestamp(r['mint_timestamp']).isoformat(),
                    "amount": next(
                        a['value'] for a in r['metadata']['attributes']
                        if a['trait_type'] == 'Charitable Amount'
                    ),
                    "beneficiary": next(
                        a['value'] for a in r['metadata']['attributes']
                        if a['trait_type'] == 'Beneficiary'
                    )
                }
                for r in year_receipts
            ]
        }


def main():
    """Example usage"""
    print("=" * 60)
    print("NFT Donation Receipt Minter - Test Mode")
    print("=" * 60)
    
    minter = NFTReceiptMinter(node_id="Node137")
    
    # Mint a test receipt
    print("\nMinting test receipt...")
    receipt = minter.mint_receipt(
        total_amount=Decimal('100.00'),
        nonprofit_amount=Decimal('7.00'),
        beneficiary='ValorYield Engine',
        donor_address='0x1234567890abcdef',
        transaction_hash='0xabcdef123456'
    )
    
    print(f"\nReceipt ID: {receipt['receipt_id']}")
    print(f"Status: {receipt['status']}")
    print(f"Metadata Hash: {receipt['metadata_hash']}")
    
    # Upload to IPFS (simulated)
    print("\nUploading to IPFS...")
    ipfs_uri = minter.upload_to_ipfs(receipt)
    print(f"IPFS URI: {ipfs_uri}")
    
    # Mint NFT (simulated)
    print("\nMinting NFT on blockchain...")
    nft_result = minter.mint_nft_on_chain(
        receipt=receipt,
        contract_address='0xNFTContract123',
        donor_wallet='0x1234567890abcdef'
    )
    
    print(f"Token ID: {nft_result['token_id']}")
    print(f"Transaction Hash: {nft_result['transaction_hash']}")
    
    # Verify receipt
    print("\nVerifying receipt...")
    verified = minter.verify_receipt(receipt['receipt_id'])
    print(f"Verification: {'VALID' if verified and 'error' not in verified else 'INVALID'}")
    
    # Tax summary
    print("\nGenerating tax summary...")
    tax_summary = minter.calculate_tax_summary(
        donor_address='0x1234567890abcdef',
        tax_year=2025
    )
    
    print(json.dumps(tax_summary, indent=2))
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
