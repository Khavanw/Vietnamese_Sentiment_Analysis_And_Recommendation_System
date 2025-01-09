import torch
from torch import nn
from transformers import RobertaConfig, RobertaModel, RobertaPreTrainedModel

class RobertaForAIViVN(RobertaPreTrainedModel):
    config_class = RobertaConfig
    base_model_prefix = "roberta"

    def __init__(self, config):
        super(RobertaForAIViVN, self).__init__(config)
        self.num_labels = config.num_labels
        self.roberta = RobertaModel(config)
        self.qa_outputs = nn.Linear(4*config.hidden_size, self.num_labels)

        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None,
                labels=None):
        outputs = self.roberta(input_ids,
                               attention_mask=attention_mask,
                               position_ids=position_ids,
                               head_mask=head_mask)
        cls_output = torch.cat((outputs.last_hidden_state[:,0, :],
                                outputs.hidden_states[-1][:,0, :],
                                outputs.hidden_states[-2][:,0, :],
                                outputs.hidden_states[-3][:,0, :]), -1)
        logits = self.qa_outputs(cls_output)

        # Tính toán loss nếu labels được cung cấp
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits, labels)
            return loss, logits
        return logits
