from python_framework.api.src.annotation.RepositoryAnnotation import Repository
from python_framework.api.src.model import ActuatorHealth

@Repository(model=ActuatorHealth.ActuatorHealth)
class ActuatorHealthRepository:

    def save(self, model):
        return self.repository.saveAndCommit(model)

    def findAll(self):
        return self.repository.findAllAndCommit(self.model)