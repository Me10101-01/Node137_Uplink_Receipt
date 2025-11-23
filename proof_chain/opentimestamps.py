#!/usr/bin/env python3
"""
OpenTimestamps Integration
Provides blockchain timestamping for immutable proof-of-existence
"""

import hashlib
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class OpenTimestampsManager:
    """
    Manages OpenTimestamps operations for document timestamping
    
    OpenTimestamps provides cryptographic proof that a document
    existed at a specific time by anchoring its hash to Bitcoin blockchain.
    """
    
    def __init__(self, ots_cli_path: Optional[str] = None):
        """
        Initialize OpenTimestamps manager
        
        Args:
            ots_cli_path: Path to ots CLI tool (default: search PATH)
        """
        self.ots_cli = ots_cli_path or 'ots'
        self.timestamp_dir = Path('timestamps')
        self.timestamp_dir.mkdir(exist_ok=True)
        
        # Check if OTS is available
        self.available = self.check_ots_available()
    
    def check_ots_available(self) -> bool:
        """Check if OpenTimestamps CLI is available"""
        try:
            result = subprocess.run(
                [self.ots_cli, '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def timestamp_file(self, file_path: str) -> Dict:
        """
        Create an OpenTimestamps proof for a file
        
        Args:
            file_path: Path to file to timestamp
            
        Returns:
            Dictionary with timestamp information
        """
        if not self.available:
            return self.simulate_timestamp(file_path)
        
        file_path = Path(file_path)
        ots_file = file_path.with_suffix(file_path.suffix + '.ots')
        
        try:
            print(f"Creating timestamp for {file_path.name}...")
            
            # Run ots stamp
            result = subprocess.run(
                [self.ots_cli, 'stamp', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    'status': 'stamped',
                    'file': str(file_path),
                    'ots_file': str(ots_file),
                    'timestamp': time.time(),
                    'message': 'Timestamp proof created (pending Bitcoin confirmation)'
                }
            else:
                raise Exception(f"Timestamp failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'file': str(file_path),
                'message': 'Timestamp request timed out'
            }
        except Exception as e:
            return {
                'status': 'error',
                'file': str(file_path),
                'error': str(e)
            }
    
    def timestamp_data(self, data: str, filename: str = 'document') -> Dict:
        """
        Create timestamp for data (not a file)
        
        Args:
            data: Data to timestamp
            filename: Base filename for storage
            
        Returns:
            Dictionary with timestamp information
        """
        # Write data to temporary file
        temp_file = self.timestamp_dir / f"{filename}_{int(time.time())}.txt"
        temp_file.write_text(data)
        
        # Timestamp the file
        result = self.timestamp_file(str(temp_file))
        
        # Calculate hash for reference
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        result['sha256'] = data_hash
        
        return result
    
    def verify_timestamp(self, ots_file: str) -> Dict:
        """
        Verify an OpenTimestamps proof
        
        Args:
            ots_file: Path to .ots file
            
        Returns:
            Verification result dictionary
        """
        if not self.available:
            return {
                'status': 'simulation',
                'message': 'OTS not available - cannot verify'
            }
        
        try:
            # Run ots verify
            result = subprocess.run(
                [self.ots_cli, 'verify', ots_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse output for timestamp
                output = result.stdout
                
                return {
                    'status': 'verified',
                    'ots_file': ots_file,
                    'output': output,
                    'verified': True
                }
            else:
                return {
                    'status': 'unverified',
                    'ots_file': ots_file,
                    'message': 'Timestamp not yet confirmed on blockchain',
                    'output': result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'message': 'Verification timed out'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def upgrade_timestamp(self, ots_file: str) -> Dict:
        """
        Upgrade timestamp proof (get Bitcoin confirmations)
        
        Args:
            ots_file: Path to .ots file
            
        Returns:
            Upgrade result dictionary
        """
        if not self.available:
            return {
                'status': 'simulation',
                'message': 'OTS not available'
            }
        
        try:
            result = subprocess.run(
                [self.ots_cli, 'upgrade', ots_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'status': 'upgraded' if result.returncode == 0 else 'no_upgrade',
                'ots_file': ots_file,
                'output': result.stdout
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def simulate_timestamp(self, file_path: str) -> Dict:
        """
        Simulate timestamping when OTS is not available
        
        Creates a hash-based proof of existence.
        
        Args:
            file_path: Path to file
            
        Returns:
            Simulated timestamp result
        """
        file_path = Path(file_path)
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Create simulation proof
        proof = {
            'type': 'simulated_timestamp',
            'file': str(file_path),
            'sha256': file_hash,
            'timestamp': time.time(),
            'timestamp_iso': datetime.utcnow().isoformat(),
            'note': 'This is a simulated timestamp. Install OpenTimestamps CLI for real Bitcoin timestamping.'
        }
        
        # Save proof
        proof_file = file_path.with_suffix(file_path.suffix + '.timestamp.json')
        with open(proof_file, 'w') as f:
            json.dump(proof, f, indent=2)
        
        return {
            'status': 'simulated',
            'file': str(file_path),
            'proof_file': str(proof_file),
            'sha256': file_hash,
            'timestamp': proof['timestamp'],
            'message': 'Simulated timestamp created (install OTS for blockchain anchoring)'
        }


class TimestampChain:
    """
    Maintains a chain of timestamped documents
    
    Combines GPG signatures with OpenTimestamps for dual proof:
    - GPG proves authorship
    - OTS proves existence at specific time
    """
    
    def __init__(self, ots_manager: OpenTimestampsManager):
        """
        Initialize timestamp chain
        
        Args:
            ots_manager: OpenTimestamps manager instance
        """
        self.ots = ots_manager
        self.chain_file = 'timestamp_chain.json'
        self.chain = self.load_chain()
    
    def load_chain(self) -> list:
        """Load existing chain"""
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_chain(self):
        """Save chain to file"""
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def add_timestamped_document(
        self,
        document: Dict,
        gpg_signature: Optional[str] = None
    ) -> Dict:
        """
        Add a document with timestamp and signature
        
        Args:
            document: Document to timestamp
            gpg_signature: GPG signature (if available)
            
        Returns:
            Chain entry with timestamp proof
        """
        # Serialize document
        doc_json = json.dumps(document, sort_keys=True)
        doc_hash = hashlib.sha256(doc_json.encode()).hexdigest()
        
        # Create entry
        entry = {
            'sequence': len(self.chain) + 1,
            'document_hash': doc_hash,
            'document': document,
            'gpg_signature': gpg_signature,
            'created_at': time.time()
        }
        
        # Timestamp the entry
        timestamp_result = self.ots.timestamp_data(
            doc_json,
            filename=f'doc_{entry["sequence"]}'
        )
        
        entry['timestamp'] = timestamp_result
        
        # Add to chain
        self.chain.append(entry)
        self.save_chain()
        
        return entry
    
    def verify_entry(self, sequence: int) -> Dict:
        """
        Verify a specific chain entry
        
        Args:
            sequence: Entry sequence number
            
        Returns:
            Verification result
        """
        if sequence < 1 or sequence > len(self.chain):
            return {'valid': False, 'error': 'Invalid sequence number'}
        
        entry = self.chain[sequence - 1]
        
        # Verify document hash
        doc_json = json.dumps(entry['document'], sort_keys=True)
        calculated_hash = hashlib.sha256(doc_json.encode()).hexdigest()
        
        hash_valid = calculated_hash == entry['document_hash']
        
        # Verify OTS timestamp if available
        ots_file = entry['timestamp'].get('ots_file')
        if ots_file and os.path.exists(ots_file):
            ots_verification = self.ots.verify_timestamp(ots_file)
        else:
            ots_verification = {'status': 'no_ots_file'}
        
        return {
            'valid': hash_valid,
            'sequence': sequence,
            'hash_valid': hash_valid,
            'ots_verification': ots_verification,
            'created_at': entry['created_at']
        }


def main():
    """Example usage"""
    print("=" * 60)
    print("OpenTimestamps Integration - Test Mode")
    print("=" * 60)
    
    # Initialize manager
    ots = OpenTimestampsManager()
    
    print(f"\nOTS CLI available: {ots.available}")
    if not ots.available:
        print("Note: OpenTimestamps CLI not found.")
        print("Install from: https://github.com/opentimestamps/opentimestamps-client")
        print("Using simulation mode for testing.")
    
    # Test timestamping
    print("\n" + "=" * 60)
    print("Testing document timestamping...")
    print("=" * 60)
    
    test_document = {
        "type": "test_document",
        "node_id": "Node137",
        "message": "This is a test of the OpenTimestamps system",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    print("\nDocument to timestamp:")
    print(json.dumps(test_document, indent=2))
    
    # Timestamp the document
    doc_json = json.dumps(test_document, sort_keys=True)
    result = ots.timestamp_data(doc_json, 'test_document')
    
    print("\nTimestamp result:")
    print(f"Status: {result['status']}")
    print(f"SHA-256: {result.get('sha256', 'N/A')}")
    if 'ots_file' in result:
        print(f"OTS file: {result['ots_file']}")
    if 'proof_file' in result:
        print(f"Proof file: {result['proof_file']}")
    print(f"Message: {result.get('message', 'N/A')}")
    
    # Test timestamp chain
    print("\n" + "=" * 60)
    print("Testing timestamp chain...")
    print("=" * 60)
    
    chain = TimestampChain(ots)
    
    print(f"\nExisting chain entries: {len(chain.chain)}")
    
    # Add entry
    print("\nAdding test entry to chain...")
    entry = chain.add_timestamped_document(test_document)
    
    print(f"Entry added: Sequence {entry['sequence']}")
    print(f"Document hash: {entry['document_hash'][:32]}...")
    print(f"Timestamp status: {entry['timestamp']['status']}")
    
    # Verify entry
    print("\nVerifying entry...")
    verification = chain.verify_entry(entry['sequence'])
    
    print(f"Valid: {verification['valid']}")
    print(f"Hash valid: {verification['hash_valid']}")
    print(f"OTS verification: {verification['ots_verification']['status']}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Install OpenTimestamps CLI for real Bitcoin timestamping")
    print("2. Wait 1-6 hours for Bitcoin confirmation")
    print("3. Run 'ots upgrade' to get blockchain confirmations")
    print("4. Run 'ots verify' to verify timestamp against blockchain")


if __name__ == '__main__':
    main()
