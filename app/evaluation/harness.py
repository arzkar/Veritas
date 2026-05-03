import os
import logging
from typing import Dict, Any, List
from app.schemas.epistemic import GlobalInvestigationState, EpistemicStatus
import json

logger = logging.getLogger(__name__)

class EvalHarness:
    """
    Service for evaluating Veritas investigation quality using synthetic benchmarks.
    """
    
    def __init__(self):
        self.results = []

    def load_benchmark(self, file_path: str) -> Dict[str, Any]:
        """
        Loads a benchmark deck definition (ground truth claims and seeded contradictions).
        """
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r") as f:
            return json.load(f)

    def calculate_red_flag_recall(self, state: GlobalInvestigationState, ground_truth: List[Dict[str, Any]]) -> float:
        """
        Measures how many seeded contradictions (red flags) were successfully detected.
        """
        detected_flags = [
            c for c in state.claims.values() 
            if c.belief in [EpistemicStatus.CONTRADICTED, EpistemicStatus.DEBUNKED, EpistemicStatus.SUSPICIOUSLY_ABSENT]
        ]
        
        seeded_flags = [c for c in ground_truth if c.get("is_contradiction")]
        
        if not seeded_flags:
            return 1.0
            
        matches = 0
        for seeded in seeded_flags:
            for detected in detected_flags:
                # Basic semantic match or shared keyword
                if seeded["key_term"].lower() in detected.statement.lower():
                    matches += 1
                    break
                    
        recall = matches / len(seeded_flags)
        return recall

    def measure_calibration_error(self, state: GlobalInvestigationState) -> float:
        """
        Simple Expected Calibration Error (ECE) proxy.
        Measures if system confidence correlates with analysis status.
        High confidence on AMBIGUOUS claims increases error.
        """
        errors = []
        for claim in state.claims.values():
            if claim.belief == EpistemicStatus.AMBIGUOUS:
                # Error is high if confidence is high but status is ambiguous
                errors.append(claim.confidence.aggregate)
            elif claim.belief in [EpistemicStatus.SUPPORTED, EpistemicStatus.CONTRADICTED]:
                # Error is high if confidence is low but we made a hard decision
                errors.append(1.0 - claim.confidence.aggregate)
                
        if not errors:
            return 0.0
            
        return sum(errors) / len(errors)

    def generate_eval_report(self, state: GlobalInvestigationState, ground_truth: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates a comprehensive evaluation report for a single investigation.
        """
        recall = self.calculate_red_flag_recall(state, ground_truth)
        calibration = self.measure_calibration_error(state)
        
        report = {
            "document_id": state.document_id,
            "red_flag_recall": round(recall, 2),
            "calibration_error": round(calibration, 2),
            "claims_processed": len(state.claims),
            "global_score": state.global_credibility_score,
            "passed_benchmark": recall > 0.8 and calibration < 0.3
        }
        
        return report
