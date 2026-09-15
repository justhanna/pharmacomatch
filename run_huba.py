from src.huba.pipeline import HubaBatchPipeline


def main():
    print("=== HUBA (Hybrid Unified Batch Analyzer) ===")
    print("Running batch data integration and validation pipeline...")

    pipeline = HubaBatchPipeline(
        raw_dir="data/raw",
        processed_dir="data/processed",
        log_dir="data/logs"
    )

    summary = pipeline.run()

    print("\n--- Pipeline Summary ---")
    print(f"Files Processed:        {summary['processed_files_count']}")
    print(f"Valid Records Cleaned:  {summary['total_valid_records']}")
    print(f"Rejected Records:       {summary['total_rejected_records']}")
    print("Detailed report written to data/logs/")


if __name__ == "__main__":
    main()