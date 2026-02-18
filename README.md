# Reinforcement Learning Game Project

## Overview

This project focuses on designing a complete game environment and training intelligent agents using **Reinforcement Learning**, specifically the **Q-Learning algorithm**.
The objective is to build an autonomous agent capable of learning optimal decisions through interaction with the environment over multiple training episodes.

The project covers environment design, agent implementation, training, and evaluation.

---

## Objectives

* Design a fully functional **game environment**
* Implement the **Reinforcement Learning framework**
* Develop multiple agents with different strategies
* Train an agent using **Q-Learning**
* Evaluate learning performance and behavior

---

## Project Components

### 1. Environment

The environment represents the game and defines:

* State representation
* Action space
* Reward system
* Terminal conditions (win / lose / draw)
* `step(action)` function to execute a move and return:

  * next_state
  * reward
  * done flag

---

### 2. Agents

Different agents are implemented for comparison:

* **Random Agent**
  Chooses actions randomly (baseline performance).

* **Q-Learning Agent**
  Learns optimal behavior using a Q-table and improves over time through experience.

---

### 3. Reinforcement Learning (Q-Learning)

The learning process follows:

```
Q(s, a) ← Q(s, a) + α [ r + γ max Q(s', a') − Q(s, a) ]
```

Where:

* `s` = current state
* `a` = action taken
* `r` = reward received
* `s'` = next state
* `α` = learning rate
* `γ` = discount factor

The agent balances:

* **Exploration** → trying new actions
* **Exploitation** → using learned best actions

---

### 4. Training

The agent is trained over many episodes:

* Reset environment
* Interact step-by-step
* Update Q-values
* Gradually reduce exploration (epsilon decay)

---

### 5. Evaluation

After training, the agent is tested to measure:

* Win rate / success rate
* Learning improvement
* Stability of decisions

---

## Authors

Project developed as part of a Reinforcement Learning / Intelligent Systems study project.
