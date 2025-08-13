# Spotify History Analysis

This project analyzes your Spotify listening history to provide insights into your listening patterns, top artists, top tracks, and more. It includes a Jupyter Notebook for detailed analysis and a Streamlit dashboard for a more interactive experience.

## Dataset

The dataset used in this project is `spotify_history.csv`, which contains your Spotify listening history. You can download your own data from your Spotify account settings.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/spotify-history-analysis.git
```

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your `spotify_history.csv` file in the root directory of the project.
2. Run the Jupyter Notebook to see the detailed analysis:
```bash
jupyter notebook analysis.ipynb
```
3. Run the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

## Analysis

The `analysis.ipynb` notebook contains a detailed analysis of the Spotify listening history, including:
- Top 10 artists by play count
- Top 10 tracks by play count
- Total playtime
- Distribution of playtimes
- Most frequent platforms
- Time of day analysis
- Skip rate analysis
- Shuffle usage analysis

## Dashboard

The `dashboard.py` file contains a Streamlit dashboard that provides a more interactive way to explore your listening history. The dashboard includes:
- Top 10 artists by play count
- Top 10 tracks by play count
- Total playtime
- Distribution of playtimes
- Most frequent platforms
- Time of day analysis

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
