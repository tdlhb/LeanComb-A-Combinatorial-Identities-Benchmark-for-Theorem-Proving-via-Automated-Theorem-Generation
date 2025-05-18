Sure! Here's the English translation of your README content:

---

## Project Structure

```
theorem_search/
├── models/             # Weights for the policy and value networks  
├── utils/              
│   └── lean4Kit/       # Tools for interacting with Lean4  
│   └── Constrant.py    # Configuration information  
│   └── model.py        # Network architectures for policy and value networks  
│   └── ModelActor.py   # Multi-model concurrent inference manager  
│   └── MyTheorem.py    # Lean4 theorem class  
│   └── repair.py       # Repair logic  
│   └── Searcher_alphazero.py  # Theorem search engine guided by AlphaZero strategy  
│   └── Searcher.py     # Concurrent search management module  
│   └── tools.py        # Utility functions  
├── corrector.py        # Verify and enhance the theorems found during search  
├── eval.py             # Evaluate model performance  
├── search_alphazeropy.py  # Use AlphaZero method to enhance data  
└── requirements.txt  
└── README.md  
```

### Setup Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

First, update configuration details (e.g., Lean4 working directory, language model path, etc.) in `Constrant.py`.

---

### Data Augmentation Workflow

1. Use the `run_allTactics` method in `Lean4Kit.py` to convert `.lean` files into `.json` files.
2. Update the `.json` file path in `search_alphazeropy.py` and run:

```bash
python search_alphazeropy.py
```

---

### Verification of Augmented Data

1. Update the file path of the searched/augmented data in `corrector.py`.
2. Run:

```bash
python corrector.py
```

---

### Model Evaluation

1. Set paths for `task_file`, `record_file`, etc. in `eval.py`.
2. Run:

```bash
python eval.py
```

