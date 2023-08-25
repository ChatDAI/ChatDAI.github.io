import streamlit as st
from SparkApi import Spark
from GetPunchline import getPunchline
from pl2pm import getPrimitive

appid = "d3b845b3"     
api_secret = "MDJlNzUzZjFmMmMxYjczNDYwYzgwZGYw" 
api_key ="0c4fe32b0543b84e4664680876a33853"    
domain = "general"  
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  
text = []

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

st.markdown("# DuanzAI")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_area("You:",key='input')

if user_input:
    punchline = getPunchline(user_input)
    primitive = None
    if(len(punchline)>0):
        primitive=getPrimitive(punchline)
    if(primitive is not None):
        prompt=f"这里有五个示例。示例1：输入：老王没有温度感觉，身后都着火了，全燃不知。 分析：这是一句谐音梗，“全燃不知”是“全然不知”的谐音。在这句笑话的描述中，老王燃起来了却没有感觉，解释了为什么全燃不知，与谐音词全然不知意义不同，带来了幽默的效果。；示例2：输入：气象局把大象给气死了。 分析：这是一句双关梗，气象局本来是发布天气的机构，但把气和象拆开来可以理解为使大象生气，由此产生了歧义，产生了幽默的效果。；示例3：输入：“都说江南水香，我怎么闻不到？” 分析：这是一句谐音梗，“江南水香”是“江南水乡”的谐音，“水乡”本身是对江南流水美景的赞美，“乡”被谐音为“香”后意思变成了水有香味，由此产生了幽默的效果。；示例4：输入：啊！矩阵！啊！行列式！啊！特征向量！这是一首《线代诗》。 分析：这是一句谐音梗，前面是一首和线性代数（简称为线代）有关的诗，因此可被称为”线代诗”，其刚好为“现代诗”的谐音，带来了幽默的效果。；示例5：输入：宅是一种房沉迷。 分析：这是一句谐音梗，宅指的是一直在沉迷在房间中不出去，因此可以叫“房沉迷”，其又是“防沉迷”的谐音，产生了幽默的效果。。以上的示例是对每句笑话的幽默分析，接下来我会给一句笑话，你的任务是理解和分析幽默所在。“{user_input}”这句笑话的笑点在“{punchline}”，谐音“{primitive}”，请你尝试分析它的幽默之处。"
    else:
        prompt="你现在扮演的角色叫做“DuanzAI”，中文名叫“段仔”，是一个幽默理解人工智能，请回答下面的问题：" + user_input
    question = checklen(getText("user",prompt))
    duanzai = Spark(appid,api_key,api_secret,Spark_url,domain,question)
    output=duanzai.answer
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # message(st.session_state["generated"][i], key=str(i))
        st.markdown(f'''**AI:** {st.session_state["generated"][i]}''')
        # message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st.markdown(f'''**You:** {st.session_state['past'][i]}''')
