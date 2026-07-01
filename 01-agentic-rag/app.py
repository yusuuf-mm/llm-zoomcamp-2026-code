import streamlit as st
import time

# --- SESSION STATE INITIALIZATION ---
if "step" not in st.session_state:
    st.session_state.step = "Learn"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

st.set_page_config(page_title="Agentic RAG Study Coach", page_icon="🤖", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .lesson-header { color: #1E3A8A; font-size: 24px; font-weight: bold; margin-top: 20px; }
    .concept-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 15px; }
    .agent-thought { background-color: #FEF3C7; padding: 12px; border-radius: 6px; border-left: 4px solid #F59E0B; font-family: monospace; font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 LLM Zoomcamp: Module 1 Study Companion")
st.subheader("Mastering Agentic RAG & Production Tool Operations")

# --- NAVIGATION PIPELINE ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚀 Phase 1: Learn & Train", use_container_width=True, type="primary" if st.session_state.step == "Learn" else "secondary"):
        st.session_state.step = "Learn"
with col2:
    if st.button("💬 Phase 2: Interactive Sandbox Q&A", use_container_width=True, type="primary" if st.session_state.step == "Sandbox" else "secondary"):
        st.session_state.step = "Sandbox"
with col3:
    if st.button("🎯 Phase 3: Ace the Quiz", use_container_width=True, type="primary" if st.session_state.step == "Quiz" else "secondary"):
        st.session_state.step = "Quiz"

st.divider()

# ==============================================================================
# PHASE 1: LEARN & TRAIN (THE TRAINING GROUND)
# ==============================================================================
if st.session_state.step == "Learn":
    st.markdown("### 📚 Comprehensive Technical Training")
    st.write("Before writing code or executing agents, absorb the structural paradigm of production-grade Agentic Retrieval-Augmented Generation systems.")
    
    # Lesson 1
    st.markdown("<div class='lesson-header'>Lesson 1.1: The Architectural Shift to Agentic RAG</div>", unsafe_allow_html=True)
    st.markdown("""
    * **Core Concepts:** Traditional RAG is entirely linear (`Retrieve -> Augment -> Generate`). **Agentic RAG** introduces a loop driven by internal reasoning. The LLM acts as an orchestrator, evaluating user queries, selecting specialized tools, determining missing parameters, and validating data accuracy before rendering answers.
    * **The Decision Framework:** It relies on the decoupling of *Reasoning* and *Execution*. The model does not calculate or run lookups itself; it outputs structured directives (JSON/Tool Calls), allowing robust deterministic modules to manage heavy database/math operations.
    """)
    
    # Lesson 2
    st.markdown("<div class='lesson-header'>Lesson 1.2: Structuring Knowledge Repositories</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='concept-box'>
    <strong>Production Blueprint:</strong> To train an agent properly, documentation is partitioned logically. For instance, repositories are structured with top-level modules containing predictable <code>lessons/</code> subfolders using numbered markdown segments. This deterministic naming layout simplifies exact multi-file collection setups.
    </div>
    """, unsafe_allow_html=True)
    
    # Lesson 3
    st.markdown("<div class='lesson-header'>Lesson 1.3: Mastering Tool Use & Router Orchestration</div>", unsafe_allow_html=True)
    st.markdown("""
    * **Function Calling Rules:** Tools must provide explicit schema definitions (Name, Description, Type-Safe Arguments via Pydantic or JSON Schema). 
    * **Router Strategies:** Real-world workflows leverage complex routing meshes. For example, high-volume classification tasks route to fast, lightweight models, complex multi-step planning offloads to deep reasoning pipelines, and fallback strategies shift processing to local environments if strict rate limits (like OpenRouter's 20 RPM on free tiers) are approached.
    """)

# ==============================================================================
# PHASE 2: INTERACTIVE SANDBOX Q&A
# ==============================================================================
elif st.session_state.step == "Sandbox":
    st.markdown("### 💬 Agentic Logic Simulator")
    st.write("Test your architectural understanding or prompt this local agent simulator to observe how tool use choices and execution thoughts occur under the hood.")
    
    # Pre-baked system setup for realistic simulation
    simulated_knowledge = {
        "what is the knowledge base repository layout?": {
            "thought": "CRITICAL: Query targets repository structure. Selecting tool: 'gitsource_fetch_structure'. Argument: {'commit': '8c1834d'}",
            "answer": "The course repository organizes lessons within top-level module folders. Inside each folder, a dedicated 'lessons/' subfolder hosts sequentially numbered markdown pages containing the documentation text."
        },
        "how does openrouter route free models?": {
            "thought": "CRITICAL: Query targets fallback and routing. Selecting tool: 'openrouter_lookup_free_tier'.",
            "answer": "OpenRouter maps models via specific suffixes (e.g., ':free'). It applies a 20 requests per minute baseline. Production pipelines monitor this threshold to dynamically trigger fallback paths."
        }
    }
    
    # Render chat logs
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "thought" in message:
                st.markdown(f"<div class='agent-thought'><strong>🤖 Agent Thinking Chain:</strong><br>{message['thought']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask a question about Module 1 architecture (e.g., repository layout or OpenRouter routing)..."):
        # Display user question
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Simulate agent execution response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            normalized_prompt = prompt.lower().strip()
            
            if normalized_prompt in simulated_knowledge:
                sim_data = simulated_knowledge[normalized_prompt]
                st.markdown(f"<div class='agent-thought'><strong>🤖 Agent Thinking Chain:</strong><br>{sim_data['thought']}</div>", unsafe_allow_html=True)
                time.sleep(1) # Emulate reasoning delay
                response_placeholder.markdown(sim_data["answer"])
                st.session_state.chat_history.append({"role": "assistant", "content": sim_data["answer"], "thought": sim_data["thought"]})
            else:
                fallback_thought = "CRITICAL: General structural question. Scanning structural indexes across all loaded markdown contexts..."
                fallback_ans = f"Acknowledged. In production agent architectures, handling your question regarding '{prompt}' requires defining a strict schema, applying validation rules, and maintaining a clear historical context array to track previous conversation steps."
                st.markdown(f"<div class='agent-thought'><strong>🤖 Agent Thinking Chain:</strong><br>{fallback_thought}</div>", unsafe_allow_html=True)
                time.sleep(0.8)
                response_placeholder.markdown(fallback_ans)
                st.session_state.chat_history.append({"role": "assistant", "content": fallback_ans, "thought": fallback_thought})

# ==============================================================================
# PHASE 3: ACE THE QUIZ (THE CERTIFICATION ARENA)
# ==============================================================================
elif st.session_state.step == "Quiz":
    st.markdown("### 🎯 Module 1 Knowledge Validation")
    st.write("Demonstrate your mastery over the fundamental concepts, tool structures, and baseline limitations explored in this section.")
    
    # Form layout
    with st.form("module_1_quiz"):
        # Question 1
        st.markdown("**1. What is the standard structural layout for lessons in the course repository?**")
        q1 = st.radio("Select the correct structural format:", [
            "A single monolithic markdown file covering all modules",
            "Top-level module folders containing a 'lessons/' subfolder of numbered markdown pages",
            "An unstructured root repository containing randomly assigned PDF files",
            "Dynamic databases with no predictable static asset pathing"
        ], index=None, key="q1_choice")
        
        st.divider()
        
        # Question 2
        st.markdown("**2. Why is decoupling the 'Reasoning Layer' from 'Math/Execution' a key pattern in production systems?**")
        q2 = st.radio("Select the best engineering justification:", [
            "It allows LLMs to directly execute code natively without runtime containers",
            "It ensures deterministic calculations by using specialized tools, reducing the risk of model hallucinations during math operations",
            "It completely eliminates the requirement for writing explicit tool descriptions or schemas",
            "It requires upgrading all infrastructural assets to expensive paid tiers"
        ], index=None, key="q2_choice")
        
        st.divider()
        
        # Question 3
        st.markdown("**3. What is a key constraint to plan for when deploying basic free model routing nodes (e.g., OpenRouter)?**")
        q3 = st.radio("Select the primary restriction:", [
            "No support for function calling or structured JSON parameters",
            "A strict global baseline speed limit capped at exactly 1 request per hour",
            "A standard rate limit ceiling of 20 requests per minute on free variants, requiring robust local fallback strategies",
            "Total restriction against parsing multi-turn historical message arrays"
        ], index=None, key="q3_choice")
        
        submit_btn = st.form_submit_button("Submit Assessment")
        
        if submit_btn:
            if q1 is None or q2 is None or q3 is None:
                st.error("⚠️ Review standard compliance: Please answer all questions before submitting.")
            else:
                st.session_state.quiz_answers = {"q1": q1, "q2": q2, "q3": q3}
                st.session_state.quiz_submitted = True

    # Performance evaluation
    if st.session_state.quiz_submitted and st.session_state.quiz_answers:
        st.markdown("### 📊 Performance Report Card")
        score = 0
        
        # Eval Q1
        if "lessons/ subfolder of numbered markdown pages" in st.session_state.quiz_answers["q1"]:
            st.success("✅ **Question 1 Correct!** You correctly identified the standard `lessons/` subfolder repository blueprint.")
            score += 1
        else:
            st.error("❌ **Question 1 Incorrect.** Remember, production repositories segment files inside clean, predictable module paths.")
            
        # Eval Q2
        if "ensures deterministic calculations" in st.session_state.quiz_answers["q2"]:
            st.success("✅ **Question 2 Correct!** Exactly. Offloading tasks to solvers/tools ensures exact mathematical correctness.")
            score += 1
        else:
            st.error("❌ **Question 2 Incorrect.** Re-evaluate the split between language processing and exact computations.")
            
        # Eval Q3
        if "20 requests per minute" in st.session_state.quiz_answers["q3"]:
            st.success("✅ **Question 3 Correct!** Spot on. Managing the 20 RPM boundary ensures smooth routing and graceful local fallback execution.")
            score += 1
        else:
            st.error("❌ **Question 3 Incorrect.** Review the specific API limits applied to infrastructure free tiers.")
            
        # Summary Display
        st.metric(label="Final Module Score", value=f"{score} / 3", delta="Passed" if score == 3 else "Needs Review")
        if score == 3:
            st.balloons()
            st.success("🏆 Perfect Score! You have fully mastered the architectural fundamentals of Module 1.")
