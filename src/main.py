import uuid
import datetime
import json
import re
from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store conversations in memory
conversations = {}

class RealTimeFIRGenerator:
    def __init__(self):
        # Load BNS data
        try:
            with open('src/bns_data.json', 'r', encoding='utf-8') as f:
                self.bns_data = json.load(f)
        except:
            self.bns_data = []
        
        # Build keyword mapping for section identification
        self.keyword_mapping = self._build_keyword_mapping()
    
    def _build_keyword_mapping(self):
        """Build comprehensive keyword to section mapping from BNS data"""
        mapping = {}
        
        # If BNS data is available, use it
        if self.bns_data:
            for chapter in self.bns_data:
                for section in chapter.get('sections', []):
                    section_info = {
                        'section': f"Section {section.get('section_number', '')}",
                        'title': section.get('section_title', ''),
                        'content': section.get('content', '')[:200] + "..." if len(section.get('content', '')) > 200 else section.get('content', ''),
                        'chapter': chapter.get('chapter_title', '')
                    }
                    
                    text = f"{section.get('section_title', '')} {section.get('content', '')}".lower()
                    
                    # Comprehensive keyword mapping
                    # Theft-related offenses
                    if any(word in text for word in ['theft', 'stealing', 'dishonestly takes', 'movable property']):
                        if 'theft' not in mapping:
                            mapping['theft'] = []
                        mapping['theft'].append(section_info)
                    
                    # Assault and hurt
                    if any(word in text for word in ['hurt', 'assault', 'voluntarily causing', 'grievous hurt', 'violence']):
                        if 'assault' not in mapping:
                            mapping['assault'] = []
                        mapping['assault'].append(section_info)
                    
                    # Fraud and cheating
                    if any(word in text for word in ['cheating', 'deceives', 'fraud', 'dishonestly induces', 'false pretence']):
                        if 'fraud' not in mapping:
                            mapping['fraud'] = []
                        mapping['fraud'].append(section_info)
                    
                    # Robbery and extortion
                    if any(word in text for word in ['robbery', 'extortion', 'dacoity', 'criminal force']):
                        if 'robbery' not in mapping:
                            mapping['robbery'] = []
                        mapping['robbery'].append(section_info)
                    
                    # Criminal breach of trust
                    if any(word in text for word in ['criminal breach of trust', 'entrusted', 'misappropriation']):
                        if 'breach_of_trust' not in mapping:
                            mapping['breach_of_trust'] = []
                        mapping['breach_of_trust'].append(section_info)
                    
                    # Mischief and property damage
                    if any(word in text for word in ['mischief', 'destroys', 'damages', 'property damage']):
                        if 'mischief' not in mapping:
                            mapping['mischief'] = []
                        mapping['mischief'].append(section_info)
                    
                    # House trespass and burglary
                    if any(word in text for word in ['house-trespass', 'house trespass', 'burglary', 'house-breaking']):
                        if 'trespass' not in mapping:
                            mapping['trespass'] = []
                        mapping['trespass'].append(section_info)
        
        # Enhanced fallback mapping if BNS data is not available or incomplete
        if not mapping or len(mapping) < 5:
            mapping.update({
                'theft': [
                    {'section': 'Section 303', 'title': 'Theft', 'content': 'Whoever dishonestly takes any movable property out of the possession of any person without that person\'s consent...', 'chapter': 'OF OFFENCES AGAINST PROPERTY'},
                    {'section': 'Section 304', 'title': 'Theft in dwelling house', 'content': 'Whoever commits theft in any dwelling house, or any building used as a human dwelling...', 'chapter': 'OF OFFENCES AGAINST PROPERTY'}
                ],
                'assault': [
                    {'section': 'Section 115', 'title': 'Voluntarily causing hurt', 'content': 'Whoever voluntarily causes hurt to any person other than the hurt caused in the right of private defence...', 'chapter': 'OF OFFENCES AFFECTING THE HUMAN BODY'},
                    {'section': 'Section 117', 'title': 'Voluntarily causing grievous hurt', 'content': 'Whoever voluntarily causes grievous hurt to any person other than the hurt caused in the right of private defence...', 'chapter': 'OF OFFENCES AFFECTING THE HUMAN BODY'}
                ],
                'fraud': [
                    {'section': 'Section 318', 'title': 'Cheating', 'content': 'Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property...', 'chapter': 'OF OFFENCES AGAINST PROPERTY'},
                    {'section': 'Section 319', 'title': 'Cheating by personation', 'content': 'A person is said to cheat by personation if he cheats by pretending to be some other person...', 'chapter': 'OF OFFENCES AGAINST PROPERTY'}
                ],
                'robbery': [
                    {'section': 'Section 309', 'title': 'Robbery', 'content': 'In all robbery there is either theft or extortion...', 'chapter': 'OF OFFENCES AGAINST PROPERTY'},
                    {'section': 'Section 310', 'title': 'Dacoity', 'content': 'When five or more persons conjointly commit or attempt to commit a robbery...', 'chapter': 'OF OFFENCES AGAINST PROPERTY'}
                ]
            })
        
        return mapping
    
    def identify_sections(self, incident_text):
        """Identify applicable BNS sections from incident text with comprehensive analysis"""
        incident_lower = incident_text.lower()
        applicable_sections = []
        
        # Enhanced crime type detection
        # Theft-related crimes
        if any(word in incident_lower for word in ['theft', 'steal', 'stole', 'stolen', 'rob', 'wallet', 'money', 'phone', 'purse', 'bag', 'laptop', 'jewelry', 'watch']):
            applicable_sections.extend(self.keyword_mapping.get('theft', []))
        
        # Assault and violence
        if any(word in incident_lower for word in ['assault', 'attack', 'hit', 'beat', 'violence', 'hurt', 'punch', 'kick', 'slap', 'fight']):
            applicable_sections.extend(self.keyword_mapping.get('assault', []))
        
        # Fraud and cheating
        if any(word in incident_lower for word in ['fraud', 'cheat', 'deceive', 'fake', 'scam', 'false', 'lie', 'trick', 'con']):
            applicable_sections.extend(self.keyword_mapping.get('fraud', []))
        
        # Robbery and extortion
        if any(word in incident_lower for word in ['robbery', 'rob', 'extortion', 'force', 'threat', 'intimidate', 'demand money']):
            applicable_sections.extend(self.keyword_mapping.get('robbery', []))
        
        # Breach of trust
        if any(word in incident_lower for word in ['trust', 'entrusted', 'misappropriation', 'embezzle', 'misuse']):
            applicable_sections.extend(self.keyword_mapping.get('breach_of_trust', []))
        
        # Property damage
        if any(word in incident_lower for word in ['damage', 'destroy', 'break', 'vandalism', 'mischief', 'property damage']):
            applicable_sections.extend(self.keyword_mapping.get('mischief', []))
        
        # Trespass and burglary
        if any(word in incident_lower for word in ['trespass', 'break in', 'burglary', 'enter', 'house breaking', 'unauthorized entry']):
            applicable_sections.extend(self.keyword_mapping.get('trespass', []))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_sections = []
        for section in applicable_sections:
            section_key = section['section']
            if section_key not in seen:
                seen.add(section_key)
                unique_sections.append(section)
        
        # Limit to most relevant sections (top 5)
        unique_sections = unique_sections[:5]
        
        if not unique_sections:
            unique_sections = [{'section': 'To be determined', 'title': 'Requires further investigation and legal analysis', 'content': 'The specific sections will be determined after detailed investigation.', 'chapter': 'GENERAL'}]
        
        return unique_sections
    
    def extract_entities(self, incident_text):
        """Extract entities from incident text"""
        entities = {
            'accused': [],
            'victims': [],
            'objects': [],
            'location': '',
            'time': ''
        }
        
        # Simple entity extraction using regex
        # Extract names (simple pattern)
        names = re.findall(r'\b[A-Z][a-z]+\b', incident_text)
        if names:
            entities['accused'] = names[:2]  # Take first 2 names as potential accused
        
        # Extract objects
        objects = re.findall(r'\b(?:wallet|phone|money|bag|purse|laptop|watch|jewelry|car|bike)\b', incident_text.lower())
        entities['objects'] = list(set(objects))
        
        return entities
    
    def generate_narrative(self, responses, entities, sections):
        """Generate FIR narrative"""
        narrative_parts = []
        
        narrative_parts.append("DETAILS OF THE INCIDENT:")
        narrative_parts.append("")
        
        # Complainant details
        if responses.get('name'):
            narrative_parts.append(f"The complainant, {responses['name']}, states that:")
        
        # Main incident
        if responses.get('incident_description'):
            narrative_parts.append(responses['incident_description'])
            narrative_parts.append("")
        
        # Additional details
        if responses.get('date_time'):
            narrative_parts.append(f"Date and Time of Incident: {responses['date_time']}")
        
        if responses.get('location'):
            narrative_parts.append(f"Place of Incident: {responses['location']}")
        
        if responses.get('witnesses'):
            narrative_parts.append(f"Witnesses: {responses['witnesses']}")
        
        if responses.get('evidence'):
            narrative_parts.append(f"Evidence: {responses['evidence']}")
        
        narrative_parts.append("")
        
        # Entities
        if entities['accused']:
            narrative_parts.append(f"Accused person(s): {', '.join(entities['accused'])}")
        
        if entities['objects']:
            narrative_parts.append(f"Objects involved: {', '.join(entities['objects'])}")
        
        narrative_parts.append("")
        narrative_parts.append("The above facts constitute an offence and the complainant requests for appropriate legal action.")
        
        return "\n".join(narrative_parts)
    
    def generate_html_document(self, responses, entities, sections, fir_number):
        """Generate HTML version of the FIR document for download"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIR Document - {fir_number}</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 40px;
            background: white;
            color: #000;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #000;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .fir-info {{
            margin-bottom: 20px;
        }}
        .section {{
            margin-bottom: 25px;
        }}
        .section h3 {{
            color: #000;
            border-bottom: 2px solid #dc3545;
            padding-bottom: 5px;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .field {{
            margin-bottom: 10px;
            display: flex;
            flex-wrap: wrap;
        }}
        .label {{
            font-weight: bold;
            min-width: 150px;
            margin-right: 10px;
        }}
        .value {{
            flex: 1;
        }}
        .sections-list {{
            background: #f8f9fa;
            padding: 15px;
            border: 2px solid #dc3545;
            border-radius: 8px;
        }}
        .section-item {{
            margin-bottom: 10px;
            padding: 10px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .narrative {{
            background: #f8f9fa;
            padding: 20px;
            border: 2px solid #dc3545;
            border-radius: 8px;
            white-space: pre-line;
        }}
        @media print {{
            body {{ margin: 20px; }}
            .header {{ page-break-after: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">FIRST INFORMATION REPORT (FIR)</div>
        <div class="fir-info">
            <strong>FIR Number:</strong> {fir_number}<br>
            <strong>Date Registered:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
            <strong>Status:</strong> Completed
        </div>
    </div>

    <div class="section">
        <h3>Complainant Information</h3>
        <div class="field">
            <span class="label">Name:</span>
            <span class="value">{responses.get('name', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Contact Number:</span>
            <span class="value">{responses.get('contact', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Address:</span>
            <span class="value">{responses.get('address', 'Not provided')}</span>
        </div>
    </div>

    <div class="section">
        <h3>Incident Details</h3>
        <div class="field">
            <span class="label">Description:</span>
            <span class="value">{responses.get('incident_description', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Date & Time:</span>
            <span class="value">{responses.get('date_time', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Location:</span>
            <span class="value">{responses.get('location', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Witnesses:</span>
            <span class="value">{responses.get('witnesses', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Evidence:</span>
            <span class="value">{responses.get('evidence', 'Not provided')}</span>
        </div>
        <div class="field">
            <span class="label">Additional Information:</span>
            <span class="value">{responses.get('additional_info', 'Not provided')}</span>
        </div>
    </div>
"""
        
        if sections:
            html_content += """
    <div class="section">
        <h3>Applicable Legal Sections</h3>
        <div class="sections-list">
"""
            for section in sections:
                html_content += f"""
            <div class="section-item">
                <strong>{section['section']}:</strong> {section['title']}<br>
                <em>{section.get('content', '')[:200]}...</em>
            </div>
"""
            html_content += """
        </div>
    </div>
"""
        
        narrative = self.generate_narrative(responses, entities, sections)
        if narrative:
            html_content += f"""
    <div class="section">
        <h3>Incident Narrative</h3>
        <div class="narrative">{narrative}</div>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        return html_content

class SplitScreenChatbot:
    def __init__(self):
        self.current_question = 0
        self.responses = {}
        self.fir_generator = RealTimeFIRGenerator()
        
        self.questions = [
            "What is your full name?",
            "What is your contact number?", 
            "What is your address?",
            "Please describe the incident that occurred in detail.",
            "When did this incident happen? (Date and time)",
            "Where did this incident take place?",
            "Are there any witnesses? If yes, please provide their names.",
            "Do you have any evidence or documents related to this incident?",
            "Is there anything else you would like to add to your report?"
        ]
        
        self.question_keys = [
            "name", "contact", "address", "incident_description",
            "date_time", "location", "witnesses", "evidence", "additional_info"
        ]
    
    def get_current_question(self):
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def process_response(self, response):
        # Store the response
        if self.current_question < len(self.question_keys):
            self.responses[self.question_keys[self.current_question]] = response
        
        # Generate real-time FIR content
        fir_content = self.generate_realtime_fir()
        
        # Move to next question
        self.current_question += 1
        
        # Check if conversation is complete
        completed = self.current_question >= len(self.questions)
        
        return {
            "next_question": self.get_current_question(),
            "completed": completed,
            "fir_content": fir_content,
            "progress": {
                "current": self.current_question,
                "total": len(self.questions)
            }
        }
    
    def generate_realtime_fir(self):
        """Generate FIR content in real-time as user provides information"""
        fir_number = f"FIR/{datetime.datetime.now().strftime('%Y')}/{uuid.uuid4().hex[:8].upper()}"
        
        # Basic FIR structure
        fir_content = {
            "fir_number": fir_number,
            "date_registered": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "In Progress" if self.current_question < len(self.questions) - 1 else "Completed",
            "complainant": {
                "name": self.responses.get("name", "[To be provided]"),
                "contact": self.responses.get("contact", "[To be provided]"),
                "address": self.responses.get("address", "[To be provided]")
            },
            "incident": {
                "description": self.responses.get("incident_description", "[To be provided]"),
                "date_time": self.responses.get("date_time", "[To be provided]"),
                "location": self.responses.get("location", "[To be provided]"),
                "witnesses": self.responses.get("witnesses", "[To be provided]"),
                "evidence": self.responses.get("evidence", "[To be provided]"),
                "additional_info": self.responses.get("additional_info", "[To be provided]")
            },
            "applicable_sections": [],
            "narrative": ""
        }
        
        # If incident description is available, analyze it
        if self.responses.get("incident_description"):
            # Identify applicable sections
            sections = self.fir_generator.identify_sections(self.responses["incident_description"])
            fir_content["applicable_sections"] = [
                {"section": s["section"], "description": s["title"]}
                for s in sections
            ]
            
            # Extract entities
            entities = self.fir_generator.extract_entities(self.responses["incident_description"])
            
            # Generate narrative
            fir_content["narrative"] = self.fir_generator.generate_narrative(
                self.responses, entities, sections
            )
        
        return fir_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        session_id = data.get('session_id', str(uuid.uuid4()))
        message = data.get('message', '')
        
        # Initialize or get existing conversation
        if session_id not in conversations:
            conversations[session_id] = SplitScreenChatbot()
        
        chatbot = conversations[session_id]
        
        # Start conversation
        if chatbot.current_question == 0 and not message:
            response = {
                "question": chatbot.get_current_question(),
                "completed": False,
                "session_id": session_id,
                "fir_content": chatbot.generate_realtime_fir(),
                "progress": {"current": 0, "total": len(chatbot.questions)}
            }
        else:
            # Process user response
            response = chatbot.process_response(message)
            response["session_id"] = session_id
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download_pdf/<session_id>')
def download_html(session_id):
    try:
        if session_id not in conversations:
            return jsonify({"error": "Session not found"}), 404
        
        chatbot = conversations[session_id]
        
        # Generate entities and sections
        if chatbot.responses.get("incident_description"):
            entities = chatbot.fir_generator.extract_entities(chatbot.responses["incident_description"])
            sections = chatbot.fir_generator.identify_sections(chatbot.responses["incident_description"])
        else:
            entities = {}
            sections = []
        
        # Generate FIR number
        fir_number = f"FIR/{datetime.datetime.now().strftime('%Y')}/{uuid.uuid4().hex[:8].upper()}"
        
        # Generate HTML document
        html_content = chatbot.fir_generator.generate_html_document(chatbot.responses, entities, sections, fir_number)
        
        # Create response
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename=FIR_{fir_number.replace("/", "_")}.html'
        
        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

