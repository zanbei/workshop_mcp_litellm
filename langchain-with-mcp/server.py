from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FashionRequest(BaseModel):
    city: str
    time_period: str
    style: str
    age: str

# Create a single MCP server with both tools
mcp = FastMCP("WeatherFashion")

@mcp.tool()
async def get_weather(location: str) -> str:
    weather_data = {
        "Copenhagen": {"temperature": "18C", "description": "多云"},
        "Beijing": {"temperature": "25C", "description": "晴朗"},
        "Berlin": {"temperature": "20C", "description": "晴空万里"},
        "Paris": {"temperature": "22C", "description": "阴天"},
        "Phuket": {"temperature": "32C", "description": "热带气候"},
        "Shanghai": {"temperature": "28C", "description": "潮湿"}
    }

    try:
        if location not in weather_data:
            return json.dumps({
                "error": f"没有{location}的天气数据。可用城市：{', '.join(weather_data.keys())}",
                "location": location,
            })

        data = weather_data[location]
        response = {
            "location": location,
            "temperature": data["temperature"],
            "description": data["description"],
        }

        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "error": f"发生错误：{str(e)}",
            "location": location,
        })

@mcp.tool()
async def get_fashion(location: str, temperature: str, time_period: str = "下午", age: str = "25", style: str = "休闲") -> str:
    # Parse temperature
    temp_value = float(temperature.replace("C", ""))
    
    # Adjust temperature perception based on time period
    temp_adjustments = {
        "上午": -2,  # 早上感觉较凉
        "下午": 0,   # 基准温度
        "晚上": -3,  # 晚上较凉
        "凌晨": -5   # 最冷
    }
    adjusted_temp = temp_value + temp_adjustments.get(time_period, 0)

    # Get age group specific modifications
    try:
        age_num = int(age)
        if age_num < 18:
            age_group = "teen"
        elif age_num < 30:
            age_group = "young"
        elif age_num < 50:
            age_group = "adult"
        else:
            age_group = "senior"
    except ValueError:
        age_group = "adult"

    # Basic advice based on adjusted temperature and time period
    if adjusted_temp < 10:
        base_clothing = {
            "休闲": {
                "外套": "保暖羽绒服或休闲羊毛大衣",
                "上装": "厚毛衣或连帽衫",
                "下装": "保暖牛仔裤或保暖裤",
                "配饰": "毛线帽和保暖围巾",
                "鞋子": "保暖运动鞋或靴子"
            },
            "商务": {
                "外套": "羊毛大衣或风衣",
                "上装": "西装搭配保暖内衣",
                "下装": "羊毛西裤",
                "配饰": "皮手套和羊绒围巾",
                "鞋子": "皮靴或皮鞋"
            },
            "优雅": {
                "外套": "长款羊绒大衣",
                "上装": "高领毛衣搭配西装外套",
                "下装": "羊毛西裤或长裙",
                "配饰": "设计师围巾和皮手套",
                "鞋子": "高跟靴或正装鞋"
            },
            "运动": {
                "外套": "保暖运动夹克",
                "上装": "保暖内衣搭配抓绒衣",
                "下装": "保暖运动裤",
                "配饰": "运动帽和保暖围脖",
                "鞋子": "保暖跑鞋"
            }
        }
    elif adjusted_temp < 20:
        base_clothing = {
            "休闲": {
                "外套": "轻薄牛仔夹克或连帽衫",
                "上装": "长袖T恤或轻薄毛衣",
                "下装": "牛仔裤或休闲裤",
                "配饰": "轻薄围巾或帽子",
                "鞋子": "运动鞋或休闲鞋"
            },
            "商务": {
                "外套": "轻薄西装外套",
                "上装": "衬衫或女式衬衫",
                "下装": "西裤或铅笔裙",
                "配饰": "轻薄围巾或口袋方巾",
                "鞋子": "正装鞋或乐福鞋"
            },
            "优雅": {
                "外套": "轻薄风衣或设计师夹克",
                "上装": "丝质衬衫或精致针织衫",
                "下装": "修身裤或中长裙",
                "配饰": "丝巾或精致首饰",
                "鞋子": "高跟鞋或设计师平底鞋"
            },
            "运动": {
                "外套": "轻薄运动夹克或防风衣",
                "上装": "速干长袖",
                "下装": "运动裤或短裤",
                "配饰": "运动帽或头带",
                "鞋子": "跑鞋或训练鞋"
            }
        }
    else:
        base_clothing = {
            "休闲": {
                "外套": "可选轻薄夹克",
                "上装": "T恤或短袖衬衫",
                "下装": "短裤或轻薄长裤",
                "配饰": "太阳镜和帽子",
                "鞋子": "轻便运动鞋或凉鞋"
            },
            "商务": {
                "外套": "轻薄西装外套（可选）",
                "上装": "短袖衬衫或女式衬衫",
                "下装": "轻薄西裤或裙子",
                "配饰": "口袋方巾或轻薄围巾",
                "鞋子": "透气正装鞋"
            },
            "优雅": {
                "外套": "轻薄开衫或披肩",
                "上装": "无袖衬衫或轻薄丝质上衣",
                "下装": "轻薄面料长裤或夏季连衣裙",
                "配饰": "精致首饰或丝巾",
                "鞋子": "露趾高跟鞋或优雅凉鞋"
            },
            "运动": {
                "外套": "超轻运动夹克",
                "上装": "速干背心或T恤",
                "下装": "运动短裤或裙裤",
                "配饰": "遮阳帽和运动头带",
                "鞋子": "透气跑鞋"
            }
        }

    # Get style-specific clothing
    style_clothing = base_clothing.get(style, base_clothing["休闲"])

    # Time-specific adjustments
    time_specific_tips = {
        "上午": {
            "teen": "早上较凉，注意分层穿搭。别忘了带上学校/活动用的包！",
            "young": "选择可以随着天气变暖逐层脱下的衣物。",
            "adult": "专业的早晨着装，注意温度变化时的分层。",
            "senior": "容易脱换的保暖层次，搭配舒适的步行鞋。"
        },
        "下午": {
            "teen": "适合活动和社交的舒适时尚装扮。",
            "young": "适合工作/休闲活动的平衡搭配。",
            "adult": "适合会议/活动的专业舒适着装。",
            "senior": "轻薄透气的衣物，注意防晒。"
        },
        "晚上": {
            "teen": "和朋友晚上活动时添加一件轻薄外套。",
            "young": "适合晚间社交活动或晚餐的时尚装扮。",
            "adult": "适合晚餐或活动的优雅晚装。",
            "senior": "保暖舒适的晚间装扮，注意保温。"
        },
        "凌晨": {
            "teen": "夜间外出时注意保暖和可见度。",
            "young": "夜间活动时既时尚又保暖的装扮。",
            "adult": "夜间活动的优雅保暖着装。",
            "senior": "夜间额外的保暖层次，注重舒适。"
        }
    }

    # City-specific advice with time period considerations
    city_specific = {
        "Copenhagen": {
            "城市特点": "北欧时尚之都，极简主义风格",
            "穿衣风格": "简约优雅，主要以黑、白、灰为主",
            "文化建议": "保守着装，注重环保意识",
            "特别提示": {
                "上午": "清晨较凉，尤其靠近水域时注意保暖",
                "下午": "大多数场合适合商务休闲装",
                "晚上": "晚间活动添加时尚外层",
                "凌晨": "保暖层次和反光细节注意安全"
            },
            "适合场所": "设计博物馆、新港、小美人鱼雕像",
            "禁忌": "避免过于花哨的装扮"
        },
        "Beijing": {
            "城市特点": "现代与传统并存的国际大都市",
            "穿衣风格": "优雅实用",
            "文化建议": "参观景点时着装正式",
            "特别提示": {
                "上午": "注意分层穿搭和空气质量",
                "下午": "建议防晒和戴口罩",
                "晚上": "餐饮娱乐场所适合商务休闲装",
                "凌晨": "夜间较凉注意保暖"
            },
            "适合场所": "故宫、长城、胡同",
            "禁忌": "参观寺庙时避免暴露着装"
        },
        "Berlin": {
            "城市特点": "前卫艺术与历史文化的融合",
            "穿衣风格": "个性化，街头风格流行",
            "文化建议": "着装可以大胆创新",
            "特别提示": {
                "上午": "清晨较凉注意保暖",
                "下午": "街头风格适合大多数场合",
                "晚上": "创意前卫的晚装",
                "凌晨": "夜店跳舞注意保暖"
            },
            "适合场所": "博物馆岛、勃兰登堡门、东边画廊",
            "禁忌": "参观纪念馆时避免不当着装"
        },
        "Paris": {
            "城市特点": "全球时尚之都",
            "穿衣风格": "优雅时尚，注重细节",
            "文化建议": "偏向正式优雅",
            "特别提示": {
                "上午": "早晨咖啡馆适合时尚休闲装",
                "下午": "购物时间优雅日装",
                "晚上": "晚餐和活动需要盛装",
                "凌晨": "精致的夜间着装"
            },
            "适合场所": "埃菲尔铁塔、卢浮宫、香榭丽舍大街",
            "禁忌": "正式场合避免运动装"
        },
        "Phuket": {
            "城市特点": "热带岛屿度假胜地",
            "穿衣风格": "轻便凉爽，度假风格",
            "文化建议": "注意泰国文化礼仪",
            "特别提示": {
                "上午": "活动时穿着轻便透气",
                "下午": "防晒必不可少",
                "晚上": "晚餐时间商务休闲装",
                "凌晨": "晚风轻薄层次"
            },
            "适合场所": "海滩、寺庙、夜市",
            "禁忌": "参观寺庙时着装得体"
        },
        "Shanghai": {
            "城市特点": "现代国际大都市",
            "穿衣风格": "时尚前卫，融合东西方元素",
            "文化建议": "着装可以时尚大胆",
            "特别提示": {
                "上午": "商务区适合正装",
                "下午": "前卫时尚的日装",
                "晚上": "潮流晚装",
                "凌晨": "夜生活时尚层次"
            },
            "适合场所": "外滩、豫园、田子坊",
            "禁忌": "特殊场合避免过于休闲的着装"
        }
    }

    # Get city-specific information
    city_info = city_specific.get(location, {
            "城市特点": "请查看当地特点",
            "穿衣风格": "建议了解当地穿衣习惯",
            "文化建议": "注意当地文化",
            "特别提示": {
                "上午": "查看当地早晨天气",
                "下午": "了解当地下午情况",
                "晚上": "了解当地晚间活动",
                "凌晨": "了解当地夜间情况"
            },
            "适合场所": "请查看当地旅游信息",
            "禁忌": "注意着装得体"
    })

    # Combine response
    response = {
        "Location": location,
        "Time Period": time_period,
        "Temperature": {
            "Actual": temperature,
            "Feels Like": f"{adjusted_temp}C"
        },
        "User Profile": {
            "Age Group": age_group,
            "Style Preference": style
        },
        "Clothing Recommendations": style_clothing,
        "Time-Specific Advice": time_specific_tips[time_period][age_group],
        "City-Specific Advice": city_info,
        "天气提醒": f"当前{time_period}体感温度{adjusted_temp}度，" + (
            "请注意保暖" if adjusted_temp < 10 else
            "温度适中" if adjusted_temp < 20 else
            "请注意防晒降温"
        )
    }

    return json.dumps(response, ensure_ascii=False, indent=2)

@app.post("/fashion-advice")
async def fashion_advice(request: FashionRequest):
    try:
        # Get weather data
        weather_result = await get_weather(request.city)
        weather_data = json.loads(weather_result)
        
        if "error" in weather_data:
            raise HTTPException(status_code=400, detail=weather_data["error"])
        
        # Get fashion advice
        fashion_result = await get_fashion(
            location=request.city,
            temperature=weather_data["temperature"],
            time_period=request.time_period,
            age=request.age,
            style=request.style
        )
        
        return json.loads(fashion_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    mcp.run(transport="sse")
    uvicorn.run(app, host="0.0.0.0", port=8000)
