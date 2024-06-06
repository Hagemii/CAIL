
# Requirements

The model is implemented using PyTorch. The versions of packages used are shown below.

+ numpy==1.18.0
+ scikit-learn==0.22.1
+ scipy==1.4.1
+ torch==1.4.0
+ tqdm==4.41.1
+ transformers==4.0.0

To set up the dependencies, you can run the following command:
``` bash
pip install -r requirements.txt
```

## Reproduce Results in Our Work

### 1. For TACRED

```bash
bash scipts/run_large_tacred.sh
```

### 2. For TACREV

```bash
bash scripts/run_large_tacrev.sh
```

### 3. For RETACRED

```bash
bash scripts/run_large_retacred.sh
```

### 4. For Semeval

```bash
bash scripts/run_large_semeval.sh
```

