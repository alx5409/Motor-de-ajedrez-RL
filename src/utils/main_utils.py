import sys
from engine.board import Board
from rl.agent import Agent
from rl.trainer import Trainer
from utils.config import Config
from utils.logger import Logger

def main():
    # Load configuration
    config = Config.load('config.json')

    # Initialize logger
    logger = Logger(config.log_file)

    # Initialize the chess board
    board = Board()

    # Initialize the reinforcement learning agent
    agent = Agent(config)

    # Initialize the trainer
    trainer = Trainer(agent, board, logger)

    # Start the training process
    trainer.train()

if __name__ == "__main__":
    main()