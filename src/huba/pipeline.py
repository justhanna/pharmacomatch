import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
from pydantic import ValidationError

from src.huba.reader import PatientDataReader
from src.huba.validator import GeneticVariantRecord


class HubaBatchPipeline:
    """Orkiestrator batchowy przetwarzający surowe pliki do ustrukturyzowanego formatu."""

    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed", log_dir: str = "data/logs"):
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.log_dir = Path(log_dir)

        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.reader = PatientDataReader()
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(f"HUBA_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        logger.setLevel(logging.INFO)
        log_file = self.log_dir / "huba_execution.log"

        if not logger.handlers:
            handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def run(self) -> Dict[str, Any]:
        supported_extensions = [".csv", ".tsv", ".vcf"]
        files = [p for p in self.raw_dir.glob("*") if p.suffix.lower() in supported_extensions]

        summary = {
            "timestamp": datetime.now().isoformat(),
            "processed_files_count": 0,
            "total_valid_records": 0,
            "total_rejected_records": 0,
            "file_reports": []
        }

        for file_path in sorted(files):
            file_report = {
                "file_name": file_path.name,
                "status": "SUCCESS",
                "valid_count": 0,
                "rejected_count": 0,
                "errors": []
            }
            self.logger.info(f"Starting ingestion for file: {file_path.name}")

            try:
                raw_df = self.reader.load(file_path)
                valid_records: List[Dict[str, Any]] = []

                for idx, row in raw_df.iterrows():
                    row_dict = row.to_dict()
                    if "sample_id" not in row_dict or pd.isna(row_dict["sample_id"]):
                        row_dict["sample_id"] = file_path.stem

                    try:
                        record = GeneticVariantRecord(**row_dict)
                        valid_records.append(record.model_dump())
                        file_report["valid_count"] += 1
                        summary["total_valid_records"] += 1
                    except ValidationError as ve:
                        file_report["rejected_count"] += 1
                        summary["total_rejected_records"] += 1
                        reasons = [f"{err['loc'][0]}: {err['msg']}" for err in ve.errors()]
                        err_msg = f"Row {idx} rejected: {', '.join(reasons)}"
                        file_report["errors"].append(err_msg)
                        self.logger.warning(f"Validation rejected in {file_path.name}: {err_msg}")

                if valid_records:
                    cleaned_df = pd.DataFrame(valid_records)
                    out_path = self.processed_dir / f"{file_path.stem}_cleaned.parquet"
                    cleaned_df.to_parquet(out_path, index=False)
                    self.logger.info(f"Written cleaned dataset to {out_path.name}")

                file_report["status"] = "PROCESSED_WITH_WARNINGS" if file_report["rejected_count"] > 0 else "CLEAN"
                summary["processed_files_count"] += 1

            except Exception as exc:
                file_report["status"] = "FAILED"
                file_report["errors"].append(str(exc))
                self.logger.error(f"Critical failure while processing {file_path.name}: {str(exc)}")

            summary["file_reports"].append(file_report)

        summary_file = self.log_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        self.logger.info(f"Batch completed. Summary saved to {summary_file.name}")
        return summary