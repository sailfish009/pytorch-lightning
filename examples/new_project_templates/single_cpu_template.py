"""
Runs a model on a single node on CPU only..
"""
import os
import numpy as np
import torch

from test_tube import HyperOptArgumentParser, Experiment
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint

from examples.new_project_templates.lightning_module_template import LightningTemplateModel

SEED = 2334
torch.manual_seed(SEED)
np.random.seed(SEED)


def main(hparams):
    """
    Main training routine specific for this project
    :param hparams:
    :return:
    """
    # ------------------------
    # 1 INIT LIGHTNING MODEL
    # ------------------------
    model = LightningTemplateModel(hparams)

    # ------------------------
    # 2 INIT EXP
    # ------------------------
    # init experiment
    exp = Experiment(
        name=hyperparams.experiment_name,
        save_dir=hyperparams.test_tube_save_path,
        autosave=False,
        description='test demo'
    )

    exp.argparse(hparams)
    exp.save()

    # ------------------------
    # 3 INIT TRAINER
    # ------------------------
    trainer = Trainer(experiment=exp)

    # ------------------------
    # 4 START TRAINING
    # ------------------------
    trainer.fit(model)


if __name__ == '__main__':

    # dirs
    root_dir = os.path.dirname(os.path.realpath(__file__))
    demo_log_dir = os.path.join(root_dir, 'pt_lightning_demo_logs')
    checkpoint_dir = os.path.join(demo_log_dir, 'model_weights')
    test_tube_dir = os.path.join(demo_log_dir, 'test_tube_data')

    # although we user hyperOptParser, we are using it only as argparse right now
    parent_parser = HyperOptArgumentParser(strategy='grid_search', add_help=False)

    # gpu args
    parent_parser.add_argument('--test_tube_save_path', type=str,
                               default=test_tube_dir, help='where to save logs')
    parent_parser.add_argument('--model_save_path', type=str,
                               default=checkpoint_dir, help='where to save model')
    parent_parser.add_argument('--experiment_name', type=str,
                               default='pt_lightning_exp_a', help='test tube exp name')

    # allow model to overwrite or extend args
    parser = LightningTemplateModel.add_model_specific_args(parent_parser, root_dir)
    hyperparams = parser.parse_args()

    # ---------------------
    # RUN TRAINING
    # ---------------------
    # run on HPC cluster
    print('RUNNING ON CPU')
    main(hyperparams)
