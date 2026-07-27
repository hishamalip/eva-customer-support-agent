# Eva - Flower Shop Customer Support Agent

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/flower-bouquet.png" alt="Flower Shop Icon" width="100"/>
</p>

<h3 align="center">AI-Powered Customer Support Chatbot for Flower Shops</h3>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#license">License</a>
</p>

---

## About

**Eva** is an intelligent customer support chatbot designed specifically for flower shop businesses. Built with modern AI technologies, Eva can handle customer inquiries, recommend products, manage orders, and create customer profiles - all through a friendly, conversational interface.

## Features

### Customer Service Capabilities
- **FAQ Assistance**: Answer common questions about services, policies, and business processes
- **Product Recommendations**: Suggest flower arrangements based on customer preferences (birthdays, weddings, anniversaries, etc.)
- **Order Management**: Check order status and place new orders
- **Customer Profiles**: Create and verify customer profiles with data protection checks

### Key Functionalities

| Feature | Description |
|---------|-------------|
| Knowledge Base Query | Search FAQ database for answers to common questions |
| Product Search | Find products matching customer descriptions |
| Data Protection Check | Verify customer identity before accessing personal data |
| Customer Registration | Create new customer profiles |
| Order Status | Retrieve and display existing customer orders |
| Order Placement | Place new orders with inventory validation |

## Technologies

### Core Stack
- **LangGraph**: Stateful, multi-actor applications with LLM workflows
- **LangChain**: LLM orchestration and tool integration
- **ChromaDB**: Vector database for semantic search
- **HuggingFace Embeddings**: NovaSearch/stella_en_1.5B_v5 model for embeddings
- **Streamlit**: Web-based user interface
- **JSON Files**: FAQ and inventory data
- **ChromaDB**: Persistent vector storage for embeddings

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hishamalip/eva-customer-support-agent.git
   cd eva-customer-support-agent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your API keys:
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   ```

5. **Initialize the vector database (first run only):**
   ```bash
   python -c "from vector_store import FlowerShopVectorStore; FlowerShopVectorStore()"
   ```

## Usage

### Running the Chatbot

Start the Streamlit web application:

```bash
streamlit run streamlit_frontend.py
```

The application will launch in your default browser at `http://localhost:8501`.

### Using Eva

1. **Start a conversation**: Type your message in the chat input box
2. **Get recommendations**: Ask for flower arrangements for specific occasions
3. **Check orders**: Provide your customer details to check existing orders
4. **Place orders**: Create a customer profile (if new) and place orders

### Example Conversations

**Product Recommendation:**
```
User: "I need a bouquet for a birthday with red flowers"
Eva: [Recommends suitable products from inventory]
```

**Order Status:**
```
User: "I want to check my order status"
Eva: [Guides through data protection check]
User: [Provides name, email, and date of birth]
Eva: [Displays order information]
```

**New Order:**
```
User: "I want to place a new order"
Eva: [Creates customer profile or verifies existing one]
User: [Provides order details]
Eva: [Places order and confirms]
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                   │
│                 (streamlit_frontend.py)                 │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                    LangGraph Agent                      │
│                      (chatbot.py)                       │
│  ┌─────────────┐   ┌─────────────┐    ┌─────────────┐   │
│  │   State     │──►│   Agent     │───►│  Tool Node  │   │
│  │   Graph     │   │  (LLM +     │    │  (Tool      │   │
│  └─────────────┘   │   Prompt)   │◄───│   Execution)│   │
│                    └─────────────┘    └─────────────┘   │
└─────────────────────────────────────────────────────────┘ 
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Knowledge Base  │ │ Product Search   │ │ Order            │
│ Query           │ │ & Recommendation │ │ Management       │
│ (FAQ)           │ │ (Inventory)      │ │ (Create/Retrieve)│
└─────────────────┘ └──────────────────┘ └──────────────────┘
              │               │               │
              ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                     Vector Store                        │
│                  (vector_store.py)                      │
│  ┌─────────────────────┐  ┌───────────────────────┐     │
│  │  FAQ Collection     │  │  Inventory Collection │     │
│  │  (ChromaDB + HF     │  │   (ChromaDB + HF      │     │
│  │   Embeddings)       │  │    Embeddings)        │     │
│  └─────────────────────┘  └───────────────────────┘     │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                    Data Files                            │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐  │
│  │  FAQ.json   │    │inventory.json│    │  .env       │  │
│  └─────────────┘    └──────────────┘    └─────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Workflow

1. **User Input**: Messages enter through Streamlit interface
2. **State Management**: LangGraph maintains conversation state
3. **LLM Processing**: Mistral model processes input with system prompt
4. **Tool Selection**: Agent decides which tools to call
5. **Tool Execution**: Tools query vector store or manage data
6. **Response Generation**: Agent formulates response
7. **Output**: Response displayed in Streamlit

## Project Structure

```
eva-customer-support-agent/
├── .chroma_db/                 # ChromaDB persistent storage
├── .venv/                     # Python virtual environment
├── .env                       # Environment variables
├── .gitignore                 # Git ignore patterns
├── FAQ.json                   # Frequently asked questions
├── LICENSE                    # MIT License
├── README.md                  # This file
├── chatbot.py                 # Main agent with LangGraph
├── inventory.json             # Product inventory data
├── requirements.txt           # Python dependencies
├── streamlit_frontend.py      # Streamlit web interface
├── tools.py                   # Custom tool definitions
└── vector_store.py            # Vector store implementation
```

## Tools Reference

### Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `query_knowledge_base` | Search FAQ database | `query: str` |
| `search_for_product_recommendations` | Find matching products | `description: str` |
| `data_protection_check` | Verify customer identity | `name, email, year_of_birth, month_of_birth, day_of_birth` |
| `create_new_customer` | Register new customer | `first_name, surname, year_of_birth, month_of_birth, day_of_birth, first_line_of_address, phone_number, email` |
| `retrieve_existing_customer_orders` | Get customer orders | `customer_id: str` |
| `place_order` | Create new order | `items: Dict[str, int], customer_id: str` |

## Data Protection

The system implements data protection checks before accessing customer information:

- Customers must verify identity with: Full name, Email, Date of birth
- Only verified customers can access their own order history
- Customer data is stored securely in memory (dummy database for demo)

## Sample Data

The project includes sample data for demonstration:

- **FAQ.json**: Common customer questions and answers
- **inventory.json**: Flower products with descriptions, prices, and quantities
- **CUSTOMER_DATABASE**: Pre-registered test customers
- **ORDERS_DATABASE**: Sample orders for testing

## Customization

### Adding New FAQs
Edit `FAQ.json` and reinitialize the vector store:
```json
{
  "question": "Your question here",
  "answer": "Your answer here"
}
```

### Adding Inventory Items
Edit `inventory.json`:
```json
{
  "id": "P001",
  "name": "Product Name",
  "description": "Product description for semantic search",
  "type": "Flower Type",
  "price": 29.99,
  "quantity": 50
}
```

### Changing LLM Model
Edit `chatbot.py`:
```python
llm = ChatOpenAI(
    model="your-preferred-model",
    base_url="your-api-endpoint"
)
```

## Troubleshooting

### Common Issues

**Vector store not initialized:**
```bash
rm -rf .chroma_db
python -c "from vector_store import FlowerShopVectorStore; FlowerShopVectorStore()"
```

**API key not found:**
Ensure `.env` file exists with `OPENAI_API_KEY=your_key`

**Dependencies not installed:**
```bash
pip install -r requirements.txt
```

**Streamlit not starting:**
```bash
streamlit --version  # Check if installed
pip install streamlit  # If not installed
```

## Future Enhancements

- [ ] Add authentication for customer accounts
- [ ] Integrate with real payment gateways
- [ ] Add order tracking with delivery status
- [ ] Support for multiple flower shop locations
- [ ] Add loyalty program integration
- [ ] Multi-language support
- [ ] Voice input/output capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue on the GitHub repository.

