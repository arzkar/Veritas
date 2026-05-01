from app.schemas.epistemic import GlobalInvestigationState, Claim, EpistemicStatus
import logging

logger = logging.getLogger(__name__)

class BeliefEngine:
    """
    Engine responsible for calculating global credibility scores using 
    Bayesian-inspired belief revision.
    """
    
    def __init__(self, alpha: float = 0.5, beta: float = 0.05):
        self.alpha = alpha  # Severity factor for contradictions
        self.beta = beta    # Trust factor for validations

    def update_global_score(self, state: GlobalInvestigationState) -> float:
        """
        Calculates the global_credibility_score based on claim analysis results.
        Asymmetric: Trust is harder to build than it is to destroy.
        """
        current_score = 0.85 # Optimistic prior
        red_flag_count = 0
        
        # Sort claims by importance (high importance updates first)
        sorted_claims = sorted(
            state.claims.values(), 
            key=lambda x: x.importance, 
            reverse=True
        )
        
        for claim in sorted_claims:
            confidence = claim.confidence.aggregate
            
            if claim.belief == EpistemicStatus.CONTRADICTED or claim.belief == EpistemicStatus.DEBUNKED:
                # Multiplicative Decay
                penalty = claim.importance * confidence * self.alpha
                current_score *= (1 - penalty)
                red_flag_count += 1
                
            elif claim.belief == EpistemicStatus.SUSPICIOUSLY_ABSENT:
                # Significant Decay
                penalty = claim.importance * confidence * (self.alpha * 0.6)
                current_score *= (1 - penalty)
                red_flag_count += 1
                
            elif claim.belief == EpistemicStatus.SUPPORTED:
                # Marginal Additive Increase
                bonus = claim.importance * confidence * self.beta
                current_score = min(1.0, current_score + bonus)
                
            elif claim.belief == EpistemicStatus.AMBIGUOUS:
                # Small Decay due to uncertainty
                current_score *= 0.98
        
        state.global_credibility_score = round(current_score, 2)
        state.red_flag_count = red_flag_count
        
        return state.global_credibility_score
