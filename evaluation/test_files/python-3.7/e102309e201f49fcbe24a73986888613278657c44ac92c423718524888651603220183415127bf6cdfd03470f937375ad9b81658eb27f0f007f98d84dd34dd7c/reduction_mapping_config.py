"""
Module that defines the ReductionMappingConfig that is used in the
mlcvzoo_base.data_preparation.annotation_class_mapper.AnnotationClassMapper.
"""
import logging
from typing import Dict, List, Optional
import related
from config_builder import BaseConfigClass
logger = logging.getLogger(__name__)

@related.mutable(strict=True)
class ReductionMappingMappingConfig(BaseConfigClass):
    """
    A ReductionMappingMappingConfig entry defines how model class IDs / names should
    be mapped to an output class ID and output class name. This can be used to aggregate
    or redefine model classes.
    """
    mutual_attribute_map: Dict[str, List[str]] = {'ReductionMappingMappingConfig': ['model_class_ids', 'model_class_names']}
    output_class_name: str = related.StringField()
    output_class_id: int = related.IntegerField()
    model_class_ids: Optional[List[int]] = related.ChildField(cls=list, required=False, default=None)
    model_class_names: Optional[List[str]] = related.ChildField(cls=list, required=False, default=None)

    def check_values(self) -> bool:
        success: bool = True
        if self.model_class_ids is not None:
            for model_class_id in self.model_class_ids:
                if not isinstance(model_class_id, int):
                    logger.info("model_class_ids have to be integer values! model_class_id: '%s'" % self.model_class_ids)
                    return False
        if self.model_class_names is not None:
            for model_class_name in self.model_class_names:
                if not isinstance(model_class_name, str):
                    logger.info("model_class_names have to be string values! model_class_names: '%s'" % self.model_class_names)
                    return False
        return success

@related.mutable(strict=True)
class ReductionMappingConfig(BaseConfigClass):
    """
    After a model has been trained, it will generate predictions that only include the class IDs
    or class names, it has been trained on. In order to be able to aggregate or adapt the relation
    between class IDs and class names the reduction_mapping can be used.
    """
    mapping: List[ReductionMappingMappingConfig] = related.SequenceField(ReductionMappingMappingConfig)