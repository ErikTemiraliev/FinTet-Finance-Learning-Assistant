import profile

import streamlit as st
import json
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="FinTet 金融学习助手",
    layout="wide"
)

# -----------------------------
# Dark AI assistant CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #202020;
    color: #e5e5e5;
}

footer {
    visibility: hidden;
}

header {
    background: #202020 !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1120px;
}

section[data-testid="stSidebar"] {
    background-color: #181818;
    border-right: 1px solid #333333;
}

section[data-testid="stSidebar"] * {
    color: #e5e5e5 !important;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 4px;
    color: #ffffff;
}

.sidebar-subtitle {
    font-size: 14px;
    color: #9ca3af;
    margin-bottom: 30px;
}

.hero {
    text-align: center;
    margin-top: 110px;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #f5f5f5;
    margin-bottom: 18px;
}

.hero-subtitle {
    font-size: 17px;
    color: #a3a3a3;
    line-height: 1.8;
}

.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 40px;
    margin-bottom: 12px;
}

.section-desc {
    font-size: 16px;
    color: #a3a3a3;
    margin-bottom: 30px;
    line-height: 1.7;
}

.user-bubble {
    background-color: #334155;
    color: #ffffff;
    padding: 16px 18px;
    border-radius: 18px;
    margin-top: 20px;
    margin-bottom: 14px;
    line-height: 1.7;
}

.ai-bubble {
    background-color: #303030;
    color: #e5e5e5;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #444444;
    margin-bottom: 14px;
    line-height: 1.8;
}

.stTextInput input,
.stTextArea textarea {
    background-color: #2b2b2b !important;
    color: #ffffff !important;
    border: 1px solid #4b5563 !important;
    border-radius: 18px !important;
    padding: 14px 18px !important;
    font-size: 16px !important;
    box-shadow: none !important;
    outline: none !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
    outline: none !important;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label {
    font-size: 15px !important;
    color: #cfcfcf !important;
    margin-bottom: 6px !important;
}

div[data-baseweb="select"] > div {
    background-color: #303030 !important;
    color: #ffffff !important;
    border-radius: 16px !important;
    border: 1px solid #4b5563 !important;
}

.stButton button {
    background-color: #333333 !important;
    color: #e5e5e5 !important;
    border: 1px solid #444444 !important;
    border-radius: 18px !important;
    padding: 0.65rem 1.1rem !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    min-height: 46px !important;
    box-shadow: none !important;
}

.stButton button:hover {
    background-color: #3b82f6 !important;
    color: white !important;
    border: 1px solid #3b82f6 !important;
}

.stAlert {
    border-radius: 16px;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.8rem;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Knowledge base
# -----------------------------
def load_knowledge_base():
    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        return file.read()


def retrieve_knowledge(question):
    knowledge = load_knowledge_base()
    sections = knowledge.split("\n\n")
    related_content = []

    for section in sections:
        for word in question.lower().split():
            if word in section.lower():
                related_content.append(section)
                break

    if related_content:
        return "\n\n".join(related_content[:2])
    else:
        return "No directly related content was found in the knowledge base."

# -----------------------------
# Mood-based companion feedback
# 基于情绪的陪伴式反馈
# -----------------------------
def get_mood_feedback(mood):
    if "Confident" in mood or "有信心" in mood:
        return """
<b>陪伴式反馈 / Companion feedback:</b><br>
你今天状态不错！我会给你稍微更有挑战性的解释和练习，帮助你进一步提升。<br>
You seem confident today. I will give you a slightly more challenging explanation and practice to help you improve further.
<br><br>
"""
    elif "Confused" in mood or "困惑" in mood:
        return """
<b>陪伴式反馈 / Companion feedback:</b><br>
不用担心，这个知识点对初学者来说很常见。我们一步一步来看。<br>
Don’t worry. This topic is common for beginners. Let’s understand it step by step.
<br><br>
"""
    elif "Stressed" in mood or "压力大" in mood:
        return """
<b>陪伴式反馈 / Companion feedback:</b><br>
先放轻松，我们只专注一个小知识点。完成一个小步骤就很好。<br>
Take it easy. Let’s focus on only one small concept first. Finishing one small step is already good progress.
<br><br>
"""
    elif "Tired" in mood or "疲惫" in mood:
        return """
<b>陪伴式反馈 / Companion feedback:</b><br>
你可能有点累了，所以我会用更简短的方式解释，并给你一个简单例子。<br>
You may be tired, so I will explain it briefly and give you a simple example.
<br><br>
"""
    elif "Curious" in mood or "好奇" in mood:
        return """
<b>陪伴式反馈 / Companion feedback:</b><br>
很好！保持好奇心很重要。我会结合生活中的金融例子来解释。<br>
Great! Curiosity is important. I will explain this with real-life finance examples.
<br><br>
"""
    else:
        return """
<b>陪伴式反馈 / Companion feedback:</b><br>
我们继续学习金融基础知识，我会根据你的问题给出清晰的解释。<br>
Let’s continue learning finance. I will give you a clear explanation based on your question.
<br><br>
"""
# -----------------------------
# Q&A function
# -----------------------------
def answer_question(question):
    context = retrieve_knowledge(question)
    mood_feedback = get_mood_feedback(st.session_state.current_mood)
    profile = load_user_profile()

    profile["last_studied_topic"] = question
    profile["current_mood"] = st.session_state.current_mood
    save_user_profile(profile)

    user_name = profile.get("user_name", "Student")
    finance_level = profile.get("finance_level", "Beginner / 初学者")
    preferred_style = profile.get("preferred_style", "Step-by-step / 分步骤解释")

    answer = f"""
{mood_feedback}

<b>用户画像 / User profile:</b><br>
学习者 / Learner: {user_name}<br>
金融水平 / Finance level: {finance_level}<br>
学习偏好 / Preferred style: {preferred_style}<br><br>

<b>知识库相关内容 / Related knowledge:</b><br><br>
{context}<br><br>

<b>结构化回答 / Structured answer:</b><br><br>

<b>1. 定义 / Definition:</b><br>
该问题与金融基础知识相关。<br>
This question is related to basic finance concepts.<br><br>

<b>2. 原理 / Explanation:</b><br>
系统会先从金融知识库中检索相关内容，然后结合检索结果生成回答。<br>
The system first retrieves related content from the finance knowledge base, then generates an answer.<br><br>

<b>3. 示例 / Example:</b><br>
例如，复利是指利息不仅按照本金计算，也按照之前产生的利息继续计算。<br>
For example, compound interest means interest is calculated on both principal and accumulated interest.<br><br>

<b>4. 易错点 / Common mistake:</b><br>
学生容易混淆单利和复利。<br>
Students often confuse simple interest and compound interest.
"""
    return answer


# -----------------------------
# Exercise generation
# -----------------------------
def generate_exercise(topic):
    if topic == "Simple Interest":
        return "题目：如果你存入1000元，年利率为5%，存2年，按照单利计算可以获得多少利息？"
    elif topic == "Compound Interest":
        return "题目：如果你存入1000元，年利率为5%，存2年，按照复利计算最终金额是多少？"
    elif topic == "Risk and Return":
        return "题目：请解释为什么较高的预期收益通常伴随着较高风险。"
    elif topic == "Stock":
        return "题目：股票代表什么？"
    elif topic == "Bond":
        return "题目：股票和债券有什么区别？"
    else:
        return "题目：请解释一个金融基础概念并举例。"


# -----------------------------
# Answer evaluation
# -----------------------------
def evaluate_answer(topic, student_answer):
    student_answer_lower = student_answer.lower()

    if topic == "Simple Interest":
        if "100" in student_answer_lower:
            return "正确 / Correct：回答正确。单利 = 1000 × 5% × 2 = 100 元。"
        else:
            return "错误 / Wrong：回答错误。正确计算为 1000 × 5% × 2 = 100 元。"

    elif topic == "Compound Interest":
        if "1102.5" in student_answer_lower or "1102.50" in student_answer_lower:
            return "正确 / Correct：回答正确。复利终值 = 1000 × (1 + 5%)² = 1102.50 元。"
        else:
            return "错误 / Wrong：回答错误。正确答案是 1102.50 元，需要使用复利公式 FV = Principal × (1 + Rate)^Time。"

    elif topic == "Risk and Return":
        if "risk" in student_answer_lower and "return" in student_answer_lower:
            return "正确 / Correct：基本正确，你解释了风险与收益之间的关系。"
        elif "风险" in student_answer or "收益" in student_answer:
            return "正确 / Correct：基本正确，较高预期收益通常伴随较高风险。"
        else:
            return "不完整 / Incomplete：回答不完整，应说明较高预期收益通常伴随较高风险。"

    elif topic == "Stock":
        if "ownership" in student_answer_lower or "company" in student_answer_lower:
            return "正确 / Correct：回答正确，股票代表对一家公司的部分所有权。"
        elif "公司" in student_answer or "所有权" in student_answer:
            return "正确 / Correct：回答正确，股票代表对一家公司的部分所有权。"
        else:
            return "错误 / Wrong：回答错误，股票代表对一家公司的部分所有权。"

    elif topic == "Bond":
        if "debt" in student_answer_lower or "loan" in student_answer_lower or "lend" in student_answer_lower:
            return "正确 / Correct：基本正确，债券是一种债务工具。"
        elif "债务" in student_answer or "借款" in student_answer:
            return "正确 / Correct：基本正确，债券是一种债务工具。"
        else:
            return "不完整 / Incomplete：回答不完整，债券表示投资者把钱借给发行人。"

    else:
        return "不完整 / Incomplete：答案已记录，请与知识库内容进行对比。"


# -----------------------------
# Learning history
# -----------------------------
def save_history(topic, answer, feedback):
    record = {
        "topic": topic,
        "student_answer": answer,
        "feedback": feedback
    }

    if os.path.exists("student_history.json"):
        with open("student_history.json", "r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    history.append(record)

    with open("student_history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


def diagnose_weak_points():
    if not os.path.exists("student_history.json"):
        return "没有找到学习记录。"

    with open("student_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)

    weak_points = []

    for record in history:
        feedback = record["feedback"]
        if "错误" in feedback or "不完整" in feedback:
            weak_points.append(record["topic"])

    if weak_points:
        return "薄弱知识点 / Weak points: " + ", ".join(list(set(weak_points)))
    else:
        return "暂未发现明显薄弱点，学生掌握情况较好。"


# -----------------------------
# Personalized learning plan
# 个性化学习计划
# -----------------------------
def generate_learning_plan():
    profile = load_user_profile()
    progress = get_progress_data()

    user_name = profile.get("user_name", "Student")
    finance_level = profile.get("finance_level", "Beginner / 初学者")
    current_mood = profile.get("current_mood", "Normal / 一般")
    preferred_style = profile.get("preferred_style", "Step-by-step / 分步骤解释")
    last_topic = profile.get("last_studied_topic", "None")

    weak_topics = progress.get("weak_topics", [])
    accuracy = progress.get("accuracy", 0)
    total_exercises = progress.get("total_exercises", 0)

    if weak_topics:
        weak_topic_text = "、".join(weak_topics)
        focus_topic = weak_topics[0]
    else:
        weak_topic_text = "暂未发现明显薄弱知识点"
        focus_topic = "new finance concepts / 新的金融基础概念"

    # Mood-based plan style
    if "Confused" in current_mood or "困惑" in current_mood:
        mood_strategy = "你当前状态是困惑，建议采用分步骤学习方式，先复习概念，再看例子，最后做简单练习。"
        english_mood_strategy = "Since your current mood is confused, the plan should be step-by-step: review the concept first, then study an example, and finally complete a simple exercise."
    elif "Stressed" in current_mood or "压力大" in current_mood:
        mood_strategy = "你当前压力较大，建议减少学习负担，每次只完成一个小任务。"
        english_mood_strategy = "Since you feel stressed, the plan should reduce learning pressure and focus on one small task at a time."
    elif "Tired" in current_mood or "疲惫" in current_mood:
        mood_strategy = "你当前比较疲惫，建议使用短时间学习法，每次学习 15–20 分钟。"
        english_mood_strategy = "Since you feel tired, the plan should use short study sessions of 15–20 minutes."
    elif "Confident" in current_mood or "有信心" in current_mood:
        mood_strategy = "你当前比较有信心，可以尝试更有挑战性的练习题。"
        english_mood_strategy = "Since you feel confident, you can try slightly more challenging exercises."
    else:
        mood_strategy = "你当前状态稳定，可以按照正常节奏继续学习。"
        english_mood_strategy = "Your current state is stable, so you can continue learning at a normal pace."

    plan = f"""
### 个性化学习计划 / Personalized Learning Plan

**学习者 / Learner:** {user_name}  
**金融水平 / Finance level:** {finance_level}  
**当前学习状态 / Current mood:** {current_mood}  
**学习偏好 / Preferred style:** {preferred_style}  
**最近学习主题 / Last studied topic:** {last_topic}  
**完成练习数量 / Total exercises:** {total_exercises}  
**当前正确率 / Current accuracy:** {accuracy}%  
**薄弱知识点 / Weak topics:** {weak_topic_text}  

---

### 1. 学习状态分析 / Learning Status Analysis

根据用户画像和历史答题记录，系统发现当前需要重点关注的内容是：**{focus_topic}**。

Based on the user profile and answer history, the system suggests focusing on: **{focus_topic}**.

{mood_strategy}

{english_mood_strategy}

---

### 2. 今日学习目标 / Today's Learning Goal

1. 复习一个核心金融概念。  
2. 完成一道相关练习题。  
3. 查看系统反馈并记录薄弱点。  
4. 根据反馈调整下一步学习内容。  

1. Review one core finance concept.  
2. Complete one related exercise.  
3. Check system feedback and record weak points.  
4. Adjust the next learning content based on feedback.  

---

### 3. 推荐学习步骤 / Recommended Study Steps

**Step 1：概念复习 / Concept Review**  
先复习 **{focus_topic}** 的基本定义、公式或核心原理。  

**Step 2：例子理解 / Example Understanding**  
结合一个生活化金融例子理解该知识点，例如存款利息、股票投资或债券收益。  

**Step 3：练习巩固 / Practice**  
完成一题相关练习，并在“答案反馈”页面提交答案。  

**Step 4：反馈反思 / Feedback Reflection**  
根据系统反馈判断自己是否真正理解该知识点。  

**Step 5：下一次学习 / Next Session**  
如果仍然答错，继续复习该薄弱知识点；如果答对，可以进入下一个金融主题。  

---

### 4. 陪伴式建议 / Companion Suggestion

FinTet 建议你不要一次学习太多内容。今天只需要完成一个小目标：  
**理解 {focus_topic} 并完成一道练习题。**

FinTet suggests not learning too much at once. Today, you only need to complete one small goal:  
**Understand {focus_topic} and finish one related exercise.**
"""
    return plan
# -----------------------------
# Save answer record
# 保存答题记录
# -----------------------------
def save_answer_record(topic, question, student_answer, correct_answer, feedback):
    if os.path.exists("student_history.json"):
        with open("student_history.json", "r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    record = {
        "topic": topic,
        "question": question,
        "student_answer": student_answer,
        "correct_answer": correct_answer,
        "feedback": feedback
    }

    history.append(record)

    with open("student_history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
# -----------------------------
# User profile memory
# 用户画像记忆
# -----------------------------
def load_user_profile():
    if os.path.exists("user_profile.json"):
        with open("user_profile.json", "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {
            "user_name": "Student",
            "finance_level": "Beginner / 初学者",
            "preferred_style": "Step-by-step / 分步骤解释",
            "current_mood": "Normal / 一般",
            "last_studied_topic": "None"
        }


def save_user_profile(profile):
    with open("user_profile.json", "w", encoding="utf-8") as file:
        json.dump(profile, file, ensure_ascii=False, indent=4)


def update_profile_field(key, value):
    profile = load_user_profile()
    profile[key] = value
    save_user_profile(profile)
# -----------------------------
# Session state
# -----------------------------
if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "auto_answer" not in st.session_state:
    st.session_state.auto_answer = False
# -----------------------------
# Mood check-in state
# 情绪状态记录
# -----------------------------
if "current_mood" not in st.session_state:
    st.session_state.current_mood = "Normal / 一般"
if "user_profile" not in st.session_state:
    st.session_state.user_profile = load_user_profile()
# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("""
<div class="sidebar-title">FinTet</div>
<div class="sidebar-subtitle">AI 金融学习陪伴体</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 今日学习状态 / Today's mood")

st.session_state.current_mood = st.sidebar.selectbox(
    "你今天学习金融的状态如何？ / How do you feel about studying finance today?",
    [
        "Normal / 一般",
        "Confident / 有信心",
        "Confused / 困惑",
        "Stressed / 压力大",
        "Tired / 疲惫",
        "Curious / 好奇"
    ]
)

st.sidebar.caption(f"当前状态 / Current mood: {st.session_state.current_mood}")
# Save current mood into user profile
st.session_state.user_profile["current_mood"] = st.session_state.current_mood
save_user_profile(st.session_state.user_profile)

st.sidebar.markdown("---")
st.sidebar.markdown("### 用户画像 / User Profile")

user_name = st.sidebar.text_input(
    "你的名字 / Your name",
    value=st.session_state.user_profile.get("user_name", "Student")
)

finance_level_options = [
    "Beginner / 初学者",
    "Intermediate / 中级",
    "Advanced / 高级"
]

finance_level = st.sidebar.selectbox(
    "金融学习水平 / Finance level",
    finance_level_options,
    index=finance_level_options.index(
        st.session_state.user_profile.get("finance_level", "Beginner / 初学者")
    )
)

preferred_style_options = [
    "Step-by-step / 分步骤解释",
    "Short explanation / 简短解释",
    "Example-based / 多举例解释",
    "Practice-based / 多练习"
]

preferred_style = st.sidebar.selectbox(
    "偏好的学习方式 / Preferred learning style",
    preferred_style_options,
    index=preferred_style_options.index(
        st.session_state.user_profile.get("preferred_style", "Step-by-step / 分步骤解释")
    )
)

if st.sidebar.button("保存用户画像 / Save Profile"):
    st.session_state.user_profile["user_name"] = user_name
    st.session_state.user_profile["finance_level"] = finance_level
    st.session_state.user_profile["preferred_style"] = preferred_style
    st.session_state.user_profile["current_mood"] = st.session_state.current_mood

    save_user_profile(st.session_state.user_profile)
    st.sidebar.success("用户画像已保存 / Profile saved")
menu = st.sidebar.selectbox(
    "选择功能 / Choose a function",
    [
        "金融知识问答 / Finance Q&A",
        "练习题生成 / Generate Exercise",
        "答案反馈 / Answer Feedback",
        "学情诊断 / Learning Diagnosis",
        "学习进度 / Progress Dashboard",
        "学习计划 / Learning Plan"
    ]
)

# -----------------------------
# Finance Q&A page
# -----------------------------
if menu == "金融知识问答 / Finance Q&A":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">欢迎回来，今天继续一起学习金融吧</div>
        <div class="hero-subtitle">
            FinTet AI 金融学习陪伴体<br>
            系统会根据你的学习状态、用户画像、历史记录和薄弱知识点，提供个性化学习支持。
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("解释什么是复利"):
            st.session_state.selected_question = "What is compound interest?"
            st.session_state.auto_answer = True

    with col2:
        if st.button("什么是股票？"):
            st.session_state.selected_question = "What is a stock?"
            st.session_state.auto_answer = True

    with col3:
        if st.button("债券和股票的区别"):
            st.session_state.selected_question = "What is the difference between a bond and a stock?"
            st.session_state.auto_answer = True

    with col4:
        if st.button("风险与收益关系"):
            st.session_state.selected_question = "What is the relationship between risk and return?"
            st.session_state.auto_answer = True

    question = st.text_input(
        "请输入你的金融问题 / Please enter your finance question:",
        value=st.session_state.selected_question,
        placeholder="例如：What is compound interest?"
    )

    send_clicked = False

    if st.button("发送 / Send"):
        send_clicked = True

    if send_clicked:
        st.session_state.selected_question = question
        st.session_state.auto_answer = True

    if st.session_state.auto_answer and question.strip() != "":
        st.markdown(f"""
        <div class="user-bubble">
            <b>你 / Student：</b><br>{question}
        </div>
        """, unsafe_allow_html=True)

        answer = answer_question(question)

        st.markdown(f"""
        <div class="ai-bubble">
            <b>FinTet：</b><br>{answer}
        </div>
        """, unsafe_allow_html=True)

        st.session_state.auto_answer = False

    elif send_clicked and question.strip() == "":
        st.warning("请输入问题。")


# -----------------------------
# Exercise page
# -----------------------------
elif menu == "练习题生成 / Generate Exercise":
    st.markdown('<div class="section-title">练习题生成 / Generate Exercise</div>', unsafe_allow_html=True)
    st.markdown(
    '<div class="section-desc">系统会根据金融主题生成基础练习题，帮助用户巩固知识点。</div>',
    unsafe_allow_html=True
)
    topic = st.selectbox(
        "选择知识点 / Choose a topic",
        ["Simple Interest", "Compound Interest", "Risk and Return", "Stock", "Bond"]
    )

    if st.button("生成练习 / Generate Exercise"):
        st.success(generate_exercise(topic))


# -----------------------------
# Feedback page
# -----------------------------
if menu == "答案反馈 / Answer Feedback":
    st.markdown('<div class="section-title">答案反馈 / Answer Feedback</div>', unsafe_allow_html=True)
    st.markdown(
    '<div class="section-desc">输入你的答案，系统会判断正确性并保存答题记录。</div>',
    unsafe_allow_html=True
)

    topic = st.selectbox(
        "选择练习主题 / Choose the exercise topic",
        ["Simple Interest", "Compound Interest", "Risk and Return", "Stock", "Bond"]
    )

    # Show question according to selected topic
    if topic == "Simple Interest":
        st.info("题目 / Question: If the principal is 1000, rate is 5%, and time is 2 years, what is the simple interest?")
    elif topic == "Compound Interest":
        st.info("题目 / Question: If the principal is 1000, rate is 5%, and time is 2 years, what is the future value with compound interest?")
    elif topic == "Risk and Return":
        st.info("题目 / Question: Explain the relationship between risk and return.")
    elif topic == "Stock":
        st.info("题目 / Question: What does a stock represent?")
    elif topic == "Bond":
        st.info("题目 / Question: What is a bond?")

    student_answer = st.text_area(
        "请输入你的答案 / Enter your answer:",
        key="answer_feedback_input"
    )

    submitted = st.button("提交答案 / Submit Answer")

    if submitted:
        if student_answer.strip() == "":
            st.warning("请输入答案 / Please enter your answer.")
        else:
            feedback = evaluate_answer(topic, student_answer)
            save_history(topic, student_answer, feedback)

            if feedback.startswith("正确 / Correct"):
                st.success(feedback)
            elif feedback.startswith("错误 / Wrong") or feedback.startswith("不完整 / Incomplete"):
                st.error(feedback)
            else:
                st.warning(feedback)

            st.info("答题记录已保存 / Answer record saved.")

# -----------------------------
# Progress dashboard data
# 学习进度统计
# -----------------------------
def get_progress_data():
    if os.path.exists("student_history.json"):
        with open("student_history.json", "r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    total_exercises = len(history)
    correct_count = 0
    wrong_count = 0
    weak_topics = []

    for record in history:
        feedback = record.get("feedback", "")
        topic = record.get("topic", "Unknown")

        if feedback.startswith("正确 / Correct"):
            correct_count += 1
        elif feedback.startswith("错误 / Wrong") or feedback.startswith("不完整 / Incomplete"):
            wrong_count += 1
            weak_topics.append(topic)

    weak_topics = list(set(weak_topics))

    if total_exercises > 0:
        accuracy = round((correct_count / total_exercises) * 100, 1)
    else:
        accuracy = 0

    return {
        "total_exercises": total_exercises,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "accuracy": accuracy,
        "weak_topics": weak_topics
    }
# -----------------------------
# Diagnosis page
# -----------------------------
if menu == "学情诊断 / Learning Diagnosis":
    st.markdown('<div class="section-title">学情诊断 / Learning Diagnosis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">系统会根据历史答题记录分析薄弱知识点。</div>',
        unsafe_allow_html=True
    )
    if st.button("开始诊断 / Start Diagnosis"):
        st.warning(diagnose_weak_points())


# -----------------------------
# Plan page
# -----------------------------
if menu == "学习计划 / Learning Plan":
    st.markdown('<div class="section-title">个性化学习计划 / Personalized Learning Plan</div>', unsafe_allow_html=True)
    st.markdown(
    '<div class="section-desc">系统会根据用户画像、学习状态、历史答题记录和薄弱知识点生成个性化学习计划。</div>',
    unsafe_allow_html=True
)

    if st.button("生成计划 / Generate Plan"):
        st.markdown(generate_learning_plan())

# -----------------------------
# Progress Dashboard page
# 学习进度面板
# -----------------------------
elif menu == "学习进度 / Progress Dashboard":
    st.markdown('<div class="section-title">学习进度面板 / Progress Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">系统会根据用户画像和历史答题记录展示长期学习状态。</div>',
        unsafe_allow_html=True
    )

    profile = load_user_profile()
    progress = get_progress_data()

    st.markdown("### 用户画像 / User Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("学习者 / Learner", profile.get("user_name", "Student"))

    with col2:
        st.metric("当前状态 / Current mood", profile.get("current_mood", "Normal / 一般"))

    with col3:
        st.metric("金融水平 / Finance level", profile.get("finance_level", "Beginner / 初学者"))

    st.markdown("### 学习记录 / Learning Records")

    col4, col5, col6, col7 = st.columns(4)

    with col4:
        st.metric("完成练习 / Exercises", progress["total_exercises"])

    with col5:
        st.metric("正确次数 / Correct", progress["correct_count"])

    with col6:
        st.metric("错误次数 / Wrong", progress["wrong_count"])

    with col7:
        st.metric("正确率 / Accuracy", f'{progress["accuracy"]}%')

    st.markdown("### 个性化学习状态 / Personalized Learning Status")

    st.info(f'最近学习主题 / Last studied topic: {profile.get("last_studied_topic", "None")}')
    st.info(f'学习偏好 / Preferred style: {profile.get("preferred_style", "Step-by-step / 分步骤解释")}')

    if progress["weak_topics"]:
        st.warning("薄弱知识点 / Weak topics: " + ", ".join(progress["weak_topics"]))
    else:
        st.success("暂未发现明显薄弱知识点 / No obvious weak topics found yet.")

    st.markdown("### 下一步建议 / Recommended Next Step")

    if progress["weak_topics"]:
        st.write("建议优先复习以下薄弱知识点，并完成相关练习：")
        st.write("It is recommended to review the weak topics first and complete related exercises.")
        for topic in progress["weak_topics"]:
            st.write(f"- {topic}")
    else:
        st.write("建议继续学习新的金融基础概念，并保持练习。")
        st.write("You can continue learning new finance concepts and keep practicing.")