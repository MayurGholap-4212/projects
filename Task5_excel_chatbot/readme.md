# 📊 Excel Analytics Chatbot with Open-Source LLM

A comprehensive chatbot solution for analyzing Excel and CSV data using open-source Large Language Models (LLMs). This project combines the power of natural language processing with traditional data analysis to provide intelligent insights from your datasets.

## 🌟 Features

### Core Capabilities
- **Multi-format Support**: Excel (.xlsx, .xls) and CSV files
- **Open-Source LLM Integration**: Uses GPT-2, DialoGPT, or CodeGen models
- **Intelligent Data Analysis**: Automatic statistical analysis and pattern detection
- **Semantic Search**: Advanced context retrieval using sentence transformers
- **Interactive Web Interface**: Clean, user-friendly Gradio interface
- **Hybrid Analysis**: Combines AI-generated insights with data-driven statistics

### Advanced Analytics
- **Correlation Analysis**: Automatic detection of relationships between variables
- **Missing Data Analysis**: Comprehensive null value reporting
- **Distribution Analysis**: Statistical summaries and data distribution insights
- **Trend Analysis**: Time-series pattern detection
- **Custom Queries**: Natural language questions about your data

### Technical Features
- **Robust CSV Handling**: Multiple encoding and separator detection
- **Error Recovery**: Fallback mechanisms for reliable operation
- **Memory Efficient**: Optimized for large datasets
- **Fast Processing**: FAISS-powered similarity search
- **Extensible Architecture**: Easy to add new models and features

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

1. **Open Google Colab**: Go to [colab.research.google.com](https://colab.research.google.com)

2. **Create New Notebook**: Click "New notebook"

3. **Install Dependencies**: Run this cell first:
```python
!pip install transformers torch gradio pandas openpyxl xlrd sentence-transformers faiss-cpu
```

4. **Copy Main Code**: Copy the entire chatbot code from the artifact and run it

5. **Launch Interface**: The interface will automatically launch with a public URL

### Option 2: Local Installation

#### Prerequisites
- Python 3.8+
- 4GB+ RAM (8GB recommended)
- Internet connection for model downloads

#### Installation Steps

```bash
# Clone or download the code
# Create virtual environment
python -m venv excel_chatbot_env

# Activate virtual environment
# Windows:
excel_chatbot_env\Scripts\activate
# macOS/Linux:
source excel_chatbot_env/bin/activate

# Install dependencies
pip install transformers torch gradio pandas openpyxl xlrd sentence-transformers faiss-cpu
```

#### Run the Application
```python
python excel_chatbot.py
```

## 📋 Usage Guide

### 1. Upload Your Data

**Supported Formats:**
- Excel files: `.xlsx`, `.xls`
- CSV files: `.csv`

**CSV Requirements:**
- UTF-8 encoding preferred
- Comma-separated values
- First row should contain headers
- No password protection

### 2. Ask Questions

**Example Queries:**

#### Data Overview
- "Give me a summary of this data"
- "What are the main characteristics of this dataset?"
- "Describe the structure of my data"

#### Statistical Analysis
- "What correlations exist between numeric columns?"
- "Show me statistics for all numeric columns"
- "Which columns have the most missing values?"

#### Specific Insights
- "What is the relationship between price and sales?"
- "Analyze the distribution of customer ages"
- "What trends do you see in the revenue data?"

#### Custom Analysis
- "Find outliers in the salary column"
- "Compare performance across different categories"
- "What factors influence customer satisfaction?"

### 3. Interpret Results

The chatbot provides:
- **AI-Generated Insights**: Natural language explanations
- **Statistical Analysis**: Concrete numbers and calculations
- **Data Visualizations**: Descriptive statistics
- **Actionable Recommendations**: Based on patterns found

## 🔧 Configuration Options

### Model Selection

You can easily switch between different LLM models by modifying the `model_name` variable:

```python
# Option 1: GPT-2 (Default - Fast and reliable)
model_name = "gpt2"

# Option 2: Larger GPT-2 (Better quality, slower)
model_name = "gpt2-medium"

# Option 3: Conversational model
model_name = "microsoft/DialoGPT-small"

# Option 4: Code-aware model (Better for technical analysis)
model_name = "Salesforce/codegen-350M-mono"
```

### Performance Tuning

#### For Faster Processing:
```python
# Reduce max_length in generation
max_length = input_ids.shape[1] + 50  # Instead of 100

# Use smaller models
model_name = "gpt2"  # Instead of gpt2-medium
```

#### For Better Quality:
```python
# Use larger models
model_name = "gpt2-large"

# Increase context length
max_length = 600  # Instead of 400
```

### Memory Optimization

For large datasets:
```python
# Process data in chunks
chunk_size = 1000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process chunk
```

## 🛠️ Technical Architecture

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gradio UI     │────│  Chatbot Core    │────│   Data Engine   │
│   (Interface)   │    │  (Orchestrator)  │    │   (Analytics)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │              ┌──────────────────┐              │
         │              │   LLM Engine     │              │
         └──────────────│ (Text Generation)│──────────────┘
                        └──────────────────┘
                                 │
                    ┌──────────────────────────┐
                    │   Semantic Search        │
                    │ (Context Retrieval)      │
                    └──────────────────────────┘
```

### Key Libraries

- **Transformers**: Hugging Face transformer models
- **PyTorch**: Neural network framework
- **Gradio**: Web interface framework
- **Pandas**: Data manipulation and analysis
- **SentenceTransformers**: Semantic embeddings
- **FAISS**: Fast similarity search
- **NumPy**: Numerical computing

### Data Flow

1. **File Upload** → Gradio interface receives file
2. **Data Loading** → Pandas reads and processes data
3. **Analysis** → Statistical analysis and embeddings generation
4. **Query Processing** → User question semantic search
5. **LLM Generation** → AI model generates insights
6. **Response Synthesis** → Combines AI and statistical insights
7. **Display** → Results shown in interface

## 🔍 Troubleshooting

### Common Issues and Solutions

#### CSV Loading Problems

**Issue**: "Only one column detected"
```
Solution: Your CSV likely uses semicolons (;) instead of commas
- Try re-saving with comma separators
- Or the chatbot will auto-detect and fix this
```

**Issue**: "Encoding error"
```
Solution: Save your CSV with UTF-8 encoding
- Excel: File → Save As → CSV UTF-8
- Google Sheets: File → Download → CSV
```

**Issue**: "File appears empty"
```
Solution: Check your file structure
- Ensure first row contains headers
- Verify data exists below headers
- Remove any blank rows at the top
```

#### Memory Issues

**Issue**: "Out of memory" error
```
Solution: Use smaller models or reduce data size
- Switch to "gpt2" instead of "gpt2-medium"
- Sample your data: df.sample(n=10000)
- Use Google Colab Pro for more RAM
```

#### Model Loading Issues

**Issue**: "Model not found" error
```
Solution: Check internet connection and model name
- Ensure stable internet for model download
- Verify model name spelling
- Try alternative models like "gpt2"
```

### Performance Optimization

#### Slow Response Times
```python
# Reduce generation length
max_length = input_ids.shape[1] + 50

# Use smaller context
max_length = 300  # Instead of 400

# Switch to faster model
model_name = "gpt2"  # Instead of larger models
```

#### Large File Handling
```python
# Sample large datasets
if df.shape[0] > 50000:
    df = df.sample(n=10000)
    
# Process in chunks for analysis
chunk_size = 5000
```

## 📚 Example Use Cases

### Business Analytics
```
Dataset: Sales data with columns: Date, Product, Region, Sales, Price
Query: "Which regions have the highest sales growth?"
Output: Regional analysis with growth rates and trends
```

### Financial Analysis
```
Dataset: Stock prices with columns: Date, Symbol, Open, Close, Volume
Query: "What correlations exist between volume and price changes?"
Output: Correlation analysis and trading insights
```

### Customer Analysis
```
Dataset: Customer data with columns: Age, Income, Purchases, Satisfaction
Query: "What factors influence customer satisfaction most?"
Output: Statistical relationships and customer insights
```

### Academic Research
```
Dataset: Survey responses with multiple variables
Query: "Summarize the key findings from this survey data"
Output: Comprehensive statistical summary and patterns
```

## 🔄 Advanced Features

### Custom Model Integration

Add your own models:
```python
# Add custom model option
custom_models = {
    "custom_model": "path/to/your/model",
    "specialized_model": "organization/model-name"
}

# Modify initialization
model_name = custom_models["custom_model"]
```

### API Integration

Convert to API service:
```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/analyze")
async def analyze_data(file, query):
    return chatbot.generate_insights(query)

uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Batch Processing

Process multiple files:
```python
def batch_analyze(file_list, queries):
    results = []
    for file_path in file_list:
        chatbot.load_excel_file(file_path)
        for query in queries:
            result = chatbot.generate_insights(query)
            results.append({"file": file_path, "query": query, "result": result})
    return results
```

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd excel-analytics-chatbot

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black *.py
flake8 *.py
```

### Adding New Features

1. **New Analysis Types**: Add methods to `ExcelAnalyticsChatbot` class
2. **New Models**: Update model configuration section
3. **New File Formats**: Extend `load_excel_file` method
4. **UI Improvements**: Modify Gradio interface

### Testing

```python
# Test with sample data
def test_basic_functionality():
    chatbot = ExcelAnalyticsChatbot()
    # Create sample DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    chatbot.df = df
    result = chatbot.generate_insights("Summarize this data")
    assert len(result) > 0
```

## 📄 License

This project is open-source and available under the MIT License.

## 🆘 Support

### Getting Help

1. **Check Troubleshooting Section**: Most common issues are covered above
2. **Test with Sample Data**: Use the "Test with Sample CSV" button
3. **Check Error Messages**: They often contain specific solutions
4. **Review Examples**: Look at the provided example queries

### Reporting Issues

When reporting problems, include:
- Error message (full traceback)
- File type and size
- Operating system
- Python version
- Steps to reproduce

### Community

- Share your interesting findings
- Contribute improvements
- Report bugs and suggest features
- Help others with similar issues

## 🔮 Future Enhancements

### Planned Features
- **Data Visualization**: Interactive charts and graphs
- **Export Capabilities**: PDF reports and analysis summaries
- **Multi-file Analysis**: Compare datasets
- **Advanced ML**: Predictive analytics integration
- **Custom Dashboards**: Personalized analytics views

### Model Improvements
- **Fine-tuned Models**: Domain-specific analytical models
- **Multimodal Support**: Image and text analysis
- **Real-time Processing**: Streaming data analysis
- **Cloud Integration**: AWS/GCP model hosting

---
