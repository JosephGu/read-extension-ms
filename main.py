import os
from fastapi import FastAPI, status
from openai import OpenAI

app = FastAPI()


@app.get("/getBooks", status_code=status.HTTP_200_OK)
def root():
    return {
        "message": [
            {"series": "RAZ", "level": "T", "name": "Nuclear Energy: Benefits and Risks"},
            {"series": "RAZ", "level": "T", "name": "Ancient Greek Philosophy: Thinkers and Ideas"},
            {"series": "RAZ", "level": "T", "name": "Climate Modeling: Predicting Weather Patterns"},
            {"series": "RAZ", "level": "T", "name": "The American Civil War: Causes and Battles"},
            {"series": "RAZ", "level": "T", "name": "Biomes of the World: Ecosystem Diversity"},
            {"series": "RAZ", "level": "T", "name": "The History of Photography: From Daguerreotypes to Digital"},
            {"series": "RAZ", "level": "T", "name": "Honey Bees: Colony Life and Pollination"},
            {"series": "RAZ", "level": "T", "name": "The Roman Empire: Expansion and Fall"},
            {"series": "RAZ", "level": "T", "name": "Renewable Resources: Geothermal and Hydro Power"},
            {"series": "RAZ", "level": "T", "name": "Shakespeare: Life and Famous Plays"},
            {"series": "RAZ", "level": "T", "name": "Desert Animals: Survival Strategies"},
            {"series": "RAZ", "level": "T", "name": "The Industrial Revolution in Europe"},
            {"series": "RAZ", "level": "T", "name": "Astronomy: The Sun and Its Influence"},
            {"series": "RAZ", "level": "T", "name": "Endangered Plants: Conservation Efforts"},
            {"series": "RAZ", "level": "T", "name": "Medieval Castles: Design and Function"},
            {"series": "RAZ", "level": "T", "name": "Genetics: Inherited Traits and Disorders"},
            {"series": "RAZ", "level": "T", "name": "Ocean Currents: Climate and Marine Life"},
            {"series": "RAZ", "level": "T", "name": "The Silk Road: Merchants and Cultures"},
            {"series": "RAZ", "level": "T", "name": "Robotics: From Factory to Home"},
            {"series": "RAZ", "level": "T", "name": "Volcanic Eruptions: Past and Present"},
            {"series": "RAZ", "level": "T", "name": "Folk Tales: Moral Lessons and Traditions"},
            {"series": "RAZ", "level": "T", "name": "The History of Medicine: Early Treatments"},
            {"series": "RAZ", "level": "T", "name": "Solar Systems Beyond Our Own"},
            {"series": "RAZ", "level": "T", "name": "Urban Gardens: Green Spaces in Cities"},
            {"series": "RAZ", "level": "T", "name": "The French and Indian War: Colonial Conflicts"},
            {"series": "RAZ", "level": "T", "name": "Bird Migration: Patterns and Reasons"},
            {"series": "RAZ", "level": "T", "name": "Computer Programming: Basic Coding"},
            {"series": "RAZ", "level": "T", "name": "Glaciers: Melting and Climate Impact"},
            {"series": "RAZ", "level": "T", "name": "Ancient Egyptian Religion: Gods and Rituals"},
            {"series": "RAZ", "level": "T", "name": "Music Genres: From Classical to Hip-Hop"},
            {"series": "RAZ", "level": "U", "name": "The History of Mathematics: From Ancient to Modern"},
            {"series": "RAZ", "level": "U", "name": "Biotechnology Advancements in Medicine"},
            {"series": "RAZ", "level": "U", "name": "Cold War Politics: Superpower Conflicts"},
            {"series": "RAZ", "level": "U", "name": "Early Human Migration: Out of Africa"},
            {"series": "RAZ", "level": "U", "name": "Renewable Energy: Wind and Solar Innovations"},
            {"series": "RAZ", "level": "U", "name": "Ancient Mesopotamian Civilizations"},
            {"series": "RAZ", "level": "U", "name": "The Science of Memory: How We Remember"},
            {"series": "RAZ", "level": "U", "name": "Rainforest Conservation: Fighting Deforestation"},
            {"series": "RAZ", "level": "U", "name": "The American Revolution: Key Events"},
            {"series": "RAZ", "level": "U", "name": "Robotics in Manufacturing: Automation"},
            {"series": "RAZ", "level": "U", "name": "Marine Biology: Deep-Sea Creatures"},
            {"series": "RAZ", "level": "U", "name": "The Evolution of Written Language"},
            {"series": "RAZ", "level": "U", "name": "Earthquakes: Prediction and Preparedness"},
            {"series": "RAZ", "level": "U", "name": "Renaissance Art: Techniques and Artists"},
            {"series": "RAZ", "level": "U", "name": "Genetics: The Code of Life"},
            {"series": "RAZ", "level": "U", "name": "The Silk Road: Trade and Ideas"},
            {"series": "RAZ", "level": "U", "name": "Astronomy: Exploring Distant Galaxies"},
            {"series": "RAZ", "level": "U", "name": "Urban Sprawl: Environmental Impact"},
            {"series": "RAZ", "level": "U", "name": "The History of Aviation: From Hot Air Balloons to Jets"},
            {"series": "RAZ", "level": "U", "name": "Invasive Species: Threats to Ecosystems"},
            {"series": "RAZ", "level": "U", "name": "Medieval Universities: Origins of Higher Education"},
            {"series": "RAZ", "level": "U", "name": "Quantum Physics: The Basics of Subatomic Particles"},
            {"series": "RAZ", "level": "U", "name": "Folk Music: Traditions Around the World"},
            {"series": "RAZ", "level": "U", "name": "Volcanoes: Monitoring and Research"},
            {"series": "RAZ", "level": "U", "name": "The French Revolution: Causes and Effects"},
            {"series": "RAZ", "level": "U", "name": "Animal Intelligence: Problem-Solving Abilities"},
            {"series": "RAZ", "level": "U", "name": "Digital Art: From Pixels to Virtual Reality"},
            {"series": "RAZ", "level": "U", "name": "Desertification: Spreading Arid Lands"},
            {"series": "RAZ", "level": "U", "name": "The History of the Olympics"},
            {"series": "RAZ", "level": "U", "name": "Neuroscience: Mapping the Brain"},
            {"series": "RAZ", "level": "V", "name": "Quantum Computing Breakthroughs"},
            {"series": "RAZ", "level": "V", "name": "Indigenous Cultures of the World"},
            {"series": "RAZ", "level": "V", "name": "Neanderthal History and Archaeology"},
            {"series": "RAZ", "level": "V", "name": "The Evolution of Modern Medicine"},
            {"series": "RAZ", "level": "V", "name": "Urbanization: Growth and Challenges"},
            {"series": "RAZ", "level": "V", "name": "Birds of Prey: Hunting and Survival"},
            {"series": "RAZ", "level": "V", "name": "The History of the Internet"},
            {"series": "RAZ", "level": "V", "name": "Desert Ecosystems: Extreme Adaptations"},
            {"series": "RAZ", "level": "V", "name": "Ancient Chinese Dynasties"},
            {"series": "RAZ", "level": "V", "name": "Robotics in Healthcare"},
            {"series": "RAZ", "level": "V", "name": "Climate Patterns and Global Weather"},
            {"series": "RAZ", "level": "V", "name": "Renaissance Science and Inventions"},
            {"series": "RAZ", "level": "V", "name": "Marine Pollution: Causes and Solutions"},
            {"series": "RAZ", "level": "V", "name": "The Art of Origami: History and Techniques"},
            {"series": "RAZ", "level": "V", "name": "Volcanic Islands: Formation and Life"},
            {"series": "RAZ", "level": "V", "name": "The French and Indian War"},
            {"series": "RAZ", "level": "V", "name": "Hibernation: How Animals Survive Winter"},
            {"series": "RAZ", "level": "V", "name": "Modern Architecture: Form and Function"},
            {"series": "RAZ", "level": "V", "name": "Genetically Modified Organisms (GMOs)"},
            {"series": "RAZ", "level": "V", "name": "The Silk Road: Cultural Exchanges"},
            {"series": "RAZ", "level": "V", "name": "Jupiter and Its Moons"},
            {"series": "RAZ", "level": "V", "name": "Sign Language: Communication Without Sound"},
            {"series": "RAZ", "level": "V", "name": "The Industrial Revolution in America"},
            {"series": "RAZ", "level": "V", "name": "Coral Reef Restoration"},
            {"series": "RAZ", "level": "V", "name": "Mythology: Gods and Heroes of Greece"},
            {"series": "RAZ", "level": "V", "name": "Astronomy: Tools of the Trade"},
            {"series": "RAZ", "level": "V", "name": "The History of Jazz Music"},
            {"series": "RAZ", "level": "V", "name": "Endangered Species: Conservation Efforts"},
            {"series": "RAZ", "level": "V", "name": "Plate Tectonics and Continental Drift"},
            {"series": "RAZ", "level": "V", "name": "Folktales from Around the Globe"}           
        ]
    }


@app.get("/sendBook", status_code=status.HTTP_200_OK)
def send_book(series: str, level: str, name: str):
    try:
        # 获取API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return {
                "success": False,
                "message": "API key not found",
                "error_code": "API_KEY_MISSING",
            }, status.HTTP_400_BAD_REQUEST

        # 创建OpenAI客户端
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        # 调用API
        response = client.chat.completions.create(
            model="deepseek-chat",
            temperature=1,
            messages=[
                {
                    "role": "user",
                    "content": f"我是7岁男孩，每天会以昨晚看的书作为topic来和外教老师进行英语口语练习，帮我根据{series}系列{level}级别并且书名为{name}的书生成3个子topic，要求是英文的，并且包含book的名称以及章节名称，长度在不超过200个英文单词，你的口吻是家长给老师写的课前便签",
                }
            ],
            stream=False,
        )

        # 提取结果
        content = response.choices[0].message.content
        print(content)
        # 返回成功响应
        return {"success": True, "message": content}

    except Exception as e:
        # 捕获所有异常并返回错误响应
        return {
            "success": False,
            "message": str(e),
            "error_code": "SERVER_ERROR",
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
