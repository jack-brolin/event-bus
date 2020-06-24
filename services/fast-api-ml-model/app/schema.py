from pydantic import BaseModel


class LogisticRegressionParameters(BaseModel):
    max_iter: int
    c: int
    random_state: int
    penalty: str


class GradientBoostingClassifier(BaseModel):
    learning_rate: float
    n_estimators: int
    subsample: float
    min_samples_split: int
    min_samples_leaf: int
    max_depth: int
