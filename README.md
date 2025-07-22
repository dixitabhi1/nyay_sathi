# AI Legal Assistant Chatbot - Red & Black Theme

A sophisticated AI-powered legal assistant chatbot with a professional red and black card theme design. This application provides real-time FIR (First Information Report) generation with split-screen interface and comprehensive BNS (Bharatiya Nyaya Sanhita 2023) integration.

## 🎨 Design Features

- **Classic Red & Black Theme**: Professional card-based design with elegant color scheme
- **Split-Screen Interface**: Real-time FIR drafting alongside conversational interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Card-Based Layout**: Modern card design with shadows and gradients

## ✨ Key Features

### 🤖 Intelligent Chatbot
- Interactive conversation flow for incident reporting
- Step-by-step information gathering
- Real-time progress tracking
- Professional conversational interface

### 📄 Real-Time FIR Generation
- Live document drafting as user provides information
- Professional FIR formatting with unique reference numbers
- Automatic legal section identification from BNS 2023
- Entity extraction (accused persons, victims, objects, crime types)

### 🏛️ Legal Intelligence
- Complete BNS (Bharatiya Nyaya Sanhita 2023) dataset integration
- Advanced keyword-to-section mapping
- Contextual legal recommendations
- Comprehensive crime type detection

### 📥 Document Export
- HTML document download with professional formatting
- Print-ready layout optimized for legal documentation
- Unique FIR numbering system
- Complete incident narrative generation

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Extract the project files**
   ```bash
   unzip red-black-legal-chatbot.zip
   cd red-black-legal-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Access the chatbot**
   Open your web browser and navigate to: `http://localhost:5000`

## 🎯 How to Use

1. **Start Incident Report**: Click the "Start Incident Report" button
2. **Provide Information**: Answer the chatbot's questions step by step
3. **Watch Real-Time Drafting**: See your FIR document being created in real-time on the right panel
4. **Download Document**: Once complete, download your FIR document using the download button

## 📋 Information Collected

The chatbot collects the following information:
- **Personal Details**: Name, contact number, address
- **Incident Description**: Detailed description of what happened
- **Time & Location**: When and where the incident occurred
- **Witnesses**: Names of any witnesses
- **Evidence**: Available evidence or documents
- **Additional Information**: Any other relevant details

## 🏛️ Legal Section Identification

The system automatically identifies applicable BNS sections based on:
- **Theft Cases**: Sections 303, 304 (Theft, Theft in dwelling house)
- **Assault Cases**: Sections 115, 117 (Voluntarily causing hurt)
- **Fraud Cases**: Sections 318, 319 (Cheating)
- **Property Crimes**: Various property-related sections
- **And many more crime types** with comprehensive BNS coverage

## 🎨 Theme Customization

The red and black theme includes:
- **Primary Colors**: Classic red (#dc3545) and black (#000000)
- **Card Design**: Elevated cards with shadows and rounded corners
- **Gradients**: Smooth color transitions for modern appearance
- **Typography**: Professional fonts with proper hierarchy
- **Interactive Elements**: Hover effects and smooth transitions

## 📁 Project Structure

```
red-black-legal-chatbot/
├── src/
│   ├── main.py              # Flask application
│   ├── templates/
│   │   └── index.html       # Main interface with red/black theme
│   ├── static/              # Static files (if any)
│   └── bns_data.json        # BNS 2023 legal dataset
├── requirements.txt         # Python dependencies
├── run.py                  # Application launcher
└── README.md               # This file
```

## 🔧 Technical Details

### Backend
- **Framework**: Flask (Python web framework)
- **Data Processing**: JSON-based BNS data handling
- **Document Generation**: HTML-based FIR document creation
- **API Endpoints**: RESTful API for chat and document download



### Frontend
- **Design**: Responsive HTML5/CSS3 with card theme
- **JavaScript**:  JS for real-time interactions
- **Styling**: Custom CSS with red and black color scheme
- **Layout**: Split-screen design with flexbox

### Legal Database
- **Dataset**: Complete BNS 2023 (462,401 bytes)
- **Sections**: All major crime categories covered
- **Mapping**: Advanced keyword-to-section identification
- **Updates**: Based on latest legal framework

## 🌐 Deployment

The application is designed to be easily deployable:
- **Local Development**: Run with `python run.py`
- **Production**: Compatible with various hosting platforms
- **Docker**: Can be containerized for cloud deployment
- **Scaling**: Supports multiple concurrent users

## 🔒 Security & Privacy

- **Data Handling**: All data processed locally during session
- **No External APIs**: Self-contained legal analysis
- **Session Management**: Secure session handling
- **Privacy**: No data stored permanently without user consent

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill any process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Permission Issues**
   ```bash
   # On Linux/Mac, ensure proper permissions
   chmod +x run.py
   ```

## 📞 Support

For technical support or questions:
- Check the console output for error messages
- Ensure all dependencies are properly installed
- Verify Python version compatibility (3.7+)
- Review the application logs for debugging information

## 📄 License

This project is provided as-is for educational and professional use. Please ensure compliance with local laws and regulations when using for actual legal documentation.

## 🔄 Updates

- **v1.0**: Initial release with basic functionality
- **v2.0**: Added BNS integration and enhanced UI
- **v3.0**: Implemented red and black theme with card design
- **Current**: Real-time FIR generation with professional styling

---

**Note**: This application is designed to assist in legal documentation but should not replace professional legal advice. Always consult with qualified legal professionals for official legal matters.

