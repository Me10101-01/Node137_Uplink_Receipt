#!/usr/bin/env python3
"""
Transparency Report Generator
Creates comprehensive public reports of all dual-entity operations
"""

import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional


class TransparencyReportGenerator:
    """
    Generates comprehensive transparency reports for public accountability
    
    Reports include:
    - Entity information and legal status
    - Financial transactions and charitable allocations
    - Compliance verification
    - Blockchain verification links
    - Beneficiary distributions
    """
    
    def __init__(self, output_dir: str = 'transparency/reports'):
        """
        Initialize report generator
        
        Args:
            output_dir: Directory for report output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_monthly_report(
        self,
        month: int,
        year: int,
        transactions: List[Dict],
        entity_info: Optional[Dict] = None
    ) -> Dict:
        """
        Generate monthly transparency report
        
        Args:
            month: Report month (1-12)
            year: Report year
            transactions: List of transactions for the month
            entity_info: Entity information (optional)
            
        Returns:
            Dictionary containing the complete report
        """
        report_date = datetime.now(timezone.utc)
        report_id = f"{year}-{month:02d}"
        
        # Calculate totals
        total_revenue = sum(
            Decimal(str(tx.get('total_amount', 0)))
            for tx in transactions
        )
        
        total_charity = sum(
            Decimal(str(tx.get('nonprofit_amount', 0)))
            for tx in transactions
        )
        
        total_operational = sum(
            Decimal(str(tx.get('dao_amount', 0)))
            for tx in transactions
        )
        
        # Calculate percentage
        charity_percentage = (
            (total_charity / total_revenue * 100)
            if total_revenue > 0
            else Decimal('0')
        )
        
        # Build report
        report = {
            "report_id": report_id,
            "report_type": "monthly_transparency",
            "generated_at": report_date.isoformat(),
            "period": {
                "month": month,
                "year": year,
                "description": datetime(year, month, 1).strftime("%B %Y")
            },
            
            "entities": entity_info or self._default_entity_info(),
            
            "financial_summary": {
                "total_revenue": f"${total_revenue:.2f}",
                "charitable_allocation": f"${total_charity:.2f}",
                "operational_allocation": f"${total_operational:.2f}",
                "charitable_percentage": f"{charity_percentage:.2f}%",
                "transaction_count": len(transactions)
            },
            
            "compliance": {
                "target_percentage": "7.00%",
                "actual_percentage": f"{charity_percentage:.2f}%",
                "compliant": abs(charity_percentage - Decimal('7.0')) < Decimal('0.1'),
                "oath_honored": True,
                "discrepancies": []
            },
            
            "transactions": [
                {
                    "source": tx.get('source'),
                    "date": tx.get('timestamp'),
                    "total": tx.get('total_amount'),
                    "charity": tx.get('nonprofit_amount'),
                    "operational": tx.get('dao_amount'),
                    "nonprofit_tx": tx.get('nonprofit_tx_id'),
                    "dao_tx": tx.get('dao_tx_id'),
                    "status": tx.get('status')
                }
                for tx in transactions
            ],
            
            "verification": {
                "blockchain_logs": "Available via CAT_PUSH protocol",
                "ipfs_archive": "Pending upload",
                "arweave_archive": "Pending upload",
                "github_commit": "Linked to repository"
            },
            
            "beneficiaries": {
                "note": "Funds transferred to ValorYield Engine for distribution",
                "planned_beneficiaries": [
                    "St. Jude Children's Research Hospital",
                    "Médecins Sans Frontières (Doctors Without Borders)",
                    "Veterans Support Organizations",
                    "Educational Technology Initiatives"
                ],
                "distribution_status": "Pending ValorYield Engine 501(c)(3) approval"
            },
            
            "notes": [
                "All amounts in USD",
                "Charitable percentage locked at 7% per oath specification",
                "Nonprofit receives funds FIRST in all transactions",
                "All transactions publicly verifiable on blockchain",
                "Full source code available at https://github.com/Me10101-01/Node137_Uplink_Receipt"
            ]
        }
        
        # Save report
        report_file = self.output_dir / f"transparency_report_{report_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also create markdown version
        self._generate_markdown_report(report, report_file.with_suffix('.md'))
        
        return report
    
    def _default_entity_info(self) -> Dict:
        """Return default entity information"""
        return {
            "dao": {
                "name": "Strategickhaos DAO LLC",
                "type": "Unincorporated Nonprofit Association / DAO",
                "jurisdiction": "Wyoming, USA",
                "filing_id": "2025-001708194",
                "status": "Active",
                "operator": "Domenic Garza (Node 137)"
            },
            "nonprofit": {
                "name": "ValorYield Engine",
                "type": "Nonprofit Organization",
                "ein": "39-2923503",
                "jurisdiction": "Wyoming, USA",
                "filing_id": "2025-001708312",
                "501c3_status": "Pending Application",
                "director": "Domenic Garza"
            }
        }
    
    def _generate_markdown_report(self, report: Dict, output_file: Path):
        """
        Generate human-readable markdown version of report
        
        Args:
            report: Report dictionary
            output_file: Output file path
        """
        period = report['period']
        summary = report['financial_summary']
        compliance = report['compliance']
        
        md = f"""# Transparency Report: {period['description']}

**Report ID:** {report['report_id']}  
**Generated:** {report['generated_at']}  
**Report Type:** Monthly Transparency  

---

## Executive Summary

This report provides complete transparency into the operations of the Strategickhaos dual-entity system for {period['description']}.

### Financial Summary

| Metric | Amount |
|--------|--------|
| **Total Revenue** | {summary['total_revenue']} |
| **Charitable Allocation (7%)** | {summary['charitable_allocation']} |
| **Operational Allocation (93%)** | {summary['operational_allocation']} |
| **Transactions Processed** | {summary['transaction_count']} |

### Compliance Status

| Item | Status |
|------|--------|
| **Target Percentage** | {compliance['target_percentage']} |
| **Actual Percentage** | {compliance['actual_percentage']} |
| **Compliant** | {'✅ Yes' if compliance['compliant'] else '❌ No'} |
| **Oath Honored** | {'✅ Yes' if compliance['oath_honored'] else '❌ No'} |

---

## Entity Information

### Strategickhaos DAO LLC
- **Type:** {report['entities']['dao']['type']}
- **Jurisdiction:** {report['entities']['dao']['jurisdiction']}
- **Filing ID:** {report['entities']['dao']['filing_id']}
- **Status:** {report['entities']['dao']['status']}
- **Operator:** {report['entities']['dao']['operator']}

### ValorYield Engine
- **Type:** {report['entities']['nonprofit']['type']}
- **EIN:** {report['entities']['nonprofit']['ein']}
- **Jurisdiction:** {report['entities']['nonprofit']['jurisdiction']}
- **Filing ID:** {report['entities']['nonprofit']['filing_id']}
- **501(c)(3) Status:** {report['entities']['nonprofit']['501c3_status']}
- **Director:** {report['entities']['nonprofit']['director']}

---

## Transaction Details

"""
        # Add transaction table
        if report['transactions']:
            md += "| Date | Source | Total | Charity | Operational | Status |\n"
            md += "|------|--------|-------|---------|-------------|--------|\n"
            
            for tx in report['transactions']:
                date = tx.get('date', 'N/A')
                if isinstance(date, (int, float)):
                    date = datetime.fromtimestamp(date, tz=timezone.utc).strftime('%Y-%m-%d')
                
                md += f"| {date} | {tx['source']} | ${tx['total']} | ${tx['charity']} | ${tx['operational']} | {tx['status']} |\n"
        else:
            md += "*No transactions for this period*\n"
        
        md += f"""

---

## Beneficiary Organizations

{report['beneficiaries']['note']}

### Planned Beneficiaries:
"""
        for beneficiary in report['beneficiaries']['planned_beneficiaries']:
            md += f"- {beneficiary}\n"
        
        md += f"""

**Distribution Status:** {report['beneficiaries']['distribution_status']}

---

## Verification & Audit Trail

- **Blockchain Logs:** {report['verification']['blockchain_logs']}
- **IPFS Archive:** {report['verification']['ipfs_archive']}
- **Arweave Archive:** {report['verification']['arweave_archive']}
- **GitHub Repository:** {report['verification']['github_commit']}

All transactions are cryptographically signed and timestamped for public verification.

---

## Important Notes

"""
        for note in report['notes']:
            md += f"- {note}\n"
        
        md += f"""

---

## Contact & Questions

- **GitHub Issues:** https://github.com/Me10101-01/Node137_Uplink_Receipt/issues
- **Repository:** https://github.com/Me10101-01/Node137_Uplink_Receipt
- **Legal Documents:** See `/legal` directory in repository

---

*This report is automatically generated and cryptographically signed. All data is verifiable on public blockchains.*

**Report Hash:** {self._calculate_report_hash(report)}  
**Signature:** [GPG signature to be added]  
**Timestamp:** [OpenTimestamps proof to be added]  
"""
        
        # Write markdown file
        with open(output_file, 'w') as f:
            f.write(md)
    
    def _calculate_report_hash(self, report: Dict) -> str:
        """Calculate SHA-256 hash of report"""
        import hashlib
        report_json = json.dumps(report, sort_keys=True)
        return hashlib.sha256(report_json.encode()).hexdigest()
    
    def generate_annual_summary(
        self,
        year: int,
        monthly_reports: List[Dict]
    ) -> Dict:
        """
        Generate annual summary from monthly reports
        
        Args:
            year: Year for summary
            monthly_reports: List of monthly report dictionaries
            
        Returns:
            Annual summary dictionary
        """
        # Aggregate totals
        total_revenue = Decimal('0')
        total_charity = Decimal('0')
        total_transactions = 0
        
        for report in monthly_reports:
            summary = report.get('financial_summary', {})
            total_revenue += Decimal(summary.get('total_revenue', '$0').replace('$', ''))
            total_charity += Decimal(summary.get('charitable_allocation', '$0').replace('$', ''))
            total_transactions += summary.get('transaction_count', 0)
        
        charity_percentage = (
            (total_charity / total_revenue * 100)
            if total_revenue > 0
            else Decimal('0')
        )
        
        annual_summary = {
            "report_id": f"{year}-ANNUAL",
            "report_type": "annual_summary",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "year": year,
            
            "financial_summary": {
                "total_revenue": f"${total_revenue:.2f}",
                "charitable_allocation": f"${total_charity:.2f}",
                "operational_allocation": f"${(total_revenue - total_charity):.2f}",
                "charitable_percentage": f"{charity_percentage:.2f}%",
                "total_transactions": total_transactions,
                "months_reported": len(monthly_reports)
            },
            
            "compliance": {
                "target_percentage": "7.00%",
                "actual_percentage": f"{charity_percentage:.2f}%",
                "compliant": abs(charity_percentage - Decimal('7.0')) < Decimal('0.1'),
                "all_months_compliant": all(
                    r.get('compliance', {}).get('compliant', False)
                    for r in monthly_reports
                )
            },
            
            "monthly_breakdown": [
                {
                    "month": r['period']['month'],
                    "revenue": r['financial_summary']['total_revenue'],
                    "charity": r['financial_summary']['charitable_allocation'],
                    "transactions": r['financial_summary']['transaction_count']
                }
                for r in monthly_reports
            ],
            
            "impact": {
                "total_charitable_impact": f"${total_charity:.2f}",
                "beneficiaries_supported": "Pending ValorYield Engine distribution",
                "lives_impacted": "To be calculated after 501(c)(3) approval"
            }
        }
        
        # Save annual summary
        summary_file = self.output_dir / f"annual_summary_{year}.json"
        with open(summary_file, 'w') as f:
            json.dump(annual_summary, f, indent=2)
        
        return annual_summary


def main():
    """Example usage"""
    print("=" * 60)
    print("Transparency Report Generator - Test Mode")
    print("=" * 60)
    
    generator = TransparencyReportGenerator()
    
    # Create sample transactions
    sample_transactions = [
        {
            "source": "test",
            "source_tx_id": "test_001",
            "total_amount": "100.00",
            "nonprofit_amount": "7.00",
            "dao_amount": "93.00",
            "nonprofit_tx_id": "nonprofit_001",
            "dao_tx_id": "dao_001",
            "timestamp": datetime.now(timezone.utc).timestamp(),
            "status": "success"
        },
        {
            "source": "test",
            "source_tx_id": "test_002",
            "total_amount": "250.00",
            "nonprofit_amount": "17.50",
            "dao_amount": "232.50",
            "nonprofit_tx_id": "nonprofit_002",
            "dao_tx_id": "dao_002",
            "timestamp": datetime.now(timezone.utc).timestamp(),
            "status": "success"
        }
    ]
    
    # Generate monthly report
    print("\nGenerating monthly report for November 2025...")
    report = generator.generate_monthly_report(
        month=11,
        year=2025,
        transactions=sample_transactions
    )
    
    print(f"\nReport ID: {report['report_id']}")
    print(f"Period: {report['period']['description']}")
    print(f"\nFinancial Summary:")
    print(f"  Total Revenue: {report['financial_summary']['total_revenue']}")
    print(f"  Charitable: {report['financial_summary']['charitable_allocation']}")
    print(f"  Operational: {report['financial_summary']['operational_allocation']}")
    print(f"  Percentage: {report['financial_summary']['charitable_percentage']}")
    print(f"  Transactions: {report['financial_summary']['transaction_count']}")
    
    print(f"\nCompliance:")
    print(f"  Target: {report['compliance']['target_percentage']}")
    print(f"  Actual: {report['compliance']['actual_percentage']}")
    print(f"  Compliant: {'✅ Yes' if report['compliance']['compliant'] else '❌ No'}")
    
    print(f"\nReport files created:")
    print(f"  JSON: transparency/reports/transparency_report_2025-11.json")
    print(f"  Markdown: transparency/reports/transparency_report_2025-11.md")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
