from fastapi import Request, HTTPException, status
from typing import Optional, Dict

class FeatureGate:
    """
    Genius Constraint: FeatureGate ensures that capabilities are only unlocked 
    when the Wavefunction (License) supports it.
    """
    
    TIERS = {
        "Free": {"max_projects": 3, "advanced_advisors": False, "banking": False},
        "Professional": {"max_projects": 999, "advanced_advisors": True, "banking": False},
        "Enterprise": {"max_projects": 999, "advanced_advisors": True, "banking": False},
        "Banking_Advisory": {"max_projects": 999, "advanced_advisors": True, "banking": True},
    }

    @staticmethod
    async def check_license(request: Request, required_feature: Optional[str] = None):
        tier_name = request.headers.get("X-GADOS-Tier", "Free")
        tier_config = FeatureGate.TIERS.get(tier_name, FeatureGate.TIERS["Free"])
        
        if required_feature:
            if not tier_config.get(required_feature, False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "code": "FEATURE_LOCKED",
                        "message": f"Upgrade to {FeatureGate.required_tier(required_feature)} to unlock {required_feature}.",
                        "current_tier": tier_name
                    }
                )
        return tier_name

    @staticmethod
    def required_tier(feature: str) -> str:
        for name, config in FeatureGate.TIERS.items():
            if config.get(feature, False):
                return name
        return "Unknown"
