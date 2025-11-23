#!/usr/bin/env python3
"""
GPG Signing and Verification System
Provides cryptographic signing for all Node137 operations
"""

try:
    import gnupg
    GNUPG_AVAILABLE = True
except ImportError:
    GNUPG_AVAILABLE = False
    
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, List


class GPGManager:
    """
    Manages GPG operations for ReflexShell node identity
    
    This system provides:
    - Key generation and management
    - Document signing
    - Signature verification
    - Chain of custody maintenance
    """
    
    def __init__(self, gpg_home: Optional[str] = None):
        """
        Initialize GPG manager
        
        Args:
            gpg_home: Path to GPG home directory (default: ~/.gnupg)
        """
        self.gpg_home = gpg_home or os.path.expanduser('~/.gnupg')
        os.makedirs(self.gpg_home, exist_ok=True)
        
        if GNUPG_AVAILABLE:
            try:
                self.gpg = gnupg.GPG(gnupghome=self.gpg_home)
            except Exception as e:
                print(f"Warning: Could not initialize python-gnupg: {e}")
                print("Falling back to command-line GPG")
                self.gpg = None
        else:
            self.gpg = None
    
    def generate_node_key(
        self,
        node_id: str,
        name: str = "Node 137",
        email: str = "node137@strategickhaos.system",
        comment: str = "ReflexShell Sovereign Node",
        key_type: str = "RSA",
        key_length: int = 4096
    ) -> Dict:
        """
        Generate a GPG keypair for a ReflexShell node
        
        Args:
            node_id: Unique node identifier
            name: Name for the key
            email: Email for the key
            comment: Comment field
            key_type: Type of key (RSA, DSA, etc.)
            key_length: Key length in bits
            
        Returns:
            Dictionary with key information
        """
        print(f"Generating GPG keypair for {node_id}...")
        print(f"Key type: {key_type} {key_length}-bit")
        print(f"This may take a moment...")
        
        if self.gpg:
            # Use python-gnupg
            input_data = self.gpg.gen_key_input(
                name_real=name,
                name_email=email,
                name_comment=f"{comment} - {node_id}",
                key_type=key_type,
                key_length=key_length,
                passphrase=''  # No passphrase for automated signing - PRODUCTION: Use HSM or secure key storage
            )
            
            key = self.gpg.gen_key(input_data)
            
            return {
                'fingerprint': str(key),
                'node_id': node_id,
                'name': name,
                'email': email,
                'status': 'generated'
            }
        else:
            # Use command-line GPG
            batch_input = f"""
%echo Generating key for {node_id}
Key-Type: {key_type}
Key-Length: {key_length}
Name-Real: {name}
Name-Comment: {comment} - {node_id}
Name-Email: {email}
Expire-Date: 0
%no-protection
%commit
%echo done
"""
            
            batch_file = Path(self.gpg_home) / f'keygen_{node_id}.batch'
            batch_file.write_text(batch_input)
            
            try:
                result = subprocess.run(
                    ['gpg', '--batch', '--gen-key', str(batch_file)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                batch_file.unlink()  # Clean up
                
                if result.returncode == 0:
                    # Get the fingerprint
                    list_result = subprocess.run(
                        ['gpg', '--list-keys', '--with-colons', email],
                        capture_output=True,
                        text=True
                    )
                    
                    fingerprint = None
                    for line in list_result.stdout.split('\n'):
                        if line.startswith('fpr:'):
                            fingerprint = line.split(':')[9]
                            break
                    
                    return {
                        'fingerprint': fingerprint,
                        'node_id': node_id,
                        'name': name,
                        'email': email,
                        'status': 'generated'
                    }
                else:
                    raise Exception(f"Key generation failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                raise Exception("Key generation timed out")
    
    def sign_document(
        self,
        data: str,
        fingerprint: Optional[str] = None,
        detached: bool = False
    ) -> str:
        """
        Sign a document with GPG
        
        Args:
            data: Data to sign (string or JSON-serializable object)
            fingerprint: Key fingerprint to use (default: first available)
            detached: Create detached signature
            
        Returns:
            Signed data or signature
        """
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        
        if self.gpg:
            # Use python-gnupg
            signed = self.gpg.sign(
                data,
                keyid=fingerprint,
                detach=detached
            )
            return str(signed)
        else:
            # Use command-line GPG
            cmd = ['gpg', '--armor', '--sign']
            if detached:
                cmd.append('--detach-sign')
            if fingerprint:
                cmd.extend(['--local-user', fingerprint])
            
            result = subprocess.run(
                cmd,
                input=data.encode(),
                capture_output=True
            )
            
            if result.returncode == 0:
                return result.stdout.decode()
            else:
                raise Exception(f"Signing failed: {result.stderr.decode()}")
    
    def verify_signature(self, signed_data: str) -> Dict:
        """
        Verify a GPG signature
        
        Args:
            signed_data: Signed data to verify
            
        Returns:
            Verification result dictionary
        """
        if self.gpg:
            # Use python-gnupg
            verified = self.gpg.verify(signed_data)
            
            return {
                'valid': verified.valid,
                'fingerprint': verified.fingerprint,
                'username': verified.username,
                'timestamp': verified.timestamp,
                'status': verified.status
            }
        else:
            # Use command-line GPG
            result = subprocess.run(
                ['gpg', '--verify'],
                input=signed_data.encode(),
                capture_output=True,
                text=True
            )
            
            return {
                'valid': result.returncode == 0,
                'output': result.stderr,
                'status': 'verified' if result.returncode == 0 else 'failed'
            }
    
    def export_public_key(self, fingerprint: str) -> str:
        """
        Export public key in ASCII armor format
        
        Args:
            fingerprint: Key fingerprint
            
        Returns:
            ASCII-armored public key
        """
        if self.gpg:
            return self.gpg.export_keys(fingerprint)
        else:
            result = subprocess.run(
                ['gpg', '--armor', '--export', fingerprint],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"Export failed: {result.stderr}")
    
    def list_keys(self) -> List[Dict]:
        """
        List all available keys
        
        Returns:
            List of key information dictionaries
        """
        if self.gpg:
            keys = self.gpg.list_keys()
            return [
                {
                    'fingerprint': key['fingerprint'],
                    'uids': key['uids'],
                    'length': key['length'],
                    'algo': key['algo'],
                    'created': key['date']
                }
                for key in keys
            ]
        else:
            result = subprocess.run(
                ['gpg', '--list-keys', '--with-colons'],
                capture_output=True,
                text=True
            )
            
            keys = []
            current_key = {}
            
            for line in result.stdout.split('\n'):
                parts = line.split(':')
                if parts[0] == 'pub':
                    current_key = {
                        'algo': parts[3],
                        'length': parts[2],
                        'created': parts[5]
                    }
                elif parts[0] == 'fpr':
                    current_key['fingerprint'] = parts[9]
                elif parts[0] == 'uid':
                    current_key['uid'] = parts[9]
                    keys.append(current_key.copy())
            
            return keys


class SignatureChain:
    """
    Maintains a cryptographic chain of signed documents
    
    Each document references the hash of the previous document,
    creating an immutable chain of custody.
    """
    
    def __init__(self, gpg_manager: GPGManager, chain_file: Optional[str] = None):
        """
        Initialize signature chain
        
        Args:
            gpg_manager: GPG manager instance
            chain_file: Path to chain storage file
        """
        self.gpg = gpg_manager
        self.chain_file = chain_file or 'signature_chain.json'
        self.chain = self.load_chain()
    
    def load_chain(self) -> List[Dict]:
        """Load existing chain from file"""
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_chain(self):
        """Save chain to file"""
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def get_last_hash(self) -> Optional[str]:
        """Get hash of last document in chain"""
        if self.chain:
            return self.chain[-1]['hash']
        return None
    
    def add_document(
        self,
        document: Dict,
        fingerprint: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Add a signed document to the chain
        
        Args:
            document: Document to add
            fingerprint: GPG key to sign with
            metadata: Additional metadata
            
        Returns:
            Chain entry with signature
        """
        # Get previous hash
        previous_hash = self.get_last_hash()
        
        # Create chain entry
        entry = {
            'document': document,
            'previous_hash': previous_hash,
            'metadata': metadata or {},
            'sequence': len(self.chain) + 1
        }
        
        # Calculate hash
        entry_json = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        entry['hash'] = entry_hash
        
        # Sign the entry
        signature = self.gpg.sign_document(entry_json, fingerprint, detached=True)
        entry['signature'] = signature
        
        # Add to chain
        self.chain.append(entry)
        self.save_chain()
        
        return entry
    
    def verify_chain(self) -> Dict:
        """
        Verify integrity of entire chain
        
        Returns:
            Verification result
        """
        if not self.chain:
            return {'valid': True, 'message': 'Empty chain'}
        
        errors = []
        
        for i, entry in enumerate(self.chain):
            # Check sequence number
            if entry['sequence'] != i + 1:
                errors.append(f"Entry {i}: Invalid sequence number")
            
            # Check previous hash
            if i > 0:
                expected_prev = self.chain[i-1]['hash']
                if entry['previous_hash'] != expected_prev:
                    errors.append(f"Entry {i}: Previous hash mismatch")
            
            # Verify hash
            entry_copy = entry.copy()
            signature = entry_copy.pop('signature')
            entry_hash = entry_copy.pop('hash')
            
            calculated_hash = hashlib.sha256(
                json.dumps(entry_copy, sort_keys=True).encode()
            ).hexdigest()
            
            if calculated_hash != entry_hash:
                errors.append(f"Entry {i}: Hash mismatch")
            
            # Verify signature
            verification = self.gpg.verify_signature(signature)
            if not verification.get('valid'):
                errors.append(f"Entry {i}: Invalid signature")
        
        return {
            'valid': len(errors) == 0,
            'entries_checked': len(self.chain),
            'errors': errors
        }


def main():
    """Example usage"""
    print("=" * 60)
    print("GPG Signing System - Test Mode")
    print("=" * 60)
    
    # Initialize GPG manager
    gpg_mgr = GPGManager()
    
    # List existing keys
    print("\nExisting GPG keys:")
    keys = gpg_mgr.list_keys()
    for key in keys:
        print(f"  - {key.get('fingerprint', 'N/A')[:16]}... {key.get('uid', 'N/A')}")
    
    if not keys:
        print("  (No keys found)")
        print("\nNote: Key generation requires GPG to be installed.")
        print("To generate a key manually:")
        print("  gpg --gen-key")
    
    # Test signing
    print("\n" + "=" * 60)
    print("Testing document signing...")
    print("=" * 60)
    
    test_document = {
        "type": "test_document",
        "node_id": "Node137",
        "message": "This is a test of the GPG signing system",
        "timestamp": "2025-11-23T04:00:00Z"
    }
    
    print("\nDocument to sign:")
    print(json.dumps(test_document, indent=2))
    
    try:
        if keys:
            fingerprint = keys[0]['fingerprint']
            print(f"\nSigning with key: {fingerprint[:16]}...")
            
            signed = gpg_mgr.sign_document(test_document, fingerprint)
            print("\nSigned successfully!")
            print(f"Signature length: {len(signed)} bytes")
            
            # Verify
            print("\nVerifying signature...")
            verification = gpg_mgr.verify_signature(signed)
            print(f"Valid: {verification.get('valid')}")
            print(f"Status: {verification.get('status')}")
        else:
            print("\nSkipping signing test (no keys available)")
    except Exception as e:
        print(f"\nSigning test failed: {e}")
    
    # Test signature chain
    print("\n" + "=" * 60)
    print("Testing signature chain...")
    print("=" * 60)
    
    chain_file = '/tmp/test_signature_chain.json'
    chain = SignatureChain(gpg_mgr, chain_file)
    
    print(f"\nChain file: {chain_file}")
    print(f"Existing entries: {len(chain.chain)}")
    
    # Add test entry
    try:
        if keys:
            print("\nAdding test entry to chain...")
            entry = chain.add_document(
                document=test_document,
                fingerprint=keys[0]['fingerprint'],
                metadata={'test': True}
            )
            print(f"Entry added: Sequence {entry['sequence']}")
            print(f"Hash: {entry['hash'][:32]}...")
            
            # Verify chain
            print("\nVerifying chain integrity...")
            verification = chain.verify_chain()
            print(f"Valid: {verification['valid']}")
            print(f"Entries checked: {verification['entries_checked']}")
            if verification['errors']:
                print("Errors:")
                for error in verification['errors']:
                    print(f"  - {error}")
        else:
            print("\nSkipping chain test (no keys available)")
    except Exception as e:
        print(f"\nChain test failed: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
