from configuration import ModelConfig, DeployConfig
from generator import TextGenerator

model_config = ModelConfig().get_args()
deploy_config = DeployConfig().get_args()

model_config.inf_model = 'finetuned'
model = TextGenerator(model_config, deploy_config)

text = "trump posthumously pardons boxer jack johnson"

gen = model.generate(text, 3)