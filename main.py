import os
import streamlit as st
from vapi_python import Vapi
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Interview Assistant",
    page_icon="👔",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-title {
        font-size: 24px;
        color: #424242;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-active {
        color: #4CAF50;
        font-weight: bold;
    }
    .status-inactive {
        color: #F44336;
        font-weight: bold;
    }
    .container {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .interview-question {
        font-weight: bold;
        margin-top: 10px;
    }
    .interview-note {
        font-style: italic;
        color: #666;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'call_active' not in st.session_state:
    st.session_state.call_active = False
if 'vapi_instance' not in st.session_state:
    st.session_state.vapi_instance = None
if 'interview_type' not in st.session_state:
    st.session_state.interview_type = "software_engineer"
if 'interview_level' not in st.session_state:
    st.session_state.interview_level = "mid_level"
if 'interview_duration' not in st.session_state:
    st.session_state.interview_duration = "30_minutes"

# Title and description
st.markdown('<div class="main-title">AI Interview Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Practice your interview skills with an AI interviewer</div>', unsafe_allow_html=True)

# API Key input
api_key = os.getenv("VAPI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your Vapi API Key:", type="password", 
                           help="Get your API key from the Vapi dashboard")

# Interview configuration section
if not st.session_state.call_active:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Interview Configuration")

    col1, col2 = st.columns(2)

    with col1:
        interview_type = st.selectbox(
            "Interview Type:", 
            options=[
                "software_engineer", 
                "data_scientist", 
                "product_manager", 
                "marketing", 
                "sales", 
                "customer_service"
            ],
            format_func=lambda x: x.replace("_", " ").title(),
            index=0
        )
        
        interview_level = st.selectbox(
            "Experience Level:", 
            options=[
                "entry_level", 
                "mid_level", 
                "senior_level", 
                "leadership"
            ],
            format_func=lambda x: x.replace("_", " ").title(),
            index=1
        )

    with col2:
        interview_duration = st.selectbox(
            "Interview Duration:", 
            options=[
                "15_minutes", 
                "30_minutes", 
                "45_minutes", 
                "60_minutes"
            ],
            format_func=lambda x: x.replace("_", " ").title(),
            index=1
        )
        
        company_type = st.selectbox(
            "Company Type:", 
            options=[
                "startup", 
                "mid_size", 
                "enterprise", 
                "faang"
            ],
            format_func=lambda x: "FAANG" if x == "faang" else x.replace("_", " ").title(),
            index=2
        )

    # Custom context input
    st.subheader("Additional Context (Optional)")
    job_description = st.text_area(
        "Job Description or Additional Details:",
        placeholder="Paste job description or provide additional context for the interview...",
        height=100
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Interview templates based on role
interview_templates = {
    "software_engineer": {
        "entry_level": "You are conducting an entry-level software engineering interview. Focus on basic programming concepts, data structures, algorithms, and problem-solving skills. Ask questions about the candidate's educational background and any projects they've worked on.",
        "mid_level": "You are conducting a mid-level software engineering interview. Focus on more advanced programming concepts, system design fundamentals, and practical experience. Ask about previous work experience, technical challenges they've overcome, and how they approach problem-solving.",
        "senior_level": "You are conducting a senior-level software engineering interview. Focus on advanced system design, architecture decisions, technical leadership, and mentoring abilities. Ask about complex projects they've led, technical decisions they've made, and how they handle team dynamics.",
        "leadership": "You are conducting an engineering leadership interview. Focus on technical vision, team management, project planning, and cross-functional collaboration. Ask about their leadership style, how they've grown engineering teams, and how they balance technical and management responsibilities."
    },
    "data_scientist": {
        "entry_level": "You are conducting an entry-level data science interview. Focus on statistics fundamentals, basic machine learning concepts, and data manipulation skills. Ask about their educational background, projects, and familiarity with tools like Python, R, SQL, and basic ML libraries.",
        "mid_level": "You are conducting a mid-level data science interview. Focus on applied machine learning, feature engineering, model evaluation, and business impact. Ask about previous projects, how they've translated business problems into data problems, and their experience with production ML systems.",
        "senior_level": "You are conducting a senior-level data science interview. Focus on advanced modeling techniques, research experience, and technical leadership in data science teams. Ask about novel approaches they've developed, how they've mentored junior data scientists, and their vision for data science in organizations.",
        "leadership": "You are conducting a data science leadership interview. Focus on data strategy, team building, cross-functional collaboration, and business impact at scale. Ask about how they've built data science teams, implemented data governance, and aligned data science initiatives with business goals."
    },
    "product_manager": {
        "entry_level": "You are conducting an entry-level product management interview. Focus on product thinking, user empathy, and basic product development processes. Ask about their understanding of product management, any relevant projects, and how they approach user problems.",
        "mid_level": "You are conducting a mid-level product management interview. Focus on product strategy, prioritization frameworks, cross-functional collaboration, and metrics. Ask about products they've managed, how they've made prioritization decisions, and how they measure success.",
        "senior_level": "You are conducting a senior-level product management interview. Focus on product vision, strategy development, team leadership, and business impact. Ask about complex product challenges they've solved, how they've influenced organizational strategy, and their approach to product innovation.",
        "leadership": "You are conducting a product leadership interview. Focus on product organization structure, developing product culture, executive communication, and strategic thinking. Ask about how they've built product teams, aligned product roadmaps with company strategy, and navigated complex stakeholder environments."
    },
    "marketing": {
        "entry_level": "You are conducting an entry-level marketing interview. Focus on marketing fundamentals, digital marketing channels, content creation, and analytical skills. Ask about their understanding of marketing principles, any campaigns they've worked on, and their familiarity with marketing tools.",
        "mid_level": "You are conducting a mid-level marketing interview. Focus on campaign management, channel strategy, audience targeting, and performance analysis. Ask about marketing campaigns they've led, how they've optimized channel performance, and their approach to marketing analytics.",
        "senior_level": "You are conducting a senior-level marketing interview. Focus on marketing strategy, brand development, team leadership, and cross-channel integration. Ask about comprehensive marketing strategies they've developed, how they've built brand equity, and their approach to marketing innovation.",
        "leadership": "You are conducting a marketing leadership interview. Focus on marketing organization structure, brand vision, marketing technology stack, and business growth strategy. Ask about how they've built marketing teams, aligned marketing with business objectives, and navigated changing market conditions."
    },
    "sales": {
        "entry_level": "You are conducting an entry-level sales interview. Focus on communication skills, basic sales techniques, customer service orientation, and learning agility. Ask about their understanding of the sales process, any sales experience they have, and how they handle objections.",
        "mid_level": "You are conducting a mid-level sales interview. Focus on sales methodology, account management, negotiation skills, and consistent quota achievement. Ask about their sales process, how they manage customer relationships, and specific examples of deals they've closed.",
        "senior_level": "You are conducting a senior-level sales interview. Focus on strategic account planning, complex deal navigation, team leadership, and consistent overperformance. Ask about major accounts they've managed, how they've navigated complex sales cycles, and their approach to sales leadership.",
        "leadership": "You are conducting a sales leadership interview. Focus on sales organization structure, sales strategy development, coaching methodology, and revenue growth. Ask about how they've built and developed sales teams, their approach to territory planning, and how they've driven sustainable revenue growth."
    },
    "customer_service": {
        "entry_level": "You are conducting an entry-level customer service interview. Focus on communication skills, empathy, problem-solving abilities, and patience. Ask about their understanding of customer service principles, how they handle difficult situations, and their approach to helping customers.",
        "mid_level": "You are conducting a mid-level customer service interview. Focus on conflict resolution, customer retention strategies, process improvement, and team collaboration. Ask about challenging customer situations they've resolved, how they've improved customer service processes, and their approach to customer satisfaction.",
        "senior_level": "You are conducting a senior-level customer service interview. Focus on customer service strategy, team leadership, quality assurance, and cross-functional collaboration. Ask about customer service teams they've led, how they've improved service metrics, and their approach to customer experience management.",
        "leadership": "You are conducting a customer service leadership interview. Focus on customer service organization structure, service culture development, technology integration, and business impact. Ask about how they've built customer service teams, implemented service technologies, and aligned service strategy with business objectives."
    }
}

# Company type contexts
company_contexts = {
    "startup": "This is for a fast-paced startup environment where versatility, ownership, and comfort with ambiguity are highly valued. The company has limited resources but offers significant growth opportunities and impact.",
    "mid_size": "This is for a mid-sized company with established processes but still room for innovation and growth. The company values both specialized expertise and cross-functional collaboration.",
    "enterprise": "This is for a large enterprise with complex organizational structures, established processes, and significant resources. The company values scalable solutions, attention to detail, and navigating complex stakeholder environments.",
    "faang": "This is for a FAANG-level tech company (Facebook/Meta, Apple, Amazon, Netflix, Google) or similar tier-1 tech company. The company has extremely high standards, rigorous interview processes, and expects exceptional technical depth and problem-solving abilities."
}

# Duration adjustments
duration_contexts = {
    "15_minutes": "This is a brief screening interview to assess basic qualifications and fit. Focus on high-level questions and keep the conversation moving quickly.",
    "30_minutes": "This is a standard interview round focused on specific areas of expertise. Balance depth and breadth in your questioning.",
    "45_minutes": "This is an extended interview allowing for deeper exploration of the candidate's experience and skills. Include both technical and behavioral questions.",
    "60_minutes": "This is a comprehensive interview covering multiple aspects of the candidate's qualifications. Include technical assessment, behavioral questions, and allow time for the candidate to ask questions."
}

# Call control section
st.markdown('<div class="container">', unsafe_allow_html=True)
st.subheader("Interview Control")

# Display call status
status_text = "ACTIVE" if st.session_state.call_active else "INACTIVE"
status_class = "status-active" if st.session_state.call_active else "status-inactive"
st.markdown(f"Interview Status: <span class='{status_class}'>{status_text}</span>", unsafe_allow_html=True)

# Start/Stop call buttons
col1, col2 = st.columns(2)

def start_interview():
    if not api_key:
        st.error("Please enter your Vapi API Key")
        return
    
    try:
        # Initialize Vapi instance
        vapi = Vapi(api_key=api_key)
        st.session_state.vapi_instance = vapi
        
        # Store current interview settings
        st.session_state.interview_type = interview_type
        st.session_state.interview_level = interview_level
        st.session_state.interview_duration = interview_duration
        
        # Build context for the interview
        role_context = interview_templates[interview_type][interview_level]
        company_context = company_contexts[company_type]
        duration_context = duration_contexts[interview_duration]
        
        # Combine contexts
        full_context = f"""
        You are an AI interviewer conducting a professional job interview. 
        
        {role_context}
        
        {company_context}
        
        {duration_context}
        
        Additional context about the position: {job_description if job_description else "No additional context provided."}
        
        Important guidelines:
        1. Introduce yourself as the interviewer at the beginning.
        2. Ask one question at a time and wait for the candidate's response.
        3. Listen carefully to answers and ask relevant follow-up questions.
        4. Balance technical and behavioral questions appropriate for the role and level.
        5. Be professional, courteous, and encouraging, but also thorough in your assessment.
        6. When the interview time is nearly up, let the candidate know and ask if they have any questions.
        7. Thank the candidate for their time at the end of the interview.
        
        Start the interview with a brief introduction and your first question.
        """
        
        # Create custom assistant
        assistant = {
            "firstMessage": f"Hello, I'll be conducting your interview today for the {interview_type.replace('_', ' ')} position. Let's get started with the first question.",
            "context": full_context,
            "model": "gpt-4o",
            "voice": "jennifer-playht",
            "recordingEnabled": True,
            "interruptionsEnabled": False
        }
        
        st.session_state.vapi_instance.start(assistant=assistant)
        st.session_state.call_active = True
        st.success("Interview started successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Error starting interview: {str(e)}")

def stop_interview():
    if st.session_state.vapi_instance:
        try:
            st.session_state.vapi_instance.stop()
            st.session_state.call_active = False
            st.session_state.vapi_instance = None
            st.success("Interview ended successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error stopping interview: {str(e)}")

with col1:
    if not st.session_state.call_active:
        st.button("Start Interview", on_click=start_interview, type="primary", use_container_width=True)

with col2:
    if st.session_state.call_active:
        st.button("End Interview", on_click=stop_interview, type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Interview guidance section
if st.session_state.call_active:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Interview in Progress")
    st.markdown("""
    Your interview is active. Speak into your microphone to respond to the interviewer's questions.
    
    Tips for a successful interview:
    - Speak clearly and at a moderate pace
    - Use specific examples from your experience
    - Structure your answers using the STAR method (Situation, Task, Action, Result)
    - Ask clarifying questions if needed
    - Be authentic in your responses
    
    Click "End Interview" when you're finished with the conversation.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Interview Preparation Tips")
    
    # Show different tips based on the selected role
    if interview_type == "software_engineer":
        st.markdown("""
        ### Software Engineering Interview Tips
        
        <div class="interview-question">Technical Preparation:</div>
        <div class="interview-note">Review data structures, algorithms, system design, and coding fundamentals relevant to your level.</div>
        
        <div class="interview-question">Common Questions:</div>
        - Explain a challenging technical problem you've solved
        - How do you approach debugging a complex issue?
        - Describe your experience with [relevant technologies]
        - How do you stay updated with the latest developments in software engineering?
        
        <div class="interview-question">Questions to Ask:</div>
        - What does the development process look like?
        - How is code reviewed in the team?
        - What are the biggest technical challenges the team is facing?
        """, unsafe_allow_html=True)
    elif interview_type == "data_scientist":
        st.markdown("""
        ### Data Science Interview Tips
        
        <div class="interview-question">Technical Preparation:</div>
        <div class="interview-note">Review statistics, machine learning algorithms, feature engineering, and data manipulation techniques.</div>
        
        <div class="interview-question">Common Questions:</div>
        - Describe a data science project you've worked on from start to finish
        - How do you validate your models?
        - How do you handle missing or imbalanced data?
        - Explain a complex concept to a non-technical stakeholder
        
        <div class="interview-question">Questions to Ask:</div>
        - What data infrastructure is in place?
        - How is data science integrated with the product development process?
        - What metrics matter most to the business?
        """, unsafe_allow_html=True)
    elif interview_type == "product_manager":
        st.markdown("""
        ### Product Management Interview Tips
        
        <div class="interview-question">Preparation:</div>
        <div class="interview-note">Review product development processes, prioritization frameworks, and metrics analysis.</div>
        
        <div class="interview-question">Common Questions:</div>
        - How do you prioritize features?
        - Describe a product you launched from concept to completion
        - How do you gather and incorporate user feedback?
        - Tell me about a time you had to make a difficult product decision
        
        <div class="interview-question">Questions to Ask:</div>
        - How is product success measured?
        - How do product, design, and engineering collaborate?
        - What's the product development process like?
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        ### Interview Tips
        
        <div class="interview-question">General Preparation:</div>
        <div class="interview-note">Research the company, prepare your elevator pitch, and review your experience relevant to the role.</div>
        
        <div class="interview-question">Common Questions:</div>
        - Tell me about yourself
        - Why are you interested in this role?
        - Describe a challenging situation and how you handled it
        - What are your strengths and weaknesses?
        
        <div class="interview-question">Questions to Ask:</div>
        - What does success look like in this role?
        - How would you describe the company culture?
        - What are the biggest challenges facing the team right now?
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Vapi AI")
