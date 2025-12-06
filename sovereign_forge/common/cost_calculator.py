#!/usr/bin/env python3
"""
Cost Reduction Calculator

Calculates potential savings from replacing SaaS vendors
with sovereign self-hosted alternatives.
"""

import argparse
from dataclasses import dataclass
from typing import List
import json


@dataclass
class Vendor:
    name: str
    annual_cost: float
    users: int = 1
    plan: str = ""


@dataclass
class SovereignReplacement:
    name: str
    vendor: str
    infrastructure_cost: float
    development_hours: int
    annual_savings: float
    roi_months: int


class CostCalculator:
    def __init__(self):
        self.vendors = []
        self.infrastructure_base_cost = 132.0  # Annual base infra cost
    
    def add_vendor(self, name: str, annual_cost: float, users: int = 1, plan: str = ""):
        """Add a vendor to the cost analysis"""
        self.vendors.append(Vendor(name, annual_cost, users, plan))
    
    def calculate_savings(self, development_hours: int = 0) -> dict:
        """Calculate total savings from sovereign replacements"""
        total_vendor_cost = sum(v.annual_cost for v in self.vendors)
        annual_savings = total_vendor_cost - self.infrastructure_base_cost
        savings_percentage = (annual_savings / total_vendor_cost * 100) if total_vendor_cost > 0 else 0
        
        # Calculate ROI (assuming $50/hr development cost)
        development_cost = development_hours * 50
        roi_months = (development_cost / annual_savings * 12) if annual_savings > 0 else 0
        
        return {
            'vendor_costs': {
                'total_annual': total_vendor_cost,
                'vendors': [
                    {
                        'name': v.name,
                        'annual_cost': v.annual_cost,
                        'users': v.users,
                        'plan': v.plan
                    }
                    for v in self.vendors
                ]
            },
            'sovereign_costs': {
                'infrastructure_annual': self.infrastructure_base_cost,
                'development_one_time': development_cost,
                'development_hours': development_hours
            },
            'savings': {
                'annual': annual_savings,
                'percentage': savings_percentage,
                'five_year': annual_savings * 5,
                'roi_months': round(roi_months, 1)
            }
        }
    
    def generate_report(self) -> str:
        """Generate human-readable savings report"""
        calc = self.calculate_savings()
        
        report = f"""
# 💰 Sovereign Software Forge - Cost Reduction Analysis

## Current Vendor Spend (Annual)

"""
        for vendor in calc['vendor_costs']['vendors']:
            report += f"- **{vendor['name']}** ({vendor['plan']}): ${vendor['annual_cost']:.2f}\n"
        
        report += f"\n**Total Annual Vendor Cost**: ${calc['vendor_costs']['total_annual']:.2f}\n"
        
        report += f"""

## Sovereign Stack Cost (Annual)

- **Infrastructure**: ${calc['sovereign_costs']['infrastructure_annual']:.2f}
  - Kubernetes cluster: $0 (existing/edu credits)
  - Domain/DNS: $12
  - Electricity: ~$120

**Total Annual Sovereign Cost**: ${calc['sovereign_costs']['infrastructure_annual']:.2f}

---

## 💎 Cost Savings

- **Annual Savings**: ${calc['savings']['annual']:.2f}
- **Savings Percentage**: {calc['savings']['percentage']:.1f}%
- **5-Year Savings**: ${calc['savings']['five_year']:.2f}

## 📊 Return on Investment

- **Development Cost (One-Time)**: ${calc['sovereign_costs']['development_one_time']:.2f}
- **Development Hours**: {calc['sovereign_costs']['development_hours']}
- **ROI Break-Even**: {calc['savings']['roi_months']} months

---

## Recommendation

"""
        if calc['savings']['roi_months'] < 12:
            report += "✅ **HIGHLY RECOMMENDED** - ROI break-even in less than 1 year\n"
        elif calc['savings']['roi_months'] < 24:
            report += "✅ **RECOMMENDED** - ROI break-even in less than 2 years\n"
        else:
            report += "⚠️ **EVALUATE** - ROI break-even takes longer, consider strategic value\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Calculate cost savings from sovereign replacements"
    )
    parser.add_argument(
        '--config',
        help="JSON config file with vendor costs"
    )
    parser.add_argument(
        '--output',
        help="Output file for report (default: stdout)"
    )
    parser.add_argument(
        '--format',
        choices=['markdown', 'json'],
        default='markdown',
        help="Output format"
    )
    
    args = parser.parse_args()
    
    calculator = CostCalculator()
    
    if args.config:
        # Load from config file
        with open(args.config) as f:
            config = json.load(f)
            for vendor in config.get('vendors', []):
                calculator.add_vendor(
                    vendor['name'],
                    vendor['annual_cost'],
                    vendor.get('users', 1),
                    vendor.get('plan', '')
                )
    else:
        # Default example
        calculator.add_vendor("Airtable", 240, 1, "Team")
        calculator.add_vendor("Zapier", 240, 1, "Starter")
        calculator.add_vendor("GitHub Enterprise", 252, 1, "Trial→Paid")
        calculator.add_vendor("Notion", 120, 1, "Plus")
        calculator.add_vendor("Slack", 84, 1, "Pro")
        calculator.add_vendor("Various SaaS", 500, 1, "Misc")
    
    if args.format == 'json':
        result = calculator.calculate_savings(development_hours=280)
        output = json.dumps(result, indent=2)
    else:
        output = calculator.generate_report()
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ Report saved to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
