#!/usr/bin/env python3
"""
Example: Using the Document Refinery programmatically.

This demonstrates how to:
1. Initialize the Document Refinery
2. Add models for evaluation
3. Ingest and parse documents
4. Run comprehensive evaluations
5. Generate anti-fragility reports
"""

from pathlib import Path
from document_refinery import DocumentRefinery
from document_refinery.models import LocalModelAdapter

def main():
    print("=" * 60)
    print("Strategickhaos Document Refinery - Example Usage")
    print("=" * 60)
    
    # 1. Initialize the Document Refinery
    print("\n📋 Initializing Document Refinery...")
    refinery = DocumentRefinery()
    
    # 2. Add a model for evaluation
    print("🤖 Adding local model adapter...")
    model = LocalModelAdapter({
        "model_name": "example-local-model",
        "model_path": "./models/local",
        "device": "cpu",
    })
    refinery.add_model("local-model", model)
    
    # 3. Prepare documents for evaluation
    print("\n📄 Preparing documents...")
    document_paths = [
        Path("document_refinery/examples/sample_nda.md"),
        Path("document_refinery/examples/sample_dpa.md"),
    ]
    
    # Check if documents exist
    for doc_path in document_paths:
        if not doc_path.exists():
            print(f"⚠️  Warning: {doc_path} not found")
    
    # 4. Ingest documents
    print("\n🔍 Ingesting and parsing documents...")
    documents = refinery.ingest_documents(document_paths)
    print(f"   Parsed {len(documents)} document(s)")
    
    for doc_path, parsed_doc in documents.items():
        print(f"\n   📄 {Path(doc_path).name}")
        print(f"      Title: {parsed_doc.title}")
        print(f"      Chunks: {len(parsed_doc.chunks)}")
        print(f"      Words: {parsed_doc.metadata.get('word_count', 0)}")
    
    # 5. Run evaluation
    print("\n🔬 Running Red/Blue/Purple team evaluation...")
    print("   This will test:")
    print("   - 🔴 Red Team: Adversarial attacks (hallucinations, prompt injection, etc.)")
    print("   - 🔵 Blue Team: Defense checks (guardrails, PII protection, etc.)")
    print("   - 🟣 Purple Team: Comprehensive metrics and resilience scoring")
    
    results = refinery.evaluate(documents)
    
    # 6. Display summary
    print("\n📊 Evaluation Summary:")
    for model_name, model_results in results.get("models", {}).items():
        print(f"\n   Model: {model_name}")
        
        # Purple team overall score
        purple_results = model_results.get("purple_team", {})
        overall_score = purple_results.get("overall_score", 0.0)
        print(f"   Overall Anti-Fragility Score: {overall_score:.1%}")
        
        # Red team summary
        red_results = model_results.get("red_team", {})
        print(f"\n   🔴 Red Team:")
        print(f"      Total Attacks: {red_results.get('total_attacks', 0)}")
        print(f"      Successful Attacks: {red_results.get('successful_attacks', 0)}")
        print(f"      Attack Success Rate: {red_results.get('success_rate', 0):.1%}")
        
        # Blue team summary
        blue_results = model_results.get("blue_team", {})
        print(f"\n   🔵 Blue Team:")
        print(f"      Total Checks: {blue_results.get('total_checks', 0)}")
        print(f"      Passed Checks: {blue_results.get('passed_checks', 0)}")
        print(f"      Defense Score: {blue_results.get('defense_score', 0):.1%}")
        
        # Risk assessment
        risks = purple_results.get("risk_assessment", {})
        critical_count = len(risks.get("critical", []))
        high_count = len(risks.get("high", []))
        
        if critical_count > 0 or high_count > 0:
            print(f"\n   ⚠️  Risks Identified:")
            print(f"      Critical: {critical_count}")
            print(f"      High: {high_count}")
    
    # 7. Generate reports
    print("\n📝 Generating reports...")
    output_dir = Path("./refinery_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    reports = {
        "anti_fragility": refinery.generate_report(
            results,
            output_dir / "anti_fragility_report.md",
            "anti_fragility"
        ),
        "governance": refinery.generate_report(
            results,
            output_dir / "governance_report.md",
            "governance"
        ),
    }
    
    print("\n✅ Reports generated:")
    for report_type, report_path in reports.items():
        print(f"   - {report_type}: {report_path}")
    
    print("\n" + "=" * 60)
    print("✨ Example complete!")
    print("\nNext steps:")
    print("1. Review the anti-fragility report for detailed findings")
    print("2. Review the governance report for compliance insights")
    print("3. Address any critical or high risks identified")
    print("4. Re-run evaluation to verify improvements")
    print("=" * 60)


if __name__ == "__main__":
    main()
