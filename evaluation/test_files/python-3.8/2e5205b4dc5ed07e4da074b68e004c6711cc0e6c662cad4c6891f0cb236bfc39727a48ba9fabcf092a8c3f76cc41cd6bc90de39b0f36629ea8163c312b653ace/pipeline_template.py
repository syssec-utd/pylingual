"""! @brief Pipeline class, implements ZIDS_Pipeline base class."""
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
from dsframework.base.pipeline.pipeline import ZIDS_Pipeline
from .preprocessor.preprocess import generatedProjectNamePreprocess
from .postprocessor.postprocess import generatedProjectNamePostprocess
from .predictors.predictor import generatedProjectNamePredictor
from .forcers.forcer import generatedProjectNameForcer
from .artifacts.shared_artifacts import generatedProjectNameSharedArtifacts

class generatedClass(ZIDS_Pipeline):
    """! Pipeline main class

    Its main job is to build the pipeline components by default it includes four main components:
    preprocess, predictor, forcer and postprocess.
    """

    def __init__(self):
        """! The generatedClass class (Pipeline) initializer."""
        super().__init__()

    def get_artifacts(self):
        """! Loads the artifacts and return the results.

        It triggers execution of load_artifacts and load_vocabs on base  ZIDS_SharedArtifacts,
        overrides ZIDS_Pipeline.get_artifacts.


        Returns:
             generatedProjectNameSharedArtifacts() - Results of loaded artifacts.

        """
        return generatedProjectNameSharedArtifacts()

    def build_pipeline(self):
        """! Builds the pipeline.

        Instantiate the default four main components:
        Preprocessor, Predictor, Forcer and Postprocessor.
        """
        self.preprocessor = generatedProjectNamePreprocess(artifacts=self.artifacts)
        self.predictor = generatedProjectNamePredictor()
        self.add_component(self.predictor)
        self.forcer = generatedProjectNameForcer()
        self.add_component(self.forcer)
        self.postprocessor = generatedProjectNamePostprocess(artifacts=self.artifacts)

    def preprocess(self, **kwargs):
        """! Executes preprocessor, called from pipeline execute method.

        Args:
            **kwargs : Dataset and additional parameters loaded initially.
        Returns:
            List of predictable objects (generatedProjectNameInputs datatype)
        """
        return self.preprocessor(**kwargs)

    def postprocess(self, predictables):
        """! Executes the postprocessor, called from pipeline execute method.

        Args:
            predictables: List[generatedProjectNameInputs] - List of predictable objects.
        Returns:
            generatedProjectNamePostprocess: List[generatedProjectNameOutputs]: List of results.
        """
        return self.postprocessor(predictables)