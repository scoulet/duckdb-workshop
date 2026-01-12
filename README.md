# DuckDB vs. Pandas: Analytical Benchmark

This project demonstrates the performance gap between **Pandas** (In-memory/Row-based processing) and **DuckDB** (Out-of-core/Vectorized/Columnar processing). 

It is designed as a teaching resource to illustrate why modern analytical engines are moving towards "Streaming" architectures for datasets that exceed available RAM.

## 🚀 The Challenge
We process a **5,000,000 row** healthcare dataset to calculate the average BMI per hospital service for patients over 50.

### Key Technical Concepts
- **Stateless vs. Stateful**: DuckDB filters data in a streaming (stateless) fashion, keeping only the small aggregation results in memory (stateful).
- **Columnar Storage**: Using Parquet, DuckDB only reads the columns required for the calculation (`age`, `imc`, `service`), ignoring the rest.
- **Out-of-core Processing**: Unlike Pandas, DuckDB can process datasets larger than your RAM by "spilling" to disk if necessary.



## 🛠 Prerequisites
This project uses **uv**, an extremely fast Python package installer and resolver written in Rust.

If you don't have it yet, install it via:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

```

## 📦 Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/duckdb-workshop.git](https://github.com/your-username/duckdb-workshop.git)
cd duckdb-workshop

```


2. **Sync the environment:**
```bash
uv sync

```



## 🏃 Usage

Run the benchmark script directly with `uv`:

```bash
uv run main.py

```

## 📊 Expected Output

The script will:

1. Generate a 5M row `.parquet` file.
2. Run the analysis using **Pandas** (loading the full file into memory).
3. Run the analysis using **DuckDB** (streaming directly from the file).
4. Print a performance comparison.

> **Note:** On most laptops, DuckDB is expected to be **5x to 10x faster** than Pandas for this specific analytical task.