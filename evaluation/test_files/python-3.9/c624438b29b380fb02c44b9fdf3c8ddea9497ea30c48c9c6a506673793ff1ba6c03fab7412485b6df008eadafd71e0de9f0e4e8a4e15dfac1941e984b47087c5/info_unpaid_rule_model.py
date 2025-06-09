from typing import Any, Dict, List
from sktmls.models import MLSModelError, MLSRuleModel

class InfoUnpaidRuleModel(MLSRuleModel):

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if len(self.features) != len(x):
            raise MLSModelError('The length of input is different from that of features in model.json')
        filter_col = x[0]
        if filter_col != 'Y':
            return {'items': []}
        else:
            return {'items': [{'id': 'INF0000001', 'name': '미납 요금 및 납부 안내', 'type': 'info_unpaid', 'props': {}}]}